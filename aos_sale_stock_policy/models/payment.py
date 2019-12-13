# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = "account.payment"
    
    def _prepare_account_move_line(self, line):
        data = super(AccountPayment, self)._prepare_account_move_line(line)
        data['sale_id'] = line.invoice_id and line.invoice_id.sale_id and line.invoice_id.sale_id.id or False
        return data 
    
    sale_ids = fields.Many2many('sale.order', string='Sale Order')
    
    @api.model
    def default_get(self, fields):
        rec = super(AccountPayment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            if 'sale_id' in invoice:
                sale_ids = invoice['sale_id'] and [invoice['sale_id'][0]]
                rec['sale_ids'] = sale_ids
        return rec
    
    @api.onchange('register_ids')
    def _onchange_register_ids(self):
        res = super(AccountPayment, self)._onchange_register_ids()
        sales = self.env['sale.order']
        for line in self.register_ids:
            if line.amount_to_pay:
                sales += line.sale_id
            elif not line.amount_to_pay:
                sales -= line.sale_id
        self.sale_ids = sales
        return res
    
    @api.multi
    def confirm(self):
        res = super(AccountPayment, self).confirm()
        for rec in self:
#             if not rec.sale_ids and not rec.register_ids and rec.invoice_ids and rec.invoice_ids.sale_id:
#                 rec.write({'sale_ids': [(4, [rec.invoice_ids.sale_id.id])]})
#             elif not rec.sale_ids and rec.register_ids and rec.register_ids.mapped('sale_id') and rec.invoice_ids: 
#                 rec.write({'sale_ids': [(4, filter(None, [payment.amount_to_pay and payment.sale_id.id for payment in rec.register_ids]))]})
            rec.state = 'confirm'
        return res
            
    #===========================================================================
    # CHANGE DEF FROM aos_account
    #===========================================================================
#     @api.multi
#     def post(self):
#         """ Create the journal items for the payment and update the payment's state to 'posted'.
#             A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
#             and another in the destination reconciliable account (see _compute_destination_account_id).
#             If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
#             If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
#         """
#         super(AccountPayment, self).post()
#         for rec in self:
#             if not rec.sale_ids and not rec.register_ids:
#                 rec.write({'sale_ids': [(4, [rec.invoice_ids.sale_id.id])]})
#             elif not rec.sale_ids and rec.register_ids:                
#                 rec.write({'sale_ids': [(4, [payment.sale_id.id for payment in rec.register_ids])]})
            
    #===========================================================================
    # CHANGE DEF FROM aos_account
    #===========================================================================
    @api.multi
    def post_multi(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconciliable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        super(AccountPayment, self).post_multi()
        for rec in self:
            if not rec.sale_ids and not rec.register_ids and rec.register_ids.mapped('sale_id') and rec.invoice_ids:
                rec.write({'sale_ids': [(4, [rec.invoice_ids.sale_id.id])]})
            elif not rec.sale_ids and rec.register_ids and rec.register_ids.mapped('sale_id') and rec.invoice_ids:   
                rec.write({'sale_ids': [(4, [payment.sale_id and payment.sale_id.id for payment in rec.register_ids])]})
            

# class AccountPaymentLine(models.Model):
#     _inherit = 'account.payment.line'
#     
#     sale_id = fields.Many2one('sale.order', string='Sale Order')


class account_register_payments(models.TransientModel):
    _inherit = "account.register.payments"
    
    def get_payment_line_vals(self, payment, line):
        #print ('==aos_sale=get_payment_line_vals')
        vals = super(account_register_payments, self).get_payment_line_vals(payment, line)
        vals['sale_id'] = line.invoice_id and line.invoice_id.sale_id and line.invoice_id.sale_id.id or False
        return vals
    
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#     
#     @api.multi
#     def _action_launch_stock_rule(self):
#         """
#         Launch procurement group run method with required/custom fields genrated by a
#         sale order line. procurement group will launch '_run_pull', '_run_buy' or '_run_manufacture'
#         depending on the sale order line product rule.
#         """
#         precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
#         errors = []
#         if self._context.get('create_picking') == 'from_invoice':
#             for line in self:
#                 if line.state != 'sale' or not line.product_id.type in ('consu','product'):
#                     continue
#                 qty = line._get_qty_procurement()
#                 if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
#                     continue
#      
#                 group_id = line.order_id.procurement_group_id
#                 if not group_id:
#                     group_id = self.env['procurement.group'].create({
#                         'name': line.order_id.name, 'move_type': line.order_id.picking_policy,
#                         'sale_id': line.order_id.id,
#                         'partner_id': line.order_id.partner_shipping_id.id,
#                     })
#                     line.order_id.procurement_group_id = group_id
#                 else:
#                     # In case the procurement group is already created and the order was
#                     # cancelled, we need to update certain values of the group.
#                     updated_vals = {}
#                     if group_id.partner_id != line.order_id.partner_shipping_id:
#                         updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
#                     if group_id.move_type != line.order_id.picking_policy:
#                         updated_vals.update({'move_type': line.order_id.picking_policy})
#                     if updated_vals:
#                         group_id.write(updated_vals)
#      
#                 values = line._prepare_procurement_values(group_id=group_id)
#                 product_qty = line.product_uom_qty - qty
#      
#                 procurement_uom = line.product_uom
#                 quant_uom = line.product_id.uom_id
#                 get_param = self.env['ir.config_parameter'].sudo().get_param
#                 if procurement_uom.id != quant_uom.id and get_param('stock.propagate_uom') != '1':
#                     product_qty = line.product_uom._compute_quantity(product_qty, quant_uom, rounding_method='HALF-UP')
#                     procurement_uom = quant_uom
#      
#                 try:
#                     self.env['procurement.group'].run(line.product_id, product_qty, procurement_uom, line.order_id.partner_shipping_id.property_stock_customer, line.name, line.order_id.name, values)
#                 except UserError as error:
#                     errors.append(error.name)
#             if errors:
#                 raise UserError('\n'.join(errors))
#         return True
#     
# class InvoiceStockMove(models.Model):
#     _inherit = 'account.invoice'

#     @api.model
#     def _default_picking_receive(self):
#         type_obj = self.env['stock.picking.type']
#         company_id = self.env.context.get('company_id') or self.env.user.company_id.id
#         types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)], limit=1)
#         if not types:
#             types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
#         return types[:1]
# 
#     @api.model
#     def _default_picking_transfer(self):
#         type_obj = self.env['stock.picking.type']
#         company_id = self.env.context.get('company_id') or self.env.user.company_id.id
#         types = type_obj.search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)], limit=1)
#         if not types:
#             types = type_obj.search([('code', '=', 'outgoing'), ('warehouse_id', '=', False)])
#         return types[:4]
# 
#     picking_count = fields.Integer(string="Count")
#     invoice_picking_id = fields.Many2one('stock.picking', string="Picking")
#     picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type', required=True,
#                                       default=_default_picking_receive,
#                                       help="This will determine picking type of incoming shipment")
#     picking_transfer_id = fields.Many2one('stock.picking.type', 'Deliver To', required=True,
#                                           default=_default_picking_transfer,
#                                           help="This will determine picking type of outgoing shipment")
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('proforma', 'Pro-forma'),
#         ('proforma2', 'Pro-forma'),
#         ('open', 'Open'),
#         ('paid', 'Paid'),
#         ('cancel', 'Cancelled'),
#         ('done', 'Received'),
#     ], string='Status', index=True, readonly=True, default='draft',
#         track_visibility='onchange', copy=False)
# 
#     @api.multi
#     def action_stock_receive(self):
#         for order in self:
#             if not order.invoice_line_ids:
#                 raise UserError(_('Please create some invoice lines.'))
#             if not self.number:
#                 raise UserError(_('Please Validate invoice.'))
#             if not self.invoice_picking_id:
#                 pick = {
#                     'picking_type_id': self.picking_type_id.id,
#                     'partner_id': self.partner_id.id,
#                     'origin': self.number,
#                     'location_dest_id': self.picking_type_id.default_location_dest_id.id,
#                     'location_id': self.partner_id.property_stock_supplier.id
#                 }
#                 picking = self.env['stock.picking'].create(pick)
#                 self.invoice_picking_id = picking.id
#                 self.picking_count = len(picking)
#                 moves = order.invoice_line_ids.filtered(lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves(picking)
#                 move_ids = moves._action_confirm()
#                 move_ids._action_assign()

#     @api.multi
#     def action_stock_transfer(self):
#         for invoice in self:
#             if not invoice.invoice_line_ids:
#                 raise UserError(_('Please create some invoice lines.'))
#             if not self.number:
#                 raise UserError(_('Please Validate invoice.'))
#             if not self.invoice_picking_id:
#                 invoice.invoice_line_ids.mapped('sale_line_ids').with_context(create_picking='from_invoice')._action_launch_stock_rule()
#                 pick = {
#                     'picking_type_id': self.picking_transfer_id.id,
#                     'partner_id': self.partner_id.id,
#                     'origin': self.number,
#                     'location_dest_id': self.partner_id.property_stock_customer.id,
#                     'location_id': self.picking_transfer_id.default_location_src_id.id
#                 }
#                 picking = self.env['stock.picking'].create(pick)
#                 self.invoice_picking_id = picking.id
#                 self.picking_count = len(picking)
#                 #print ('--s--',order.invoice_line_ids.mapped('sale_line_ids'))
#                 if len(order.invoice_line_ids.mapped('sale_line_ids')) > 1:
#                     sale_id = order.invoice_line_ids.mapped('sale_line_ids').order_id.id
#                 elif len(order.invoice_line_ids.mapped('sale_line_ids')) == 1:
#                     sale_id = order.invoice_line_ids.mapped('sale_line_ids')[0].order_id.id
#                 #print ('---sale_id---',sale_id,picking)
#                 #picking.write({'sale_id': sale_id})
#                 moves = order.invoice_line_ids.filtered(lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves_transfer(picking)
#                 move_ids = moves._action_confirm()
#                 move_ids._action_assign()

#     @api.multi
#     def action_view_picking(self):
#         action = self.env.ref('stock.action_picking_tree_ready')
#         result = action.read()[0]
#         result.pop('id', None)
#         result['context'] = {}
#         result['domain'] = [('id', '=', self.invoice_picking_id.id)]
#         pick_ids = sum([self.invoice_picking_id.id])
#         if pick_ids:
#             res = self.env.ref('stock.view_picking_form', False)
#             result['views'] = [(res and res.id or False, 'form')]
#             result['res_id'] = pick_ids or False
#         return result


# class SupplierInvoiceLine(models.Model):
#     _inherit = 'account.invoice.line'
# 
#     @api.multi
#     def _create_stock_moves(self, picking):
#         moves = self.env['stock.move']
#         done = self.env['stock.move'].browse()
#         for line in self:
#             price_unit = line.price_unit
#             template = {
#                 'name': line.name or '',
#                 'product_id': line.product_id.id,
#                 'product_uom': line.uom_id.id,
#                 'location_id': line.invoice_id.partner_id.property_stock_supplier.id,
#                 'location_dest_id': picking.picking_type_id.default_location_dest_id.id,
#                 'picking_id': picking.id,
#                 'move_dest_id': False,
#                 'state': 'draft',
#                 'company_id': line.invoice_id.company_id.id,
#                 'price_unit': price_unit,
#                 'picking_type_id': picking.picking_type_id.id,
#                 'procurement_id': False,
#                 'route_ids': 1 and [
#                     (6, 0, [x.id for x in self.env['stock.location.route'].search([('id', 'in', (2, 3))])])] or [],
#                 'warehouse_id': picking.picking_type_id.warehouse_id.id,
#             }
#             diff_quantity = line.quantity
#             tmp = template.copy()
#             tmp.update({
#                 'product_uom_qty': diff_quantity,
#             })
#             template['product_uom_qty'] = diff_quantity
#             done += moves.create(template)
#         return done
# 
#     def _create_stock_moves_transfer(self, picking):
#         moves = self.env['stock.move']
#         done = self.env['stock.move'].browse()
#         for line in self:
#             price_unit = line.price_unit
#             template = {
#                 'name': line.name or '',
#                 'product_id': line.product_id.id,
#                 'product_uom': line.uom_id.id,
#                 'location_id': picking.picking_type_id.default_location_src_id.id,
#                 'location_dest_id': line.invoice_id.partner_id.property_stock_customer.id,
#                 'picking_id': picking.id,
#                 'move_dest_id': False,
#                 'state': 'draft',
#                 'company_id': line.invoice_id.company_id.id,
#                 'price_unit': price_unit,
#                 'picking_type_id': picking.picking_type_id.id,
#                 'procurement_id': False,
#                 'route_ids': 1 and [
#                     (6, 0, [x.id for x in self.env['stock.location.route'].search([('id', 'in', (2, 3))])])] or [],
#                 'warehouse_id': picking.picking_type_id.warehouse_id.id,
#             }
#             diff_quantity = line.quantity
#             tmp = template.copy()
#             tmp.update({
#                 'product_uom_qty': diff_quantity,
#             })
#             template['product_uom_qty'] = diff_quantity
#             done += moves.create(template)
#         return done



