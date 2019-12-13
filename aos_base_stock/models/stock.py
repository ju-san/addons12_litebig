# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    
    def _get_locations_values(self, vals):
        sub_locations = super(StockWarehouse, self)._get_locations_values(vals=vals)
        #CHANGE NAME STOCK INTO WAREHOUSE STOCK
        sub_locations.update({'lot_stock_id': {'name': vals.get('name')}})
        return sub_locations


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'
    
    def get_action_picking_tree_late(self):
        return self._get_action('stock.action_picking_tree_late')
        if self.code == 'incoming':
            action = self._get_action('aos_base_stock.action_picking_tree_late_in')
        elif self.code == 'outgoing':
            action = self._get_action('aos_base_stock.action_picking_tree_late_out')
        else:
            action = self._get_action('stock.action_picking_tree_late')
        return action

    def get_action_picking_tree_backorder(self):
        #return self._get_action('stock.action_picking_tree_backorder')
        if self.code == 'incoming':
            action = self._get_action('aos_base_stock.action_picking_tree_backorder_in')
        elif self.code == 'outgoing':
            action = self._get_action('aos_base_stock.action_picking_tree_backorder_out')
        else:
            action = self._get_action('stock.action_picking_tree_backorder')
        return action

    def get_action_picking_tree_waiting(self):
        #return self._get_action('stock.action_picking_tree_waiting')
        if self.code == 'incoming':
            action = self._get_action('aos_base_stock.action_picking_tree_waiting_in')
        elif self.code == 'outgoing':
            action = self._get_action('aos_base_stock.action_picking_tree_waiting_out')
        else:
            action = self._get_action('stock.action_picking_tree_waiting')
        return action

    def get_action_picking_tree_ready(self):
        #print ('=get_action_picking_tree_ready===',self.code)
        #return self._get_action('stock.action_picking_tree_ready')
        if self.code == 'incoming':
            action = self._get_action('aos_base_stock.action_picking_tree_ready_in')
        elif self.code == 'outgoing':
            action = self._get_action('aos_base_stock.action_picking_tree_ready_out')
        else:
            action = self._get_action('stock.action_picking_tree_ready')
        return action
    
    def get_stock_picking_action_picking_type(self):
        if self.code == 'incoming':
            action = self._get_action('aos_base_stock.stock_picking_action_picking_type_in')
        elif self.code == 'outgoing':
            action = self._get_action('aos_base_stock.stock_picking_action_picking_type_out')
        else:
            action = self._get_action('stock.stock_picking_action_picking_type')
        return action
    
    split_assign_picking = fields.Boolean('Split Picking', help='Always check for create split picking for every rules')
    
    
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    picking_ref = fields.Char('Shipping Attachment')
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type')
    
    @api.onchange('location_id', 'location_dest_id')
    def onchange_location_src_dest_id(self):
        #move_lines
        if self.location_id:
            for mline in self.move_ids_without_package:
                mline.location_id = self.location_id.id
            for iline in self.move_line_ids_without_package:
                mline.location_id = self.location_id.id
        if self.location_dest_id:
            for mline in self.move_ids_without_package:
                mline.location_dest_id = self.location_dest_id.id
            for iline in self.move_line_ids_without_package:
                iline.location_dest_id = self.location_dest_id.id
    
class stock_move(models.Model):
    _inherit = 'stock.move'
    
    def _search_picking_for_assignation(self):
        self.ensure_one()
        #print ('==_search_picking_for_assignation==',self.origin)
        domain = [('group_id', '=', self.group_id.id),
                    ('location_id', '=', self.location_id.id),
                    ('location_dest_id', '=', self.location_dest_id.id),
                    ('picking_type_id', '=', self.picking_type_id.id),
                    ('printed', '=', False),
                    ('state', 'in', ['draft', 'confirmed', 'waiting', 'partially_available', 'assigned'])]
        if self.picking_type_id.split_assign_picking:
            domain += [('origin','=',self.origin)]
        return self.env['stock.picking'].search(domain, limit=1)
                