from email.policy import default
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class IrAttachments(models.Model):
    _inherit = 'ir.attachment'

    slider_image = fields.Boolean('Is slider image', default=False)
    seq = fields.Integer(default=1)

class PublicCategory(models.Model):
    _inherit = 'product.public.category'

    add_info = fields.Html("Additional Information")


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    is_featured = fields.Boolean(default=False)
