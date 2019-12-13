# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SaleConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
# 
#     purchase_landed_cost_calculate = fields.Selection([
#         (0, 'By Weight'),
#         (1, 'By Volume'),
#         (2, 'By Quantity'),
#         (3, 'By Amount'),
#         ], string="Manage Landed Cost Calculation", default=3)
#     
#     group_landed_cost_by_weight = fields.Boolean('Landed Cost by Weight', implied_group='aos_base_purchase.group_landed_cost_by_weight')
#     group_landed_cost_by_volume = fields.Boolean('Landed Cost by Volume', implied_group='aos_base_purchase.group_landed_cost_by_volume')
#     group_landed_cost_by_quantity = fields.Boolean('Landed Cost by Quantity', implied_group='aos_base_purchase.group_landed_cost_by_quantity')
#     group_landed_cost_by_amount = fields.Boolean('Landed Cost by Amount', implied_group='aos_base_purchase.group_landed_cost_by_amount')
    module_aos_sale_weight_volume = fields.Boolean('Sales Weight & Volume')
    group_sale_cost_by_weight = fields.Boolean('Sales Weight', implied_group='aos_base_sale.group_sale_cost_by_weight')
    group_sale_cost_by_volume = fields.Boolean('Sales Volume', implied_group='aos_base_sale.group_sale_cost_by_volume')

#     @api.onchange('purchase_landed_cost_calculate')
#     def onchange_warehouse_and_location_usage_level(self):
#         self.group_landed_cost_by_weight = self.purchase_landed_cost_calculate == 0
#         self.group_landed_cost_by_volume = self.purchase_landed_cost_calculate == 1
#         self.group_landed_cost_by_quantity = self.purchase_landed_cost_calculate == 2
#         self.group_landed_cost_by_amount = self.purchase_landed_cost_calculate == 3
