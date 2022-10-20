# -*- coding: utf-8 -*-
{
    'name': 'Theme Loonwholesale',
    'description': 'Theme Loonwholesale is an attractive and modern eCommerce Website theme for vape products',
    'summary': 'Theme Loonwholesale is a custom theme for the Loonwholesale webshop',
    'category': 'Theme/eCommerce',
    'version': '15.0.1.0.1',
    'author': 'Rahul Mehra',
    'company': 'Magnetposts',
    'maintainer': 'Magnetposts',
    'website': "https://magnetposts.com",
    'depends': ['base', 'website_sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/product_template_view.xml",
        "views/ir_attachment.xml",
        "views/snippets/banner.xml",
        "views/snippets/collections.xml",
        "views/snippets/featured_products.xml",
        "views/snippets/cart_summary.xml",
        "wizard/product_hook_view.xml",
        "views/template.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            # "/theme_loonwholesale/static/src/scss/style.scss",
            # "/theme_loonwholesale/static/src/js/product_deal.js",
            # "theme_loonwholesale/static/src/js/clean_product_deal.js"
        ],
    },
    'images': [
        'static/description/banner.png',
        # 'static/description/theme_screenshot.png',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
