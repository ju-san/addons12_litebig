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
    'name': 'Stock Allocation',
    'version': '12.0.0.1.0',
    'author': "Alphasoft",
    'sequence': 1,
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'license': 'AGPL-3',
    'category': 'Sales',
    'summary': 'Stock Split Allocation from Picking Operation',
    'depends': ['stock'],
    'description': """
Module based on Alphasoft
=====================================================
""",
    'demo': [],
    'test': [],
    'data': [
        #"security/stock_security.xml",
        'wizard/stock_picking_split_views.xml',
        'views/stock_picking_view.xml',
        #'views/stock_move_line_view.xml',
        #'views/product_view.xml',
     ],
    'css': [],
    'js': [],
    'price': 55.00,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
}
