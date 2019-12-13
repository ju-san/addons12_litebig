# -*- coding: utf-8 -*-
# import odoo.addons.decimal_precision as dp
# from odoo import api, fields, models, tools, _
# from odoo.modules import get_module_resource
# from odoo.osv.expression import get_unaccent_wrapper
# from odoo.exceptions import UserError, ValidationError
# from odoo.osv.orm import browse_record
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
import math
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

import odoo.addons.decimal_precision as dp


class ResUsersCategory(models.Model):
    _name = 'res.users.category'
    _description = 'Res Users Tags'
    
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    color = fields.Integer(string='Color Index')
    description = fields.Char('Description')
    users_ids = fields.Many2many('res.users', column1='category_id', column2='user_id', string='Users')

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    color = fields.Integer(string='Color Index')
    
class ResUsers(models.Model):
    _inherit = "res.users"
    _inherit = ['res.users', 'mail.thread', 'ir.needaction_mixin']
    
    category_id = fields.Many2many('res.users.category', column1='user_id', column2='category_id', string='Tags')