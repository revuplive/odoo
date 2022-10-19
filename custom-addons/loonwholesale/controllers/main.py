import json
import logging
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home, ensure_db
from odoo.exceptions import AccessError, UserError, AccessDenied



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
