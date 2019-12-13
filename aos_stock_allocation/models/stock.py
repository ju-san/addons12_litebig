# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockLocation(models.Model):
    _inherit = 'stock.location'
    
    split_location = fields.Boolean('Is a Split Location?', help='Check this box to allow using this location as a split location.')
                