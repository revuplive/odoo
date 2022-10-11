# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    product_deal = fields.Many2one('product.template', string="Product to showcase",
                                   config_parameter="theme_loonwholesale.product_data")

    product_date = fields.Datetime(string="Deal End Date", config_parameter="theme_loonwholesale.product_date")


