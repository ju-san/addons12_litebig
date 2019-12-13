# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare



MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
}
# Since invoice amounts are unsigned, this is how we know if money comes in or goes out
MAP_INVOICE_TYPE_PAYMENT_SIGN = {
    'out_invoice': 1,
    'in_refund': -1,
    'in_invoice': -1,
    'out_refund': 1,
}

class account_abstract_payment(models.AbstractModel):
    _inherit = "account.abstract.payment"
    _description = "Contains the logic shared between models which allows to register payments"
    
    payment_difference = fields.Monetary(compute='_compute_payment_difference', readonly=True)
    payment_difference_handling = fields.Selection([('open', 'Akan dibayarkan kembali'), ('reconcile', 'Cashback/Saldo Stockist')], default='open', string="Sisa Kekurangan", copy=False)
    journal_nonbank_id1 = fields.Many2one('account.journal', 'Journal Non Bank 1')
    desc1 = fields.Char('Keterangan')
    amount1 = fields.Monetary(string='Payment Amount 1')
    journal_nonbank_id2 = fields.Many2one('account.journal', 'Journal Non Bank 2')
    desc2 = fields.Char('Keterangan')
    amount2 = fields.Monetary(string='Payment Amount 2')
    journal_nonbank_id3 = fields.Many2one('account.journal', 'Journal Non Bank 3')
    desc3 = fields.Char('Keterangan')
    amount3 = fields.Monetary(string='Payment Amount 3')
    journal_nonbank_id4 = fields.Many2one('account.journal', 'Journal Non Bank 4')
    desc4 = fields.Char('Keterangan')
    amount4 = fields.Monetary(string='Payment Amount 4')
    journal_nonbank_id5 = fields.Many2one('account.journal', 'Journal Non Bank 5')
    desc5 = fields.Char('Keterangan')
    amount5 = fields.Monetary(string='Payment Amount 5')
    desc = fields.Char('Keterangan')
    total_transfer_amount = fields.Monetary(compute='_kekurangan_transfer_amount', readonly=True)
    kekurangan_transfer_amount = fields.Monetary(compute='_kekurangan_transfer_amount', readonly=True)
    journal_code = fields.Selection([('2', 'Receipt'),('3', 'Others')], string="Journal Code", default='2')
    
    @api.depends('invoice_ids', 'amount', 'amount1', 'amount2', 'amount3', 'amount4', 'amount5', 'payment_date', 'currency_id')
    def _compute_payment_difference(self):
        for pay in self.filtered(lambda p: p.invoice_ids):
            payment_amount = -pay.amount-pay.amount1-pay.amount2-pay.amount3-pay.amount4-pay.amount5 if pay.payment_type == 'outbound' else pay.amount+pay.amount1+pay.amount2+pay.amount3+pay.amount4+pay.amount5
            pay.payment_difference = pay._compute_payment_amount() - payment_amount
    
    @api.depends('invoice_ids', 'amount', 'amount1', 'amount2', 'amount3', 'amount4', 'amount5', 'payment_date', 'currency_id')
    def _kekurangan_transfer_amount(self):
        for pay in self.filtered(lambda p: p.invoice_ids):
            payment_amount = pay.amount1-pay.amount2-pay.amount3-pay.amount4-pay.amount5 if pay.payment_type == 'outbound' else pay.amount1+pay.amount2+pay.amount3+pay.amount4+pay.amount5
            pay.total_transfer_amount = payment_amount
            pay.kekurangan_transfer_amount = pay._compute_payment_amount() - payment_amount
    
class AccountPayment(models.Model): 
    _inherit = 'account.payment'
    
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the sale order without removing it.") 
    date_invoice = fields.Date(string='Tanggal Invoice', related='invoice_ids.date_invoice')
    no_invoice = fields.Char('No. Faktur')
    tgl_invoice = fields.Date('Tgl. Faktur')
    partner_code = fields.Many2one('res.partner', string='Kode Stockist', related='invoice_ids.partner_id')
    saldo_stockist = fields.Monetary(related='partner_id.saldo_stockist', string='Saldo Stockist Awal')
    total_penjualan = fields.Monetary(related='invoice_ids.invoice_line_ids.sale_line_ids.order_id.amount_total', string='Total Penjualan')
    kode_gudang = fields.Many2one('stock.warehouse', related='invoice_ids.invoice_line_ids.sale_line_ids.order_id.warehouse_id', string='Kode Gudang')
    payment_title = fields.Char(default='Pembayaran via Transfer, Pot Rabat, Fee Gudang')
#     journal_nonbank_id1 = fields.Many2one('account.journal', 'Journal Non Bank 1')
#     desc1 = fields.Char('Keterangan')
#     amount1 = fields.Monetary(string='Payment Amount 1')
#     journal_nonbank_id2 = fields.Many2one('account.journal', 'Journal Non Bank 2')
#     desc2 = fields.Char('Keterangan')
#     amount2 = fields.Monetary(string='Payment Amount 2')
#     journal_nonbank_id3 = fields.Many2one('account.journal', 'Journal Non Bank 3')
#     desc3 = fields.Char('Keterangan')
#     amount3 = fields.Monetary(string='Payment Amount 3')
#     desc = fields.Char('Keterangan')
    writeoff_label = fields.Char(
        string='Cashback',
        help='Change label of the counterpart that will hold the payment difference',
        default='Cashback')
    saldo_stockist_akhir = fields.Monetary(string='Saldo Stockist Akhir')
    total_debit = fields.Monetary(string='Total Debit')
    total_credit = fields.Monetary(string='Total Kredit')
    
    @api.onchange('amount', 'saldo_stockist', 'payment_difference', 'payment_difference_handling')
    def _onchange_amount_all(self):
        if self.payment_difference_handling == 'reconcile':
            self.saldo_stockist_akhir = self.saldo_stockist - self.payment_difference
            
    @api.multi
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconcilable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconcilable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            amount1 = rec.amount1 * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            amount2 = rec.amount2 * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            amount3 = rec.amount3 * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            amount4 = rec.amount4 * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            amount5 = rec.amount5 * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            #amount_total = amount + amount1 + amount2 + amount3
            move = rec.with_context(amount1=amount1,amount2=amount2,amount3=amount3,amount4=amount4,amount5=amount5)._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
        return True

    def _create_payment_entry(self, amount):
        """ Create a journal entry corresponding to a payment, if the payment references invoice(s) they are reconciled.
            Return the journal entry.
        """
        aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
        amount1 = self._context.get('amount1')
        amount2 = self._context.get('amount2')
        amount3 = self._context.get('amount3')
        amount4 = self._context.get('amount4')
        amount5 = self._context.get('amount5')
        debit, credit, amount_currency, currency_id = aml_obj.with_context(date=self.payment_date)._compute_amount_fields(amount, self.currency_id, self.company_id.currency_id)
        debit1, credit1, amount_currency1, currency_id = aml_obj.with_context(date=self.payment_date)._compute_amount_fields(amount1, self.currency_id, self.company_id.currency_id)
        debit2, credit2, amount_currency2, currency_id = aml_obj.with_context(date=self.payment_date)._compute_amount_fields(amount2, self.currency_id, self.company_id.currency_id)
        debit3, credit3, amount_currency3, currency_id = aml_obj.with_context(date=self.payment_date)._compute_amount_fields(amount3, self.currency_id, self.company_id.currency_id)
        debit4, credit4, amount_currency4, currency_id = aml_obj.with_context(date=self.payment_date)._compute_amount_fields(amount4, self.currency_id, self.company_id.currency_id)
        debit5, credit5, amount_currency5, currency_id = aml_obj.with_context(date=self.payment_date)._compute_amount_fields(amount5, self.currency_id, self.company_id.currency_id)

        move = self.env['account.move'].create(self._get_move_vals())

        #Write line corresponding to invoice payment
        counterpart_aml_dict = self._get_shared_move_line_vals(debit+debit1+debit2+debit3, credit+credit1+credit2+credit3, amount_currency+amount_currency1+amount_currency2+amount_currency3, move.id, False)
        counterpart_aml_dict.update(self._get_counterpart_move_line_vals(self.invoice_ids))
        counterpart_aml_dict.update({'currency_id': currency_id})
        counterpart_aml = aml_obj.create(counterpart_aml_dict)

        #Reconcile with the invoices
        if self.payment_difference_handling == 'reconcile' and self.payment_difference:
            writeoff_line = self._get_shared_move_line_vals(0, 0, 0, move.id, False)
            debit_wo, credit_wo, amount_currency_wo, currency_id = aml_obj.with_context(date=self.payment_date)._compute_amount_fields(self.payment_difference, self.currency_id, self.company_id.currency_id)
            writeoff_line['name'] = self.writeoff_label
            writeoff_line['account_id'] = self.writeoff_account_id.id
            writeoff_line['debit'] = debit_wo
            writeoff_line['credit'] = credit_wo
            writeoff_line['amount_currency'] = amount_currency_wo
            writeoff_line['currency_id'] = currency_id
            writeoff_line = aml_obj.create(writeoff_line)
            if counterpart_aml['debit'] or (writeoff_line['credit'] and not counterpart_aml['credit']):
                counterpart_aml['debit'] += credit_wo - debit_wo
            if counterpart_aml['credit'] or (writeoff_line['debit'] and not counterpart_aml['debit']):
                counterpart_aml['credit'] += debit_wo - credit_wo
            counterpart_aml['amount_currency'] -= amount_currency_wo

        #Write counterpart lines
        if not self.currency_id.is_zero(self.amount):
            if not self.currency_id != self.company_id.currency_id:
                amount_currency = 0
            liquidity_aml_dict = self._get_shared_move_line_vals(credit, debit, -amount_currency, move.id, False)
            liquidity_aml_dict.update(self._get_liquidity_move_line_vals(-amount))
            aml_obj.create(liquidity_aml_dict)
        if not self.currency_id.is_zero(self.amount1):
            if not self.currency_id != self.company_id.currency_id:
                amount_currency1 = 0
            liquidity_aml_dict1 = self._get_shared_move_line_vals(credit1, debit1, -amount_currency1, move.id, False)
            liquidity_aml_dict1.update(self.with_context(journal1=self.journal_nonbank_id1, desc1=self.desc1)._get_liquidity_move_line_vals(-amount1))
            aml_obj.create(liquidity_aml_dict1)
        if not self.currency_id.is_zero(self.amount2):
            if not self.currency_id != self.company_id.currency_id:
                amount_currency2 = 0
            liquidity_aml_dict2 = self._get_shared_move_line_vals(credit2, debit2, -amount_currency2, move.id, False)
            liquidity_aml_dict2.update(self.with_context(journal2=self.journal_nonbank_id2, desc2=self.desc2)._get_liquidity_move_line_vals(-amount2))
            aml_obj.create(liquidity_aml_dict2)
        if not self.currency_id.is_zero(self.amount3):
            if not self.currency_id != self.company_id.currency_id:
                amount_currency3 = 0
            liquidity_aml_dict3 = self._get_shared_move_line_vals(credit3, debit3, -amount_currency3, move.id, False)
            liquidity_aml_dict3.update(self.with_context(journal3=self.journal_nonbank_id3, desc3=self.desc3)._get_liquidity_move_line_vals(-amount3))
            aml_obj.create(liquidity_aml_dict3)

        #validate the payment
        if not self.journal_id.post_at_bank_rec:
            move.post()

        #reconcile the invoice receivable/payable line(s) with the payment
        if self.invoice_ids:
            self.invoice_ids.register_payment(counterpart_aml)

        return move
    
    def _get_liquidity_move_line_vals(self, amount):
        name = self._context.get('desc1') or self._context.get('desc2') or self._context.get('desc3') or self.name
        if self.payment_type == 'transfer':
            name = _('Transfer to %s') % self.destination_journal_id.name
        if self._context.get('journal1'):
            account_id = self.payment_type in ('outbound','transfer') and self._context.get('journal1').default_debit_account_id.id or self._context.get('journal1').default_credit_account_id.id
        elif self._context.get('journal2'):
            account_id = self.payment_type in ('outbound','transfer') and self._context.get('journal2').default_debit_account_id.id or self._context.get('journal2').default_credit_account_id.id
        elif self._context.get('journal3'):
            account_id = self.payment_type in ('outbound','transfer') and self.payment_type in ('outbound','transfer') and self._context.get('journal3').default_debit_account_id.id or self._context.get('journal3').default_credit_account_id.id
        elif self._context.get('journal4'):
            account_id = self.payment_type in ('outbound','transfer') and self.payment_type in ('outbound','transfer') and self._context.get('journal4').default_debit_account_id.id or self._context.get('journal4').default_credit_account_id.id
        elif self._context.get('journal5'):
            account_id = self.payment_type in ('outbound','transfer') and self.payment_type in ('outbound','transfer') and self._context.get('journal5').default_debit_account_id.id or self._context.get('journal5').default_credit_account_id.id
        else:
            account_id = self.payment_type in ('outbound','transfer') and self.journal_id.default_debit_account_id.id or self.journal_id.default_credit_account_id.id
        #print ('===x===',account_id)
        vals = {
            'name': name,
            'account_id': account_id,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id != self.company_id.currency_id and self.currency_id.id or False,
        }
        # If the journal has a currency specified, the journal item need to be expressed in this currency
        if self.journal_id.currency_id and self.currency_id != self.journal_id.currency_id:
            amount = self.currency_id._convert(amount, self.journal_id.currency_id, self.company_id, self.payment_date or fields.Date.today())
            debit, credit, amount_currency, dummy = self.env['account.move.line'].with_context(date=self.payment_date)._compute_amount_fields(amount, self.journal_id.currency_id, self.company_id.currency_id)
            vals.update({
                'amount_currency': amount_currency,
                'currency_id': self.journal_id.currency_id.id,
            })

        return vals