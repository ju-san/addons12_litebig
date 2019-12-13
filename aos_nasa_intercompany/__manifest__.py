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
    'name': 'Intercompany Transaction',
    'version': '12.0.0.1.0',
    'sequence': 1,
    'summary': 'Intercompany Transaction by Alphasoft.',
    'author': "Alphasoft",
    'website': 'https://www.alphasoft.co.id/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'description': 'Module based on Alphasoft',
    'depends': [
                'sale',
                'purchase',
                'stock',
                'account',
                'aos_nasa_sale',
                'aos_nasa_purchase',
                #'aos_base',
                ],
    'data': [
             'security/security.xml',
             'views/purchase_views.xml',
             'views/sale_views.xml',
             'views/res_users_view.xml',
             'views/company_views.xml',
             'views/stock_views.xml',
     ],
    'demo': [],
    'test': [],
    'qweb': [],
    'css': [],
    'js': [],
    'installable': True,
    'auto_install': False,
}
