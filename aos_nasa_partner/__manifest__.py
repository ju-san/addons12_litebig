# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Partner Nasa',
    'version' : '1.0',
    'summary': 'Set Standard Partner & Company',
    'sequence': 1,
    "author": "Alphasoft",
    'description': """
This module is aim to add standard partner & company for Adaa
* NPWP
    """,
    'category' : 'Partners',
    'website': 'https://www.alphasoft.co.id/',
    'images' : [],
    'depends' : ['base',
                 'mail',
                 'contacts', 
                 #'efaktur',
                 #'web_google_maps',
                 ],
    'data': [
        'data/partner_sequence.xml',
        #'data/email.xml',
        'data/mail_subtype.xml',
        #"wizard/partner_geo_localize_view.xml",
        #'security/ir.model.access.csv',
        "security/partner_security.xml",
        "views/partner_view.xml",
        "views/company_view.xml",
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
