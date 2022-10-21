import json
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import http
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.addons.web.controllers.main import Home, ensure_db
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL




_logger = logging.getLogger(__name__)
    

class ProductData(WebsiteSale):

    def _compute_item_per_row(self, items, ppr=3):
        payload = []
        for item in range(len(items)//ppr):
            payload.append([i for i in items[item*ppr:item*ppr+ppr]])
        if len(items) % ppr != 0:
            payload.append([i for i in items[
                ((len(items)//ppr)*ppr):((len(items)//ppr)*ppr) + ((len(items) % ppr) + 1)
            ]])
        _logger.info(payload)
        return payload

    @http.route('/home/banner/metadata', auth='public', type='http', website=True)
    def home_banner(self, **kwargs):
        """This will returns the banners list"""

        sliders = request.env['ir.attachment'].sudo().search([('slider_image', '=', True)])
        values = {'sliders': sliders}
        return request.render('loonwholesale.loon_banner_snippet', values)

    @http.route('/home/collections/metadata', auth='public', type='http', website=True)
    def home_page_products(self, **kwargs):
        """This will returns the collections [categories] list"""

        collections = request.env['product.public.category'].sudo().search([], limit=8)
        values = {'categs': collections}
        return request.render('loonwholesale.loon_collections_snippet', values)

    @http.route('/home/featured/metadata', auth='public', type='http', website=True)
    def home_featured_products(self, **kwargs):
        product = request.env['product.template'].sudo().search([
            ('is_featured', '=', True)
        ], limit=4)
        values = {'featured_products': product}
        return request.render('loonwholesale.loon_featured_products_snippet', values)


    @http.route(
        '/collections', 
        auth='public', type='http', website=True)
    def collections(self, **post):
        collections = request.env['product.public.category'].sudo().search([])
        values = {
            'bins': self._compute_item_per_row(collections),
        }
        return request.render("loonwholesale.loon_products", values)

    @http.route('/top-category-list', auth='public', type='http', website=True)
    def top_category_list(self, **post):
        pro_temp_obj = request.env['product.template'].sudo()
        top_menus = request.env['product.public.category'].sudo().search([])
        # for menu in top_menus:
        #     pro_temp_obj.search([('public_categ_ids.ids', 'contains', menu.id)])
        values = {
            'bins': [t.name for t in top_menus],
        }
        return request.render("loonwholesale.loonwhole_template_header_default", values)

    @http.route('/featured-products', auth='public', type='http', website=True)
    def featured(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        try:
            min_price = float(min_price)
        except ValueError:
            min_price = 0
        try:
            max_price = float(max_price)
        except ValueError:
            max_price = 0

        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/featured-products', category=category and int(category), search=search, attrib=attrib_list, min_price=min_price, max_price=max_price, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            company_currency = request.website.company_id.currency_id
            conversion_rate = request.env['res.currency']._get_conversion_rate(company_currency, pricelist.currency_id, request.website.company_id, fields.Date.today())
        else:
            conversion_rate = 1

        url = "/featured-products"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        options = self._get_search_options(
            category=category,
            attrib_values=attrib_values,
            pricelist=pricelist,
            min_price=min_price,
            max_price=max_price,
            conversion_rate=conversion_rate,
            **post
        )
        # No limit because attributes are obtained from complete product list
        product_count, details, fuzzy_search_term = request.website._search_with_fuzzy("products_only", search,
            limit=None, order=self._get_search_order(post), options=options)
        search_product = details[0].get('results', request.env['product.template']).with_context(bin_size=True)
        search_product = search_product.search([('is_featured', '=', True)])
        product_count = len(search_product)

        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            # TODO Find an alternative way to obtain the domain through the search metadata.
            Product = request.env['product.template'].with_context(bin_size=True)
            domain = self._get_search_domain(search, category, attrib_values)

            # This is ~4 times more efficient than a search for the cheapest and most expensive products
            from_clause, where_clause, where_params = Product._where_calc(domain).get_sql()
            query = f"""
                SELECT COALESCE(MIN(list_price), 0) * {conversion_rate}, COALESCE(MAX(list_price), 0) * {conversion_rate}
                  FROM {from_clause}
                 WHERE {where_clause}
            """
            request.env.cr.execute(query, where_params)
            available_min_price, available_max_price = request.env.cr.fetchone()

            if min_price or max_price:
                # The if/else condition in the min_price / max_price value assignment
                # tackles the case where we switch to a list of products with different
                # available min / max prices than the ones set in the previous page.
                # In order to have logical results and not yield empty product lists, the
                # price filter is set to their respective available prices when the specified
                # min exceeds the max, and / or the specified max is lower than the available min.
                if min_price:
                    min_price = min_price if min_price <= available_max_price else available_min_price
                    post['min_price'] = min_price
                if max_price:
                    max_price = max_price if max_price >= available_min_price else available_max_price
                    post['max_price'] = max_price

        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/featured-products/category/%s" % slug(category)

        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = pager['offset']
        products = search_product[offset:offset + ppg]

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([
                ('product_tmpl_ids', 'in', search_product.ids),
                ('visibility', '=', 'visible')
            ])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'order': post.get('order', ''),
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if filter_by_price_enabled:
            values['min_price'] = min_price or available_min_price
            values['max_price'] = max_price or available_max_price
            values['available_min_price'] = tools.float_round(available_min_price, 2)
            values['available_max_price'] = tools.float_round(available_max_price, 2)
        if category:
            values['main_object'] = category
        values.update(self._get_additional_shop_values(values))
        return request.render("loonwholesale.featured_products", values)
