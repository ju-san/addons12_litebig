# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models 
from datetime import datetime
from odoo.exceptions import UserError, AccessError 

class ResCompany(models.Model):
    ''' Defining a student information '''
    _inherit = "res.company"
    
    def load_for_current_company(self, sale_tax_rate, purchase_tax_rate):
        """ Installs this chart of accounts on the current company, replacing
        the existing one if it had already one defined. If some accounting entries
        had already been made, this function fails instead, triggering a UserError.

        Also, note that this function can only be run by someone with administration
        rights.
        """
#         self.ensure_one()
#         # do not use `request.env` here, it can cause deadlocks
#         if request and request.session.uid:
#             current_user = self.env['res.users'].browse(request.uid)
#             company = current_user.company_id
#         else:
#             # fallback to company of current user, most likely __system__
#             # (won't work well for multi-company)
#             company = self.env.user.company_id
        company = self#.env.user.company_id
        self = self._context.get('chart_template_id')
        # Ensure everything is translated to the company's language, not the user's one.
        self = self.with_context(lang=company.partner_id.lang)
        if not self.env.user._is_admin():
            raise AccessError(_("Only administrators can load a charf of accounts"))

        existing_accounts = self.env['account.account'].search([('company_id', '=', company.id)])
        if existing_accounts:
            # we tolerate switching from accounting package (localization module) as long as there isn't yet any accounting
            # entries created for the company.
            if self.existing_accounting(company):
                raise UserError(_('Could not install new chart of account as there are already accounting entries existing.'))

            # delete accounting properties
            prop_values = ['account.account,%s' % (account_id,) for account_id in existing_accounts.ids]
            existing_journals = self.env['account.journal'].search([('company_id', '=', company.id)])
            if existing_journals:
                prop_values.extend(['account.journal,%s' % (journal_id,) for journal_id in existing_journals.ids])
            accounting_props = self.env['ir.property'].search([('value_reference', 'in', prop_values)])
            if accounting_props:
                accounting_props.sudo().unlink()

            # delete account, journal, tax, fiscal position and reconciliation model
            models_to_delete = ['account.reconcile.model', 'account.fiscal.position', 'account.tax', 'account.move', 'account.journal']
            for model in models_to_delete:
                res = self.env[model].search([('company_id', '=', company.id)])
                if len(res):
                    res.unlink()
            existing_accounts.unlink()

        company.write({'currency_id': self.currency_id.id,
                       'anglo_saxon_accounting': self.use_anglo_saxon,
                       'bank_account_code_prefix': self.bank_account_code_prefix,
                       'cash_account_code_prefix': self.cash_account_code_prefix,
                       'transfer_account_code_prefix': self.transfer_account_code_prefix,
                       'chart_template_id': self.id
        })

        #set the coa currency to active
        self.currency_id.write({'active': True})

        # When we install the CoA of first company, set the currency to price types and pricelists
        if company.id == 1:
            for reference in ['product.list_price', 'product.standard_price', 'product.list0']:
                try:
                    tmp2 = self.env.ref(reference).write({'currency_id': self.currency_id.id})
                except ValueError:
                    pass

        # If the floats for sale/purchase rates have been filled, create templates from them
        self._create_tax_templates_from_rates(company.id, sale_tax_rate, purchase_tax_rate)

        # Install all the templates objects and generate the real objects
        acc_template_ref, taxes_ref = self._install_template(company, code_digits=self.code_digits)

        # Set the transfer account on the company
        company.transfer_account_id = self.env['account.account'].search([('code', '=like', self.transfer_account_code_prefix + '%')])[:1]

        # Create Bank journals
        self._create_bank_journals(company, acc_template_ref)

        # Create the current year earning account if it wasn't present in the CoA
        company.get_unaffected_earnings_account()

        # set the default taxes on the company
        company.account_sale_tax_id = self.env['account.tax'].search([('type_tax_use', 'in', ('sale', 'all')), ('company_id', '=', company.id)], limit=1).id
        company.account_purchase_tax_id = self.env['account.tax'].search([('type_tax_use', 'in', ('purchase', 'all')), ('company_id', '=', company.id)], limit=1).id
        #UPDATE INTERCOMPANY
        warehouse = self.env['stock.warehouse'].search([('company_id','=',company.id)], limit=1)
        sale_journal = self.env['account.journal'].search([('company_id','=',company.id),('type','=','sale')], limit=1)
        purchase_journal = self.env['account.journal'].search([('company_id','=',company.id),('type','=','purchase')], limit=1)
        company.warehouse_id = warehouse and warehouse.id
        company.auto_validation = 'validated'
        company.intercompany_user_id = company.partner_id.user_ids and company.partner_id.user_ids.id or 1
        company.sale_journal = sale_journal and sale_journal.id
        company.purchase_journal = purchase_journal and purchase_journal.id
        return {}

    
class AccountJournal(models.Model):
    ''' Defining a student information '''
    _inherit = "account.journal"

    type = fields.Selection(selection_add=[
            ('sale_advance', 'Advance Sale'),
            ('purchase_advance', 'Advance Purchase')])
    
    
class AccountInvoice(models.Model):
    ''' Defining a student information '''
    _inherit = "account.invoice"
    
    attn = fields.Char('Attention',size=64)
    signature = fields.Char('Signature', size=64)
    journal_bank_id = fields.Many2one('account.journal', string='Payment Method', domain=[('type', 'in', ('cash','bank'))])
    
# class AccountInvoiceLine(models.Model):
#     _inherit = 'account.invoice.line'
#     
#     def _get_price_tax(self):
#         for l in self:
#             l.price_tax = l.price_total - l.price_subtotal
#     
#     price_tax = fields.Monetary(string='Tax Amount', compute='_get_price_tax', store=False)
    