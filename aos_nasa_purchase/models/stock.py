# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from datetime import datetime 
from odoo.tools.misc import formatLang, format_date

# class StockPickingType(models.Model): 
#     _inherit = 'stock.picking.type'
#     
#     fold = fields.Boolean(string='Folded in Kanban',
#         help='This stage is folded in the kanban view when there are no records in that stage to display.')

class StockPicking(models.Model): 
    _inherit = 'stock.picking'
    
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the picking without removing it.") 
    is_return = fields.Boolean('Is Return')
    #show_range_qty = fields.Boolean('Show Range Qty', default=True)
    
            
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    
    @api.depends('location_id', 'location_dest_id', 'partner_id', 'state')
    def _compute_display_location(self):
        for mline in self:
            if mline.partner_id and mline.location_id.usage in ('customer','supplier'):
                mline.display_location_id = mline.partner_id.name
            else:
                mline.display_location_id = mline.location_id.display_name
            if mline.partner_id and mline.location_dest_id.usage in ('customer','supplier'):
                mline.display_location_dest_id = mline.partner_id.name
            else:
                mline.display_location_dest_id = mline.location_dest_id.display_name
            mline.group_id = mline.picking_id and mline.picking_id.group_id and mline.picking_id.group_id.name \
                or mline.picking_id and mline.picking_id.origin or ''
            #mline.display_location_dest_id = mline.partner_id and mline.partner_id.name if mline.location_dest_id.usage in ('customer','supplier') else mline.location_dest_id.display_name
        
    location_id = fields.Many2one('stock.location', 'Source', required=True)
    location_dest_id = fields.Many2one('stock.location', 'Destination', required=True)    
    display_location_id = fields.Char('From', compute='_compute_display_location', store=False)
    display_location_dest_id = fields.Char('To', compute='_compute_display_location', store=False)
    group_id = fields.Char('Reference SO/PO', compute='_compute_display_location', store=False)
    #reference = fields.Char(string='Reference Warehouse', related='move_id.reference', store=True, related_sudo=False, readonly=False)
    
    
class StockProductionLotGroup(models.Model):
    _name = 'stock.production.lot.group'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'SN Group'
    
    name = fields.Char(
        'Group Lot/Serial Number', default=lambda self: self.env['ir.sequence'].next_by_code('stock.lot.group.serial'),
        required=True, help="Group Unique Lot/Serial Number")
    ref = fields.Char('Internal Reference', help="Internal reference number in case it differs from the manufacturer's lot/serial number")
    lot_ids = fields.One2many('stock.production.lot', 'group_id', 'Lots', readonly=True)
    
    _sql_constraints = [
        ('name_ref_uniq', 'unique (name)', 'The group of serial number must be unique !'),
    ]
class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    group_id = fields.Many2one('stock.production.lot.group', string='Group SN')