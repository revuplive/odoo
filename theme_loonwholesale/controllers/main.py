from odoo import http
from odoo.http import request


class ProductData(http.Controller):

    @http.route('/get_product_loon', auth='public', type='json', website=True)
    def get_products(self, **kwargs):
        print('Vo controller')
        product_id = request.env['ir.config_parameter'].sudo().get_param('theme_loonwholesale.product_data')
        product = request.env['product.template'].sudo().search([('id', '=', product_id)])
        print(product)
        values = {'product': product}
        response = http.Response(template='theme_loonwholesale.product_deal_data', qcontext=values)
        return response.render()

    @http.route('/get_countdown_loon', auth='public', type='json', website=True)
    def get_countdown(self, **kwargs):
        end_date = request.env['ir.config_parameter'].sudo().get_param('theme_loonwholesale.product_date')
        return end_date
