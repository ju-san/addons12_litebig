# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from num2words import num2words
from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, UserError
import odoo.addons.decimal_precision as dp
from odoo.tools.float_utils import float_is_zero, float_compare
import math
#from odoo.addons.aos_base import amount_to_text_id
def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.multi
    @api.depends('order_line.tot_weight','order_line.tot_volume')
    def _compute_weight(self):
        for rec in self:
            weight_tot = volume_tot = 0
            for line in rec.order_line:
                if line.product_id:
                    weight_tot += line.tot_weight or 0.0
                    volume_tot += line.tot_volume or 0.0
            rec.weight = weight_tot#round_down(weight_tot)
            rec.volume = volume_tot#round_up(volume_tot)
    
    show_wv = fields.Boolean('Weight/Volume')
    weight = fields.Float(string='Total Weight (kg)', compute='_compute_weight', store=True)
    volume = fields.Float(string='Total Volume (m³)', compute='_compute_weight', store=True)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = 'Sale Order Line' 
            
    @api.depends('product_id', 'product_id.weight', 'product_id.volume')
    def _get_weight(self):
        for line in self:
            line.weight = line.product_id.weight# * line.product_qty
            line.volume = line.product_id.volume# * line.product_qty
            
    @api.depends('weight', 'volume', 'product_uom_qty')
    def _compute_weight(self):
        for line in self:
            line.tot_weight = round_down(line.product_id.weight * line.product_uom_qty, 1)
            line.tot_volume = line.product_uom_qty * (((line.product_id.height_dimension * \
                              line.product_id.length_dimension * \
                              line.product_id.width_dimension)/1000000.0) \
                              / (line.product_id.product_package_po or 1)) 
    
    #package_uom = fields.Many2one('product.packaging', help="Package ex:Dozen, Pack,")
    weight = fields.Float(compute='_get_weight', string='Unit Weight', default=0.0, digits=(16,2))#, digits=dp.get_precision('Stock Weight'))
    volume = fields.Float(compute='_get_weight', string='Unit Volume', default=0.0, digits=dp.get_precision('Volume'))
    tot_weight = fields.Float(compute='_compute_weight', string='Tot. Weight', default=0.0, digits=(16,2))#, digits=dp.get_precision('Stock Weight'))
    tot_volume = fields.Float(compute='_compute_weight', string='Tot. Volume', default=0.0, digits=dp.get_precision('Volume'))
