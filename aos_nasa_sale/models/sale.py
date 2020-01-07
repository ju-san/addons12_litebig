# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from datetime import datetime 
from odoo.tools.misc import formatLang, format_date

    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.multi
    def _debit_deposito_get(self):
        tables, where_clause, where_params = self.env['account.move.line'].with_context(state='posted', company_id=self.env.user.company_id.id)._query_get()
        where_params = [tuple(self.ids)] + where_params
        if where_clause:
            where_clause = 'AND ' + where_clause
        self._cr.execute("""SELECT account_move_line.partner_id, act.type, SUM(account_move_line.amount_residual)
                      FROM """ + tables + """
                      LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                      LEFT JOIN account_account_type act ON (a.user_type_id=act.id)
                      WHERE act.type IN ('receivable','payable')
                      AND account_move_line.partner_id IN %s
                      AND account_move_line.reconciled IS FALSE
                      """ + where_clause + """
                      GROUP BY account_move_line.partner_id, act.type
                      """, where_params)
        for pid, type, val in self._cr.fetchall():
            partner = self.browse(pid)
            if type == 'receivable':
                partner.debit = val
    @api.model
    def _debit_search(self, operator, operand):
        return self._asset_difference_search('receivable', operator, operand)
    
    saldo_stockist = fields.Monetary(compute='_debit_deposito_get', search=_debit_search, string='Saldo Stockist', help="Total amount this customer deposito.")
   
class SaleOrder(models.Model): 
    _inherit = 'sale.order'
    
    @api.one
    @api.depends('order_line', 'order_line.point_total')
    def _compute_point(self):
        self.point_amount_total = sum([line.point_total for line in self.order_line])
    
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the sale order without removing it.") 
    partner_id = fields.Many2one('res.partner', string='ST/SC/Distributor', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always', track_sequence=1, help="You can find a customer by its Name, TIN, Email or Internal Reference.")
    partner_invoice_id = fields.Many2one('res.partner', string='Alamat Tagihan', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]}, help="Invoice address for current sales order.")
    partner_shipping_id = fields.Many2one('res.partner', string='Alamat Pengiriman', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]}, help="Delivery address for current sales order.")
    partner_category_id = fields.Many2one('res.partner.category', string="Partner Tags", required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    pilih_alamat = fields.Selection([('sama','Alamat sesuai data'),('baru','Alamat baru')], string='Pilih Alamat', default='sama')
    street = fields.Text('Alamat Manual')
    partner_group_id = fields.Many2one('product.pricelist.group', string="Pricelist User", required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist Wilayah', required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Pricelist for current sales order.")
    validity_date = fields.Date(string='Tanggal', readonly=True, copy=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help="Validity date of the quotation, after this date, the customer won't be able to validate the quotation online.")
    partner_ref = fields.Char('Nama Stockist', related='partner_id.customer_ref')
    saldo_stockist = fields.Monetary(related='partner_id.saldo_stockist', string='Saldo Stockist')
    faktur_sementara = fields.Boolean('Faktur Sementara')
    barang_dikirim = fields.Boolean('Barang Dikirim')
    barang_dikirim_kesub = fields.Boolean('Ke Sub')
    apakah_promo = fields.Boolean('Promo?')
    point_amount_total = fields.Monetary(string='Total BV', compute='_compute_point', store=True)
    #picking_create = fields.Selection([('from_invoice', 'From Invoice'),('from_picking', 'From Sales')], string='Picking Policy', default='from_invoice')
    
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self.partner_category_id = self.partner_id.category_id and self.partner_id.category_id.id or False
        #self.partner_group_id = self.partner_id.partner_group_id and self.partner_id.partner_group_id.id or False
        self.pricelist_id = False
        
    @api.multi
    def _prepare_invoice(self):
        """We need to Inherit this method to set Amazon instance id in Invoice"""
        res = super(SaleOrder,self)._prepare_invoice()
        res.update({
                    'faktur_sementara':self.faktur_sementara,
                    'barang_dikirim':self.barang_dikirim,
                    'barang_dikirim_kesub':self.barang_dikirim_kesub,
                    'apakah_promo':self.apakah_promo,
                    })
        return res
    
class SaleOrderLine(models.Model): 
    _inherit = 'sale.order.line'

    poin_ok = fields.Boolean('P/N', related='product_id.poin_ok')
    point_total = fields.Float('Total BV')
    
    
#     @api.multi
#     @api.onchange('product_id')
#     def product_id_change(self):
#         if not self.product_id:
#             return {'domain': {'product_uom': []}}
# 
#         # remove the is_custom values that don't belong to this template
#         for pacv in self.product_custom_attribute_value_ids:
#             if pacv.attribute_value_id not in self.product_id.product_tmpl_id._get_valid_product_attribute_values():
#                 self.product_custom_attribute_value_ids -= pacv
# 
#         # remove the no_variant attributes that don't belong to this template
#         for ptav in self.product_no_variant_attribute_value_ids:
#             if ptav.product_attribute_value_id not in self.product_id.product_tmpl_id._get_valid_product_attribute_values():
#                 self.product_no_variant_attribute_value_ids -= ptav
# 
#         vals = {}
#         domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
#         if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
#             vals['product_uom'] = self.product_id.uom_id
#             vals['product_uom_qty'] = self.product_uom_qty or 1.0
# 
#         product = self.product_id.with_context(
#             lang=self.order_id.partner_id.lang,
#             partner=self.order_id.partner_id,
#             quantity=vals.get('product_uom_qty') or self.product_uom_qty,
#             date=self.order_id.date_order,
#             pricelist=self.order_id.pricelist_id.id,
#             uom=self.product_uom.id
#         )
# 
#         result = {'domain': domain}
# 
#         name = self.get_sale_order_line_multiline_description_sale(product)
# 
#         vals.update(name=name)
# 
#         self._compute_tax_id()
# 
#         if self.order_id.pricelist_id and self.order_id.partner_id:
#             vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
#         self.update(vals)
# 
#         title = False
#         message = False
#         warning = {}
#         if product.sale_line_warn != 'no-message':
#             title = _("Warning for %s") % product.name
#             message = product.sale_line_warn_msg
#             warning['title'] = title
#             warning['message'] = message
#             result = {'warning': warning}
#             if product.sale_line_warn == 'block':
#                 self.product_id = False
# 
#         return result
    
    @api.onchange('product_id')
    def product_id_change(self):
        domain = super(SaleOrderLine, self).product_id_change()
        if self.product_id and self.product_id.bisnis_poin:
            self.point_total = self.product_id.bisnis_poin
        if self.product_id:
            self.name = self.product_id.description_sale or self.product_id.description_purchase
        return domain
    
    def _prepare_invoice_line(self, qty):
        vals = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        vals['poin_ok'] = self.poin_ok
        vals['point_total'] = self.point_total
        return vals

            