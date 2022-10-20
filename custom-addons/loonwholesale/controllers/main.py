import json
import logging
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home, ensure_db
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.addons.website_sale.controllers.main import TableCompute


_logger = logging.getLogger(__name__)
    

class ProductData(http.Controller):

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


    @http.route('/collections', auth='public', type='http', website=True)
    def collections(self, ppg=False, **post):
        collections = request.env['product.public.category'].sudo().search([])
        # if ppg:
        #     try:
        #         ppg = int(ppg)
        #         post['ppg'] = ppg
        #     except ValueError:
        #         ppg = False
        # if not ppg:
        #     ppg = request.env['website'].get_current_website().shop_ppg or 20
        # ppr = request.env['website'].get_current_website().shop_ppr or 4
        values = {
            'bins': collections,
            # 'ppg': ppg,
            # 'ppr': ppr,
        }
        return request.render("loonwholesale.loon_products", values)
