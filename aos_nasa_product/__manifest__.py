# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Product Nasa',
    'version' : '1.0',
    'summary': 'Set Standard Product Nasa',
    'sequence': 1,
    "author": "Alphasoft",
    'description': """
This module is aim to add standard Product Nasa
    """,
    'category' : 'Partners',
    'website': 'https://www.alphasoft.co.id/',
    'images' : [],
    'depends' : ['product','aos_base_product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/product_view.xml',
        'views/res_partner_views.xml',
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
