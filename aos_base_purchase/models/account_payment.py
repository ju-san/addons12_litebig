# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class AccountPayment(models.Model):
    _inherit = "account.payment"
    
    purchase_ids = fields.Many2many('purchase.order', string='Purchase Order')
    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    street = fields.Char(related='partner_id.street')
    street2 = fields.Char(related='partner_id.street2')
    zip = fields.Char(string='ZIP', related='partner_id.zip', change_default=True, store=True)
    city = fields.Char(string='City', related='partner_id.city', store=True)
    state_id = fields.Many2one("res.country.state", string='State', related='partner_id.state_id', store=True)
    country_id = fields.Many2one('res.country', string='Country', related='partner_id.country_id', store=True)
    