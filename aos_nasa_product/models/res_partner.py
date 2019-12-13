# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class Pricelist(models.Model):
    _inherit = "product.pricelist"
    
    name = fields.Char('Pricelist Wilayah', required=True, translate=True)
    partner_category_id = fields.Many2one('res.partner.category', string="Pricelist User")
    
    
class Partner(models.Model):
    _inherit = 'res.partner'

    property_stock_warehouse_id = fields.Many2one(
        'stock.warehouse', string="Warehouse Location",
        help="The stock location used as destination when sending goods to this contact.")