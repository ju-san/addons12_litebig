# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.depends('state', 'order_line.invoice_status', 'order_line.invoice_lines', 'invoice_ids.state')
    def _get_payment(self):
        for order in self:
            payment_ids = self.env['account.payment'].sudo().search([('payment_type','in',('inbound','outbound')),('sale_ids','=',order.id)])
                
            line_invoice_status = order.invoice_ids.filtered(lambda i: i.state in ('draft','open','paid'))
            #print ('====line_invoice_status===',line_invoice_status)
            if order.state not in ('sale', 'done'):
                payment_status = 'no'
            elif all(invoice_status.state != 'paid' for invoice_status in line_invoice_status):
                payment_status = 'unpaid'
            elif all(invoice_status.state == 'paid' for invoice_status in line_invoice_status):
                payment_status = 'paid'
            elif any(invoice_status.state == 'paid' for invoice_status in line_invoice_status):
                payment_status = 'partial_paid'
            else:
                payment_status = 'no'
            order.update({
                'payment_count': len(set(payment_ids.ids)),
                'payment_ids': payment_ids.ids,
                'payment_status': payment_status,
            })
    
    payment_count = fields.Integer(string='# of Payment', compute='_get_payment', readonly=True)
    payment_ids = fields.Many2many("account.payment", string='Payments', compute="_get_payment", readonly=True, store=True, copy=False)
    
    payment_status = fields.Selection([
        ('no', 'Nothing to be Paid'),
        ('partial_paid', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('unpaid', 'Order Unpaid')
        ], string='Payment Status', compute='_get_payment', store=True, readonly=True)
    
    invoice_policy = fields.Selection([
        ('order', 'Ordered quantities'),
        ('delivery', 'Delivered quantities')], string='Invoicing Policy',
        help='Ordered Quantity: Invoice quantities ordered by the customer.\n'
             'Delivered Quantity: Invoice quantities delivered to the customer.',
        default='order')
    order_policy = fields.Selection([
            ('prepaid', 'Fully Payment Before Delivery'),
            ('manual', 'Shipping & Manual Invoice'),
            #('postpaid', 'Invoice On Order After Delivery'),
            ('picking', 'Invoice From The Picking'),
        ], 'Order Policy', default='manual', required=True, readonly=True, states={'draft': [('readonly', False)]},
                    help="""The Shipping Policy is used to synchronise invoice and delivery operations.
      - The 'Pay Before delivery' choice will first generate the invoice and then generate the picking order after the payment of this invoice.
      - The 'Shipping & Manual Invoice' will create the picking order directly and wait for the user to manually click on the 'Invoice' button to generate the draft invoice.
      - The 'Invoice From The Picking' choice is used to create an invoice during the picking process.""")
    

    def _finalize_invoices(self, invoices, references):
        """
        Invoked after creating invoices at the end of action_invoice_create.
        :param invoices: {group_key: invoice}
        :param references: {invoice: order}
        """
        for invoice in invoices.values():
            invoice.compute_taxes()
            if not invoice.invoice_line_ids:
                raise UserError(_(
                    'There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))
            # If invoice is negative, do a refund invoice instead
            if invoice.amount_total < 0:
                invoice.type = 'out_refund'
                for line in invoice.invoice_line_ids:
                    line.quantity = -line.quantity
            # Use additional field helper function (for account extensions)
            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            # Necessary to force computation of taxes. In account_invoice, they are triggered
            # by onchanges, which are not triggered when doing a create.
            invoice.compute_taxes()
            # Idem for partner
            so_payment_term_id = invoice.payment_term_id.id
            invoice._onchange_partner_id()
            # To keep the payment terms set on the SO
            invoice.payment_term_id = so_payment_term_id
            invoice.message_post_with_view('mail.message_origin_link',
                values={'self': invoice, 'origin': references[invoice]},
                subtype_id=self.env.ref('mail.mt_note').id)
            
    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        references = {}
        invoices_origin = {}
        invoices_name = {}
 
        # Keep track of the sequences of the lines
        # To keep lines under their section
        inv_line_sequence = 0
        for order in self:
            group_key = order.id if grouped else (order.partner_invoice_id.id, order.currency_id.id)
            if order.invoice_policy == 'order':
                inv_data = order._prepare_invoice()
                invoice = inv_obj.create(inv_data)
                references[invoice] = order
                invoices[group_key] = invoice
                invoices_origin[group_key] = [invoice.origin]
                invoices_name[group_key] = [invoice.name]
                for inv_line in order.order_line:
                    inv_line.invoice_line_create(invoice.id, inv_line.product_uom_qty)
            else:
                 
                # We only want to create sections that have at least one invoiceable line
                pending_section = None
     
                # Create lines in batch to avoid performance problems
                line_vals_list = []
                # sequence is the natural order of order_lines
                for line in order.order_line:
                    if line.display_type == 'line_section':
                        pending_section = line
                        continue
                    if float_is_zero(line.qty_to_invoice, precision_digits=precision):
                        continue
                    if group_key not in invoices:
                        inv_data = order._prepare_invoice()
                        invoice = inv_obj.create(inv_data)
                        references[invoice] = order
                        invoices[group_key] = invoice
                        invoices_origin[group_key] = [invoice.origin]
                        invoices_name[group_key] = [invoice.name]
                    elif group_key in invoices:
                        if order.name not in invoices_origin[group_key]:
                            invoices_origin[group_key].append(order.name)
                        if order.client_order_ref and order.client_order_ref not in invoices_name[group_key]:
                            invoices_name[group_key].append(order.client_order_ref)
     
                    if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final):
                        if pending_section:
                            section_invoice = pending_section.invoice_line_create_vals(
                                invoices[group_key].id,
                                pending_section.qty_to_invoice
                            )
                            inv_line_sequence += 1
                            section_invoice[0]['sequence'] = inv_line_sequence
                            line_vals_list.extend(section_invoice)
                            pending_section = None
     
                        inv_line_sequence += 1
                        inv_line = line.invoice_line_create_vals(
                            invoices[group_key].id, line.qty_to_invoice
                        )
                        inv_line[0]['sequence'] = inv_line_sequence
                        line_vals_list.extend(inv_line)
     
                if references.get(invoices.get(group_key)):
                    if order not in references[invoices[group_key]]:
                        references[invoices[group_key]] |= order
     
                self.env['account.invoice.line'].create(line_vals_list)
        #print ('-invoices--',invoices)
        for group_key in invoices:
            invoices[group_key].write({'name': ', '.join(invoices_name[group_key]),
                                       'origin': ', '.join(invoices_origin[group_key])})
            sale_orders = references[invoices[group_key]]
            if len(sale_orders) == 1:
                invoices[group_key].reference = sale_orders.reference
 
        if not invoices:
            raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))
 
        self._finalize_invoices(invoices, references)
        return [inv.id for inv in invoices.values()]
    
    @api.multi
    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        for order in self:
            if order.picking_ids: 
                for picking in self.picking_ids:
                    picking.write({'is_locked': False})
            if order.order_policy == 'prepaid' and not order.invoice_ids:
                order.action_invoice_create()  
            if order.order_policy == 'prepaid' and order.invoice_ids:
                for invoice in order.invoice_ids:
                    invoice.action_invoice_open()
        return res  
        
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
     
    @api.depends('qty_invoiced', 'qty_delivered', 'product_uom_qty', 'order_id.state', 'order_id.invoice_policy')
    def _get_to_invoice_qty(self):
        """
        Compute the quantity to invoice. If the invoice policy is order, the quantity to invoice is
        calculated from the ordered quantity. Otherwise, the quantity delivered is used.
        """
        
        for line in self:
            if line.order_id.state in ['sale', 'done']:
                if line.product_id.type == 'service':
                    invoice_policy = line.product_id.invoice_policy
                else:
                    invoice_policy = line.order_id.invoice_policy or line.product_id.invoice_policy
                if invoice_policy == 'order':
                    line.qty_to_invoice = line.product_uom_qty - line.qty_invoiced
                else:
                    line.qty_to_invoice = line.qty_delivered - line.qty_invoiced
            else:
                line.qty_to_invoice = 0