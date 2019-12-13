# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from datetime import datetime 
from odoo.tools.misc import formatLang, format_date


class AccountJournal(models.Model):
    ''' Defining a student information '''
    _inherit = "account.journal"

    type = fields.Selection(selection_add=[('nonbank', 'Non Bank/Non Cash')])
    
    
class AccountInvoice(models.Model): 
    _inherit = 'account.invoice'
    
    @api.one
    @api.depends('invoice_line_ids', 'invoice_line_ids.point_total')
    def _compute_point(self):
        self.point_amount_total = sum([line.point_total for line in self.invoice_line_ids])
    
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the sale order without removing it.") 
    partner_id = fields.Many2one('res.partner', string='Stockist/Stockist Center', change_default=True,
        readonly=True, states={'draft': [('readonly', False)]},
        track_visibility='always', ondelete='restrict', help="You can find a contact by its Name, TIN, Email or Internal Reference.")
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Alamat Pengiriman',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Delivery address for current invoice.")
    faktur_sementara = fields.Boolean('Faktur Sementara')
    partner_ref = fields.Char('Nama Stockist', related='partner_id.customer_ref')
    saldo_stockist = fields.Monetary(related='partner_id.saldo_stockist', string='Saldo Stockist')
    barang_dikirim = fields.Boolean('Barang Dikirim')
    barang_dikirim_kesub = fields.Boolean('Ke Sub')
    apakah_promo = fields.Boolean('Promo?')
    point_amount_total = fields.Monetary(string='Total BV', compute='_compute_point', store=True)
    
class AccountInvoiceLine(models.Model): 
    _inherit = 'account.invoice.line'
    
    poin_ok = fields.Boolean('P/N', related='product_id.poin_ok')
    point_total = fields.Float('Total BV')
            
            