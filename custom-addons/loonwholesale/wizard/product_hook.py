from zipfile import ZipFile

# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging
from io import StringIO
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductWizard(models.TransientModel):
    _name = "product.wizard"
    _description = "Upload products"

    name = fields.Char('Name')
    product_file = fields.Binary("Product Zip FIle")


    def action_uplaod(self):
        zf = ZipFile(base64.b64decode(self.product_file))
        _logger.info("------- %s -------", zf.namelist())
        with ZipFile(self.product_file) as zf:
            _logger.info(zf)
            for file in zf.namelist():
                _logger.info('%s', file)
                # if not file.endswith('.png'): # optional filtering by filetype
                #     continue
                # with zf.open(file) as f:
                    # image = pygame.image.load(f, namehint=file)