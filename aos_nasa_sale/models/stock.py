# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.depends('sale_id', 'sale_id.payment_status', 'sale_id.faktur_sementara')
    def _get_payment_status(self):
        for picking in self:
            payment_status = picking.sale_id.payment_status
            if picking.sale_id.faktur_sementara or payment_status == 'paid':
                is_locked = True
            else:
                is_locked = False
            print ('===is_locked===',picking,is_locked,picking.sale_id.faktur_sementara)
            picking.update({
                'payment_status': payment_status,
                'is_locked': is_locked,
            })
             
    payment_status = fields.Selection([
        ('no', 'Nothing to be Paid'),
        ('partial_paid', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('unpaid', 'Order Unpaid')
        ], string='Payment Status', compute='_get_payment_status', store=True, readonly=True)
#     order_policy = fields.Selection([
#             ('prepaid', 'Fully Payment Before Delivery'),
#             ('manual', 'Shipping & Manual Invoice'),
#             #('postpaid', 'Invoice On Order After Delivery'),
#             ('picking', 'Invoice From The Picking'),
#         ], 'Order Policy', related='sale_id.order_policy', readonly=True, states={'draft': [('readonly', False)]},
#                     help="""The Shipping Policy is used to synchronise invoice and delivery operations.
#       - The 'Pay Before delivery' choice will first generate the invoice and then generate the picking order after the payment of this invoice.
#       - The 'Shipping & Manual Invoice' will create the picking order directly and wait for the user to manually click on the 'Invoice' button to generate the draft invoice.
#       - The 'Invoice On Order After Delivery' choice will generate the draft invoice based on sales order after all picking lists have been finished.
#       - The 'Invoice From The Picking' choice is used to create an invoice during the picking process.""")