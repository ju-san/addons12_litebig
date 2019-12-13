# -*- coding: utf-8 -*-
# Part of Odoo. See ICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round, float_compare


class SplitPickingLine(models.TransientModel):
    _name = "stock.split.picking.line"
    _rec_name = 'product_id'
    _description = 'Return Picking Line'

    product_id = fields.Many2one('product.product', string="Product", required=True, domain="[('id', '=', product_id)]")
    quantity = fields.Float("Quantity", digits=dp.get_precision('Product Unit of Measure'), required=True)
    #location_dest_id = fields.Many2one('stock.location', string='Dest. Location')
    #picking_type_id = fields.Many2one('stock.picking.type', string='Picking Type')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='move_id.product_uom', readonly=False)
    wizard_id = fields.Many2one('stock.split.picking', string="Wizard")
    move_id = fields.Many2one('stock.move', "Move")


class SplitPicking(models.TransientModel):
    _name = 'stock.split.picking'
    _description = 'Split Picking'

    picking_id = fields.Many2one('stock.picking')
    product_split_moves = fields.One2many('stock.split.picking.line', 'wizard_id', 'Moves')
    move_dest_exists = fields.Boolean('Chained Move Exists', readonly=True)
    original_location_id = fields.Many2one('stock.location')
    parent_location_id = fields.Many2one('stock.location')
    location_id = fields.Many2one('stock.location', 'Split Location', domain="[('split_location', '=', True)]")
    #picking_type_id = fields.Many2one('stock.picking.type', string='Operation Type')
     
    @api.model
    def default_get(self, fields):
        if len(self.env.context.get('active_ids', list())) > 1:
            raise UserError(_("You may only return one picking at a time."))
        res = super(SplitPicking, self).default_get(fields)

        move_dest_exists = False
        product_split_moves = []
        picking = self.env['stock.picking'].browse(self.env.context.get('active_id'))
        if picking:
            res.update({'picking_id': picking.id})
            if picking.state == 'done':
                raise UserError(_("You may only split undone pickings."))
            for move in picking.move_lines:
                if move.scrapped:
                    continue
                if move.move_dest_ids:
                    move_dest_exists = True
                quantity = move.product_qty - sum(move.move_dest_ids.filtered(lambda m: m.state in ['partially_available', 'assigned', 'done']).\
                                                  mapped('move_line_ids').mapped('product_qty'))
                quantity = float_round(quantity, precision_rounding=move.product_uom.rounding)
                product_split_moves.append((0, 0, {'product_id': move.product_id.id, 
                                                   'quantity': quantity, 
                                                   'move_id': move.id, 
                                                   'uom_id': move.product_id.uom_id.id, 
                                                   #'location_dest_id': move.location_dest_id.id,
                                                   #'picking_type_id': move.picking_type_id.id if move.location_dest_id.usage == 'internal' else picking.picking_type_id.id
                                                   }))

            if not product_split_moves:
                raise UserError(_("No products to return (only lines in Done state and not fully returned yet can be returned)."))
            if 'product_split_moves' in fields:
                res.update({'product_split_moves': product_split_moves})
            if 'move_dest_exists' in fields:
                res.update({'move_dest_exists': move_dest_exists})
            if 'parent_location_id' in fields and picking.location_id.usage == 'internal':
                res.update({'parent_location_id': picking.picking_type_id.warehouse_id and picking.picking_type_id.warehouse_id.view_location_id.id or picking.location_id.location_id.id})
            if 'original_location_id' in fields:
                res.update({'original_location_id': picking.location_id.id})
#             if 'location_id' in fields:
#                 location_id = picking.location_id.id
#                 if picking.picking_type_id.return_picking_type_id.default_location_dest_id.return_location:
#                     location_id = picking.picking_type_id.return_picking_type_id.default_location_dest_id.id
#                 res['location_id'] = location_id
        return res

#     def _prepare_move_default_values(self, split_line, new_picking):
#         vals = {
#             'product_id': split_line.product_id.id,
#             'product_uom_qty': split_line.quantity,
#             'product_uom': split_line.product_id.uom_id.id,
#             'picking_id': new_picking.id,
#             'state': 'draft',
#             'date_expected': fields.Datetime.now(),
#             'location_id': split_line.move_id.location_id.id,
#             'location_dest_id': self.location_id.id,
#             'picking_type_id': new_picking.picking_type_id.id,
#             'warehouse_id': self.picking_id.picking_type_id.warehouse_id.id,
#             #'origin_returned_move_id': split_line.move_id.id,
#             'procure_method': 'make_to_stock',
#         }
#         return vals

    def _create_splits(self):
        # TODO sle: the unreserve of the next moves could be less brutal
        for return_move in self.product_split_moves.mapped('move_id'):
            return_move.move_dest_ids.filtered(lambda m: m.state not in ('done', 'cancel'))._do_unreserve()

        # create new picking for returned products
        self.picking_id.do_unreserve()
        returned_lines = 0
        new_moves = self.env['stock.move']
        for split_line in self.product_split_moves:
            if not split_line.move_id:
                raise UserError(_("You have manually created product lines, please delete them to proceed."))
            # TODO sle: float_is_zero?
            if split_line.quantity:
                returned_lines += 1
                #vals = self._prepare_move_default_values(split_line, new_picking)
                #print ('---vals---',vals)
                #r = split_line.move_id.copy(vals)
                #vals = {}

                # +--------------------------------------------------------------------------------------------------------+
                # |       picking_pick     <--Move Orig--    picking_pack     --Move Dest-->   picking_ship
                # |              | returned_move_ids              ↑                                  | returned_move_ids
                # |              ↓                                | split_line.move_id              ↓
                # |       return pick(Add as dest)          return toLink                    return ship(Add as orig)
                # +--------------------------------------------------------------------------------------------------------+
                #move_orig_to_link = split_line.move_id.move_dest_ids.mapped('returned_move_ids')
                #move_dest_to_link = split_line.move_id.move_orig_ids.mapped('returned_move_ids')
                #vals['move_orig_ids'] = [(4, m.id) for m in move_orig_to_link | split_line.move_id]
                #vals['move_dest_ids'] = [(4, m.id) for m in move_dest_to_link]
                rounding = split_line.move_id.product_uom.rounding
                qty_to_split = split_line.quantity
                qty_initial = split_line.move_id.product_uom_qty
                qty_diff_compare = float_compare(
                    qty_to_split, qty_initial, precision_rounding=rounding
                )
                if qty_diff_compare < 0:
                    qty_split = qty_initial - qty_to_split
                    qty_uom_split = split_line.move_id.product_uom._compute_quantity(
                        qty_to_split,
                        split_line.move_id.product_id.uom_id,
                        rounding_method='HALF-UP'
                    )
                    #print ('==qty_to_split==',split_line.move_id.origin)
                    new_move_id = split_line.move_id._split(qty_uom_split)
                    for move_line in split_line.move_id.move_line_ids:
                        if move_line.product_qty and move_line.qty_done:
                            # To avoid an error
                            # when picking is partially available
                            try:
                                move_line.write({'product_uom_qty': qty_split})
                            except UserError:
                                pass
                    new_moves |= self.env['stock.move'].browse(new_move_id)
                #r.write(vals)
        #print ('---new_moves--',new_moves)
        if not returned_lines:
            raise UserError(_("Please specify at least one non-zero quantity."))
        picking_type_id = self.picking_id.picking_type_id.id        
        if new_moves:
            picking = self.env['stock.picking'].create({
                'move_lines': [],
                'picking_type_id': picking_type_id,
                'state': 'draft',
                'origin': _("%s") % self.picking_id.name,
                'partner_id': self.picking_id.partner_id and self.picking_id.partner_id.id,
                'location_id': self.picking_id.location_id.id,
                'location_dest_id': self.location_id.id,
                'show_mark_as_todo': True
                })
            picking.message_post_with_view('mail.message_origin_link',
                values={'self': picking, 'origin': self.picking_id},
                subtype_id=self.env.ref('mail.mt_note').id)
            new_moves.write({'state': 'draft', 'picking_id': picking.id, 'location_dest_id': self.location_id.id, 'backorder_id': self.picking_id.id})
            #print ('==picking=new=3',picking.state,picking.origin,picking.name,self.picking_id.name)
            picking.action_confirm()
            picking.action_assign()
        else:
            picking = self.picking_id
            #print ('==picking=curr=',picking)
            picking.write({'location_dest_id': self.location_id.id})
            picking.mapped('move_lines').write({'location_dest_id': self.location_id.id})
        return picking.id, picking_type_id

    def create_splits(self):
        for wizard in self:
            new_picking_id, pick_type_id = wizard._create_splits()
        # Override the context to disable all the potential filters that could have been set previously
        ctx = dict(self.env.context)
        ctx.update({
            'search_default_picking_type_id': pick_type_id,
            'search_default_draft': False,
            'search_default_assigned': False,
            'search_default_confirmed': False,
            'search_default_ready': False,
            'search_default_late': False,
            'search_default_available': False,
        })
        return {
            'name': _('Allocation Picking'),
            'view_type': 'form',
            'view_mode': 'form,tree,calendar',
            'res_model': 'stock.picking',
            'res_id': new_picking_id,
            'type': 'ir.actions.act_window',
            'context': ctx,
        }
