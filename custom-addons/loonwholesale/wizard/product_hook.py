import zipfile
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging
import io
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

CATEG_IMG = []


# attribute_line_ids - product.template.attribute.line
# product.template.attribute.value - black/white 

# attribute_id - product.attribute
# value_ids - product.attribute.value

class ProductWizard(models.TransientModel):
    _name = "product.wizard"
    _description = "Upload products"

    name = fields.Char('Name')
    product_file = fields.Binary("Product Zip FIle")

    def __check_product(self, name):
        pro = self.env['product.template'].search([
            ('name', '=', name)
        ])
        if pro:
            return pro[0]
        return False
    
    def __check_categ(self, name):
        categ = self.env['product.public.category'].search([
            ('name', '=', name)
        ])
        if categ:
            return categ[0]
        return False

    def __create_category(self, category, imgdata):
        if category not in CATEG_IMG:
            cid = self.__check_categ(category)
            if not cid:
                cid = self.env['product.public.category'].create({
                    'name': category,
                    'image_1920': imgdata
                })
            CATEG_IMG.append(category)
        else:
            cid = self.env['product.public.category'].search([(
                'name', '=' ,category
            )], limit=1)

        _logger.info("caregory id: %s ", cid)
        return cid

    def __create_variant(self, pid, variant):
        aid = self.env['product.attribute'].create({
            "name": variant,
            "product_tmpl_ids": [(4, pid.id, 0)]
        })
        avid = self.env['product.attribute.value'].create({
            "name": variant,
            "attribute_id": aid.id
        })
        vid = self.env['product.template.attribute.line'].create({
            'attribute_id': aid.id,
            'value_ids': [(4, avid.id, 0)],
            'product_tmpl_id': pid.id
        })
        pid.attribute_line_ids = [(4, vid.id, 0)]

    def _process_product(self, path, imgdata):
        variant = False
        pathnames = path.split('/')[1:]
        _logger.info(pathnames)
        # without variant
        if len(pathnames) == 2:
            category = pathnames[0]
            pro_name = pathnames[-1].split('.')[0]

        # with variant
        if len(pathnames) == 3:
            category = pathnames[0]
            variant = pathnames[1]
            pro_name = ".".join(pathnames[-1].split('.')[:-1])

        # create category
        if category:
            cid = self.__create_category(category, imgdata)
            pro_exist = self.__check_product(pro_name)
            if not pro_exist:
                product_tmpl_id = self.env['product.template'].create({
                    'name': pro_name,
                    'image_1920': imgdata,
                    'public_categ_ids': [(4, cid.id, 0)]
                })
            else:
                product_tmpl_id = pro_exist
            if variant:
                self.__create_variant(product_tmpl_id, variant)


    def action_uplaod(self):
        """
        UPLOADING FORMAT
        ----------------
        - folder_name/category/product/product_img.png/jpg
        - folder_name/category/product/variant/product_img.png/jpg

        Example:
        - Loon/Loon Typhoon, Tanks, and Coils/Baby Blue Typhoon.png
        - Loon/Loon Reloaded + Reloaded Pods/Black/Black Reloaded.png

        """
        for rec in self:
            data = base64.b64decode(rec.product_file)
            try:
                with zipfile.ZipFile(io.BytesIO(data), 'r') as z:
                    for att_name in z.namelist():
                        if '.png' in att_name.lower() or '.jpg' in att_name.lower():
                            img_data = z.read(att_name)
                            # bytes_io = img_data.decode('utf-8')
                            bytes_io = base64.encodebytes(img_data)
                            self._process_product(att_name, bytes_io)
            except Exception as err:
                _logger.error("Error: %s", str(err))