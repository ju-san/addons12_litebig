# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models 
from datetime import datetime 

class PartnerBrand(models.Model):
    _name = 'res.partner.brand'
    _order = 'name'

    name = fields.Char(string='Title', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

    _sql_constraints = [('name_uniq', 'unique (name)', "Title name already exists !")]


class PartnerType(models.Model):
    _name = 'res.partner.type'
    _order = 'name'

    name = fields.Char(string='Title', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)

    _sql_constraints = [('name_uniq', 'unique (name)', "Title name already exists !")]