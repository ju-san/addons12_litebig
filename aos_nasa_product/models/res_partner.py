# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class PricelistGroup(models.Model):
    _name = "product.pricelist.group"
    _description = 'Pricelist Group User'
    
    name = fields.Char('Pricelist User', required=True, translate=True)
    
class Pricelist(models.Model):
    _inherit = "product.pricelist"
    
    name = fields.Char('Pricelist Wilayah', required=True, translate=True)
    partner_category_id = fields.Many2one('res.partner.category', string="Partner Tags")
    partner_group_id = fields.Many2one('product.pricelist.group', string="Pricelist User")
     
    
class Partner(models.Model):
    _inherit = 'res.partner'
    
    show_range = fields.Boolean('Show Range')
    partner_group_id = fields.Many2one('product.pricelist.group', string="Pricelist User")
    property_stock_warehouse_id = fields.Many2one(
        'stock.warehouse', string="Warehouse Location",
        help="The stock location used as destination when sending goods to this contact.")