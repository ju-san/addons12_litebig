# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Products Dimension',
    "version": '12.0.1.0.0',
    "license": 'AGPL-3',
    'summary': 'Products Catalog for Alphasoft Customer',
    'sequence': 1,
    "author": "Alphasoft",
    'description': """
This is the base module for managing products and dimension in Odoo.
* Length x Weight x Height
* Packages
    """,
    'category' : 'Sales',
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'depends' : ['base', 'product'],
    'data': [
        'security/product_security.xml',
        'views/product_template_view.xml',
        'views/product_view.xml',
    ],
    'demo': [
        
    ],
    'qweb': [
        
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    #'post_init_hook': '_auto_install_l10n',
}
