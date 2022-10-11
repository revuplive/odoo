{
    'name': 'Theme Loonwholesale',
    'description': 'Theme Loonwholesale is an attractive and modern eCommerce Website theme for vape products',
    'summary': 'Theme Loonwholesale is a custom theme for the Loonwholesale webshop',
    'category': 'Theme/eCommerce',
    'version': '15.0.1.0.1',
    'author': 'Steve Yerigan Odd',
    'company': 'Steve Yerigan Odd',
    'maintainer': 'Steve Yerigan Odd',
    'website': "",
    'depends': ['website_blog', 'website_sale_wishlist', 'website_sale',
                'website_sale_comparison'],
    'data': [
        "views/snippets/banner.xml",
        "views/snippets/product_deal.xml",
        "views/res_config_settings.xml",
        "views/product_deal_data.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            "/theme_loonwholesale/static/src/scss/style.scss",
            "/theme_loonwholesale/static/src/js/product_deal.js",
            "theme_loonwholesale/static/src/js/clean_product_deal.js"
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
