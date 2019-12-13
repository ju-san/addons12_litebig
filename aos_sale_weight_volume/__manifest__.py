# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Sale Weight & Volume',
    'version': '11.0.0.1.0',
    "license": 'AGPL-3',
    'category': 'Sales',
    'sequence': 1,
    "author": "Alphasoft",
    'summary': 'Sale Order Management',
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'description': """
* Weight and Volume on Purchase
    """,
    'depends': [
                'sale_management',
#                 'stock',
#                 'stock_account',
#                 'aos_base',
                'aos_base_sale',
                'aos_product_dimension',
#                 'aos_currency_set_rate',
#                 'aos_stock',
#                 'aos_account',
                #'report_webkit', 
                #'purchase_requisition',
                #'aos_tree_image',
                #'portal', 
                #'aos_purchase'
                ],
    'data': [
#         'security/purchase_order_security.xml',
#         'security/procurement_security.xml',
#         'security/ir.model.access.csv',
#         'wizard/set_currency_rate_view.xml',
        #'wizard/rejected_reason_rfq_view.xml',
#         'data/purchase_sequence.xml',
#         'data/purchase_dashboard.xml',
#         'data/purchase_type_data.xml',
#         'views/product_view.xml',
        'views/sale_order_view.xml',
#         'views/stock_view.xml',
#         'views/account_invoice_view.xml',
        #'report/report_purchase_order.xml',
        #'views/purchase_contract_view.xml',
#         'views/res_config_views.xml',
        #'portal_sale_data.xml',
    ],
    "demo": [
#         "demo/purchase_order_demo.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
