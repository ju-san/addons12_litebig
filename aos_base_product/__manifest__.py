# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2017 Alphasoft
#    (<https://www.alphasoft.co.id/>).
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
    'name': 'Base Product',
    'version': '12.0.0.1.0',
    'author': "Alphasoft",
    'sequence': 1,
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'license': 'AGPL-3',
    'category': 'Stock',
    'summary': 'Base Product of a module by Alphasoft.',
    'depends': ['product'],
    'description': '''Allows you to add delivery methods in sale orders and picking.
==============================================================
You can define your own carrier for prices. When creating
invoices from picking, the system is able to add and compute the shipping line.''',
    'demo': [],
    'test': [],
    'data': [
        'security/product_security.xml',
        'views/product_view.xml',
     ],
    'css': [],
    'js': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
