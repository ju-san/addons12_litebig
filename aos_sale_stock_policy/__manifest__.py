# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2017 Alphasoft
#    (<http://www.adeanshori.co.id>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Sale Stock Policy',
    'version': '12.0.0.1.0',
    'author': "Alphasoft",
    'sequence': 1,
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'license': 'AGPL-3',
    'category': 'Sales',
    'summary': 'Advance of a module by Alphasoft',
    'depends': ['sale', 'sale_stock'],
    'description': """
The Shipping Policy is used to synchronise invoice and delivery operations.
      - The 'Pay Before delivery' choice will first generate the invoice and then generate the picking order after the payment of this invoice.
      - The 'Shipping & Manual Invoice' will create the picking order directly and wait for the user to manually click on the 'Invoice' button to generate the draft invoice.
      - The 'Invoice From The Picking' choice is used to create an invoice during the picking process.
""",
    'demo': [],
    'test': [],
    'data': [
        #"security/sale_security.xml",
        #'views/account_payment_view.xml',
        'views/sale_view.xml',
        'views/stock_view.xml',
        #'views/res_config_views.xml',
     ],
    'css': [],
    'js': [],
    'price': 75.00,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
}
