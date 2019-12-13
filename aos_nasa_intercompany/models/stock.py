# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base_geolocalize.models.res_partner import (
    geo_find, geo_query_address)

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class stock_warehouse(models.Model):
    _inherit = 'stock.warehouse'
    
    users_ids = fields.Many2many('res.users', 'stock_warehouse_users_rel',
        'warehouse_id', 'user_id', string='Users Restrictions')