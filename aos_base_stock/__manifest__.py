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
    'name': 'Stock Base',
    'version': '12.0.0.1.0',
    'author': "Alphasoft",
    'sequence': 1,
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'license': 'AGPL-3',
    'category': 'Sales',
    'summary': 'Stock Base of a module by Alphasoft',
    'depends': ['stock'],
    'description': """
Module based on Alphasoft
=====================================================
""",
    'demo': [],
    'test': [],
    'data': [
        "security/stock_security.xml",
        #'report/report_stock_traceability.xml',
        'views/stock_picking_view.xml',
        'views/stock_move_line_view.xml',
        'views/product_view.xml',
        'views/res_partner_view.xml',
        #'views/res_config_views.xml',
     ],
    'css': [],
    'js': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
