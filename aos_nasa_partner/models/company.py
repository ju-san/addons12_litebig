# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
from odoo.osv.orm import browse_record

class ResCompany(models.Model):
    _inherit = "res.company"
    
    alias = fields.Char('Alias',size=64)
    state_name = fields.Char(related='state_id.name', string="State Name", readonly=True)
    country_name = fields.Char(related='country_id.name', string="Country Name", readonly=True)
    title_name = fields.Char(related='partner_id.title.name', string="Title Name", readonly=True)
    title_shortcut = fields.Char(related='partner_id.title.shortcut', string="Title Shortcut", readonly=True)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
