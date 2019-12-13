# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare

import odoo.addons.decimal_precision as dp

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    show_wv = fields.Boolean(string='Show Weight/Volume')#, related='purchase_id.show_wv', store=True)
    
    def _prepare_invoice_line_from_po_line(self, line):
        vals = super(AccountInvoice, self)._prepare_invoice_line_from_po_line(line=line)
        vals['weight'] = line.weight
        vals['volume'] = line.volume
        #vals['tot_weight'] = line.shipping_weight or line.tot_weight
        vals['tot_weight'] = line.tot_weight
        vals['tot_volume'] = line.tot_volume
#         vals['discount'] = line.discount
#         vals['inland_unit'] = line.inland_unit
#         vals['inland_value'] = line.inland_value
        #print ("===_prepare_invoice_line_from_po_line==",vals)
        return vals
    
#     def _set_currency_rate(self):
#         for invoice in self:
#             company_currency = invoice.company_currency_id
#             invoice_currency = invoice.currency_id or company_currency
#             if invoice_currency != company_currency:
#                 invoice.force_rate = invoice_currency.with_context(partner_id=invoice.partner_id.id,date=invoice.date_invoice, force_rate=invoice.force_rate).compute(1.0, company_currency, round=False)
#             else:
#                 invoice.force_rate = 1.0
#                 
#     @api.onchange('currency_id')
#     def _onchange_currency_id(self):
#         if self.currency_id:
#             self._set_currency_rate()
#             for line in self.invoice_line_ids.filtered(lambda r: r.purchase_line_id):
#                 line.price_unit = line.purchase_id.currency_id.with_context(partner_id=self.partner_id.id,date=self.date_invoice, force_rate=self.force_rate).compute(line.purchase_line_id.price_unit, self.currency_id, round=False)
#                 #===============================================================
#                 # ADD THIS LINE TO UPDATE CURRENCY ON LANDED
#                 line.inland_unit = line.purchase_id.currency_id.with_context(partner_id=self.partner_id.id,date=self.date_invoice, force_rate=self.force_rate).compute(line.inland_value / (line.quantity or 1.0), self.currency_id, round=False)
#                 line.inland_value = line.purchase_id.currency_id.with_context(partner_id=self.partner_id.id,date=self.date_invoice, force_rate=self.force_rate).compute((line.tot_weight or 1.0 / (sum(li.tot_weight or 1.0 for li in self.invoice_line_ids) or 1.0)) * self.amount_inland, self.currency_id, round=False)
#                 #print "===_onchange_currency_id===",line.inland_unit,line.inland_value
#                 #===============================================================
#     
#     @api.onchange('partner_id', 'company_id')
#     def _onchange_partner_id(self):
#         res = super(AccountInvoice, self)._onchange_partner_id()
#         if self.purchase_id.currency_id:
#             self.currency_id = self.purchase_id.currency_id.id
#         return res
#     
# 
#     @api.onchange('branch_id')
#     def _onchange_allowed_purchase_ids(self):
#         ''' Show only the purchase orders that have the same branch'''
#         result = super(AccountInvoice, self)._onchange_allowed_purchase_ids()
#         result['domain']['purchase_id'] += [('branch_id', '=', self.branch_id.id)]
#         return result
#     
#     # Load all unsold PO lines
#     @api.onchange('purchase_id')
#     def purchase_order_change(self):
#         if not self.purchase_id:
#             return {}
#         if not self.partner_id:
#             self.partner_id = self.purchase_id.partner_id.id
#         #=======================================================================
#         # THIS WILL DELETE INVOICE LINES
#         self.invoice_line_ids = []
#         #=======================================================================
#         new_lines = self.env['account.invoice.line']
#         for line in self.purchase_id.order_line - self.invoice_line_ids.mapped('purchase_line_id'):
#             data = self._prepare_invoice_line_from_po_line(line)
#             new_line = new_lines.new(data)
#             new_line._set_additional_fields(self)
#             new_lines += new_line
#  
#         self.invoice_line_ids += new_lines
#         self.currency_id = self.purchase_id.currency_id.id
#         self.amount_inland = self.purchase_id.amount_inland
#         #print "===amount_inland====",self.amount_inland
#         if self.purchase_id and self.purchase_id.branch_id:
#             # Assign OU from PO to Invoice
#             self.branch_id = self.purchase_id.branch_id.id
#         self.purchase_id = self.purchase_id.id
#         return {}
    
#     @api.multi
#     def compute_invoice_totals(self, company_currency, invoice_move_lines):
#         total = 0
#         total_currency = 0
#         for line in invoice_move_lines:
#             print "===compute_invoice_totals===",line
#             if self.currency_id != company_currency:
#                 currency = self.currency_id.with_context(date=self._get_currency_rate_date() or fields.Date.context_today(self))
#                 if not (line.get('currency_id') and line.get('amount_currency')):
#                     line['currency_id'] = currency.id
#                     line['amount_currency'] = currency.round(line['price'])
#                     line['price'] = currency.compute(line['price'], company_currency)
#             else:
#                 line['currency_id'] = False
#                 line['amount_currency'] = False
#                 line['price'] = self.currency_id.round(line['price'])
#             if self.type in ('out_invoice', 'in_refund'):
#                 total += line['price']
#                 total_currency += line['amount_currency'] or line['price']
#                 line['price'] = - line['price']
#             else:
#                 total -= line['price']
#                 total_currency -= line['amount_currency'] or line['price']
#         print "===compute_invoice_totals===",total, total_currency
#         return total, total_currency, invoice_move_lines
    #===========================================================================
    # change base invoice_line_move_line_get plus landed cost
    #===========================================================================
#     @api.model
#     def invoice_line_move_line_get(self):
#         res = []
#         for line in self.invoice_line_ids:
#             if line.quantity==0:
#                 continue
#             tax_ids = []
#             for tax in line.invoice_line_tax_ids:
#                 tax_ids.append((4, tax.id, None))
#                 for child in tax.children_tax_ids:
#                     if child.type_tax_use != 'none':
#                         tax_ids.append((4, child.id, None))
#             analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]
#             #print "==landed==",line.price_subtotal + line.inland_value
#             move_line_dict = {
#                 'invl_id': line.id,
#                 'type': 'src',
#                 'name': line.name.split('\n')[0][:64],
#                 'price_unit': line.price_unit,
#                 'quantity': line.quantity,
#                 'price': line.price_subtotal + line.inland_value,
#                 'account_id': line.account_id.id,
#                 'product_id': line.product_id.id,
#                 'uom_id': line.uom_id.id,
#                 'account_analytic_id': line.account_analytic_id.id,
#                 'tax_ids': tax_ids,
#                 'invoice_id': self.id,
#                 'analytic_tag_ids': analytic_tag_ids
#             }
#             res.append(move_line_dict)
#         return res
    
#     @api.multi
#     def compute_invoice_totals(self, company_currency, invoice_move_lines):
#         total = 0
#         total_currency = 0
#         for line in invoice_move_lines:
#             print "---line----",line['price'],line['account_id']
#             if self.currency_id != company_currency:
#                 currency = self.currency_id.with_context(date=self._get_currency_rate_date() or fields.Date.context_today(self))
#                 if not (line.get('currency_id') and line.get('amount_currency')):
#                     line['currency_id'] = currency.id
#                     line['amount_currency'] = currency.round(line['price'])
#                     line['price'] = currency.compute(line['price'], company_currency)
#             else:
#                 line['currency_id'] = False
#                 line['amount_currency'] = False
#                 line['price'] = self.currency_id.round(line['price'])
#             if self.type in ('out_invoice', 'in_refund'):
#                 total += line['price']
#                 total_currency += line['amount_currency'] or line['price']
#                 line['price'] = - line['price']
#             else:
#                 total -= line['price']
#                 total_currency -= line['amount_currency'] or line['price']
#         #print "====sssss=====",total, total_currency, invoice_move_lines
#         return total, total_currency, invoice_move_lines
    
#     @api.model
#     def invoice_line_move_line_get(self):
#         """Copy from invoice line to move lines"""
#         res = super(AccountInvoice, self).invoice_line_move_line_get()
#         ailo = self.env['account.invoice.line']
#         for move_line_dict in res:
#             if move_line_dict.get('invl_id'):
#                 iline = ailo.browse(move_line_dict['invl_id'])
#                 move_line_dict['price'] = iline.price_subtotal + iline.inland_value
#         return res
    #PRICE_SUBTOTAL + INLAND_VALUE
#     @api.model
#     def invoice_line_move_line_get(self):
#         res = super(AccountInvoice,self).invoice_line_move_line_get()    
#         invoice_line = self.env['account.invoice.line']
#         for line in res:
#             if line.get('invl_id'):
#                 iline = invoice_line.browse(line['invl_id'])
#                 line.update({'price': iline.price_subtotal + iline.inland_value})
#                 print "==invoice_line_move_line_get==",line,iline.price_subtotal + iline.inland_value
#         return res
    #===========================================================================
    # change base _anglo_saxon_purchase_move_lines property_account_creditor_price_difference into gain loss account get from journal
    #===========================================================================
#     @api.model
#     def _anglo_saxon_purchase_move_lines(self, i_line, res):
#         """Return the additional move lines for purchase invoices and refunds.
#         change
#         i_line: An account.invoice.line object.
#         res: The move line entries produced so far by the parent move_line_get.
#         'account_id': amount_diff > 0 and 
#         self.company_id.currency_exchange_journal_id.default_debit_account_id.id or 
#         self.company_id.currency_exchange_journal_id.default_credit_account_id.id,
#         """
#         inv = i_line.invoice_id
#         company_currency = inv.company_id.currency_id
#         if i_line.product_id and i_line.product_id.valuation == 'real_time' and i_line.product_id.type == 'product':
#             # get the fiscal position
#             fpos = i_line.invoice_id.fiscal_position_id
#             # get the price difference account at the product
#             #===================================================================
#             # USE THIS IF NOT MULTICURRENCY
#             #===================================================================
#             acc = i_line.product_id.property_account_creditor_price_difference
#             if not acc:
#                 # if not found on the product get the price difference account at the category
#                 acc = i_line.product_id.categ_id.property_account_creditor_price_difference_categ
#             acc = fpos.map_account(acc).id
#             #===================================================================
#             # reference_account_id is the stock input account
#             reference_account_id = i_line.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fpos)['stock_input'].id
#             diff_res = []
#             # CHANGE ROUNDING      
#             account_prec = 10#inv.company_id.currency_id.decimal_places
#             # calculate and write down the possible price difference between invoice price and product price
#             for line in res:
#                 if line.get('invl_id', 0) == i_line.id and reference_account_id == line['account_id']:
#                     #valuation_price_unit = i_line.product_id.uom_id._compute_price(i_line.product_id.standard_price, i_line.uom_id)
# #                     valuation_price_unit = company_currency.with_context(partner_id=inv.partner_id.id,date=inv.date_invoice, force_rate=inv.force_rate)._convert(
# #                         i_line.product_id.uom_id._compute_price(i_line.product_id.standard_price, i_line.uom_id),
# #                         inv.currency_id,
# #                         company=inv.company_id, partner=inv.partner_id, date=inv.date_invoice, round=False,
# #                     )
#                     #===========================================================
#                     # ONLY WHEN PURCHASE & INVOICE HAVE DIFFERENT PRICE
#                     #===========================================================
#                     if i_line.product_id.cost_method != 'standard' and i_line.purchase_line_id:
#                         #for average/fifo/lifo costing method, fetch real cost price from incomming moves
#                         valuation_price_unit = i_line.purchase_line_id.product_uom._compute_price(i_line.purchase_line_id.price_unit+i_line.inland_unit, i_line.uom_id)
#                         #print "===valuation_price_unit====",valuation_price_unit
#                         #=======================================================
#                         stock_move_obj = self.env['stock.move']
#                         valuation_stock_move = stock_move_obj.search([('purchase_line_id', '=', i_line.purchase_line_id.id), ('state', '=', 'done')])
#                         #print "===valuation_stock_move===",valuation_stock_move
#                         if valuation_stock_move:
#                             valuation_price_unit_total = 0
#                             valuation_total_qty = 0
#                             for val_stock_move in valuation_stock_move:
#                                 valuation_price_unit_total += (i_line.purchase_line_id.price_unit+i_line.inland_unit) * val_stock_move.product_qty
#                                 #val_move_line = val_stock_move.move_id and sum(val_stock_move.move_id.line_ids.mapped('debit')) or sum(val_stock_move.move_id.line_ids.mapped('credit'))
#                                 #valuation_price_unit_total += val_move_line# * val_stock_move.product_qty
#                                 valuation_total_qty += val_stock_move.product_qty
#                             valuation_price_unit = valuation_price_unit_total / valuation_total_qty
#                             valuation_price_unit = i_line.product_id.uom_id._compute_price(valuation_price_unit, i_line.uom_id)
#                             #print "===valuation_price_unit==",i_line.purchase_line_id.order_id.currency_id,company_currency,valuation_price_unit
#                             if i_line.purchase_line_id.order_id.currency_id != company_currency:
#                                 #=======================================================
#                                 # IF PO CURRENCY != INV CURRENCY (MAKE COMPUTE CURRENCY)
#                                 #=======================================================
#                                 valuation_price_unit = company_currency.with_context(partner_id=i_line.purchase_line_id.order_id.partner_id.id,date=inv.date_invoice, force_rate=inv.force_rate).compute(valuation_price_unit, i_line.purchase_line_id.order_id.currency_id, round=False)
#                         #print "===valuation_price_unit==",valuation_price_unit
#                         if inv.currency_id.id != company_currency.id:
#                             #=======================================================
#                             # IF INV CURRENCY != COMPANY CURRENCY (MAKE COMPUTE CURRENCY)
#                             #=======================================================
#                             valuation_price_unit = company_currency.with_context(partner_id=inv.partner_id.id,date=inv.date_invoice, force_rate=inv.force_rate).compute(valuation_price_unit, inv.currency_id, round=False)
#                             if not inv.company_id.currency_exchange_journal_id.default_debit_account_id and not inv.company_id.currency_exchange_journal_id.default_credit_account_id:
#                                 raise UserError(_('You should set account debit/credit exchange gain loss on journal (%s)' % inv.company_id.currency_exchange_journal_id.name))
#                         if valuation_price_unit != i_line.price_unit and line['price_unit'] == i_line.price_unit and acc:
#                             #print "---valuation_price_unit---",valuation_price_unit,i_line.price_unit,line['price_unit'],i_line.price_unit,acc,line
#                             # price with discount and without tax included
#                             price_unit = i_line.price_unit * (1 - (i_line.discount or 0.0) / 100.0)
#                             #price_unit = price_unit + i_line.inland_unit
#                             tax_ids = []
#                             if line['tax_ids']:
#                                 #line['tax_ids'] is like [(4, tax_id, None), (4, tax_id2, None)...]
#                                 taxes = self.env['account.tax'].browse([x[1] for x in line['tax_ids']])
#                                 price_unit = taxes.compute_all(price_unit, currency=inv.currency_id, quantity=1.0)['total_excluded']+i_line.inland_unit
#                                 for tax in taxes:
#                                     tax_ids.append((4, tax.id, None))
#                                     for child in tax.children_tax_ids:
#                                         if child.type_tax_use != 'none':
#                                             tax_ids.append((4, child.id, None))
#                             price_before = line.get('price', 0.0)+i_line.inland_value
#                             #print "===price_before===",line.get('price', 0.0),valuation_price_unit,i_line.inland_value
#                             line.update({'price': round(valuation_price_unit * line['quantity'], account_prec)})
#                             #print "===price_unit==",price_unit,valuation_price_unit,i_line.inland_unit
#                             #print "===price==",price_before,line.get('price', 0.0),valuation_price_unit * line['quantity']
#                             diff_res.append({
#                                 'type': 'src',
#                                 'name': i_line.name[:64],
#                                 'price_unit': round(price_unit - valuation_price_unit, account_prec),
#                                 'quantity': line['quantity'],
#                                 'price': round(price_before - line.get('price', 0.0), account_prec),
#                                 'account_id': inv.currency_id.id == company_currency.id and acc or round(price_before - line.get('price', 0.0), account_prec) > 0 and inv.company_id.currency_exchange_journal_id.default_debit_account_id.id or inv.company_id.currency_exchange_journal_id.default_credit_account_id.id,
#                                 'product_id': line['product_id'],
#                                 'uom_id': line['uom_id'],
#                                 'account_analytic_id': line['account_analytic_id'],
#                                 'tax_ids': tax_ids,
#                                 })
#                             #=======================================================
#                             # DO UPDATE STANDARD PRICE IF YOU REVISE THE PRICE
#                             #=======================================================
#                             if i_line.product_id.qty_available > 0:
#                                 standard_price = i_line.product_id.standard_price
#                                 qty_available = i_line.product_id.qty_available
#                                 valuation_current = standard_price * qty_available
#                                 #po line - inv line
#                                 valuation_diff = round(valuation_price_unit * line['quantity'], account_prec) - round(price_unit * line['quantity'], account_prec)
#                                 standard_price_update = (valuation_current-valuation_diff)/qty_available
#                                 #this is update revisi if you have difference price on po and inv per product
#                                 #i_line.product_id.write({'standard_price': standard_price_update})
#             return diff_res
#         return []
    
    #PRICE_SUBTOTAL + INLAND_VALUE
#     @api.model
#     def invoice_line_move_line_get(self):
#         res = super(AccountInvoice,self).invoice_line_move_line_get()    
#         invoice_line = self.env['account.invoice.line']
#         for line in res:
#             if line.get('invl_id'):
#                 iline = invoice_line.browse(line['invl_id'])
#                 line.update({'price': iline.price_subtotal + iline.inland_value})
#         return res

#         res = super(AccountInvoice, self).invoice_line_move_line_get()
#         ailo = self.env['account.invoice.line']
#         for move_line_dict in res:
#             print "----invoice_line_move_line_get----",move_line_dict.get('invl_id'),move_line_dict
#             if move_line_dict.get('invl_id'):
#                 iline = ailo.browse(move_line_dict['invl_id'])
#                 move_line_dict['price'] = iline.price_subtotal + iline.inland_value
#         return res
class AccountInvoiceLine(models.Model):
    """ Override AccountInvoice_line to add the link to the purchase order line it is related to"""
    _inherit = 'account.invoice.line'

    #purchase_line_id = fields.Many2one('purchase.order.line', 'Purchase Order Line', ondelete='set null', index=True, readonly=True, copy=False)
    weight = fields.Float('Unit Weight', default=1.0, digits=dp.get_precision('Stock Weight'))
    volume = fields.Float('Unit Volume', default=1.0)
    tot_weight = fields.Float('Tot. Weight', default=0.0, digits=dp.get_precision('Stock Weight'))
    tot_volume = fields.Float('Tot. Volume', default=0.0)