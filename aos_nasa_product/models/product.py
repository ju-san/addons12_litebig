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
from odoo.addons import decimal_precision as dp

class ProductState(models.Model):
    _name = "product.state"
    _description = 'Product State'
    _order = 'sequence,id'
    
    name = fields.Char('Name')
    sequence = fields.Integer('Sequence')
    
class ProductTemplate(models.Model):
    _inherit = "product.template"
#     
#     @api.model
#     def _get_product_partner(self):
#         return self.env.user.partner_id and self.env.user.partner_id.parent_id and self.env.user.partner_id.parent_id.id or False
#     
#     @api.multi
#     def _track_subtype(self, init_values):
#         self.ensure_one()
#         if 'name' in init_values:  # assigned -> new
#             return 'aos_product.mt_product_tmpl_new_create'
#         return super(ProductTemplate, self)._track_subtype(init_values)
#     
#     def _get_default_branch_id(self):
#         return self._context.get('force_branch', self.env.user.branch_id.id)
# 
#     branch_id = fields.Many2one('res.branch', string='Branch',
#         default=_get_default_branch_id, required=False)
#     name = fields.Char('Name', index=True, required=True, translate=True, track_visibility='always')
#     price_change_ok = fields.Boolean(string="Price Can be Edited", default=False, help='Check this if the price is editable in Sale Order Line Form')
    state_id = fields.Many2one('product.state', string='Product Status')
    indent_ok = fields.Boolean('Indent/Non Indent')
    status_izin = fields.Selection([('izin','Sudah berizin'),
                                    ('proses','Dalam Proses'),
                                    ('belum','Belum berizin')], string='Status Berizin')
#     batch_prod = fields.Char('Batch Produksi')
#     buyer_ids = fields.One2many('product.customerinfo', 'product_tmpl_id', 'Customer')
#     hs_code_id = fields.Many2one('hs.code', string="HS Code", help="Standardized code for international shipping and goods declaration", oldname="x_hs_code")
#     hs_categ_id = fields.Many2one('hs.code.category', string='Category')
#     #hs_code = fields.Char(string="HS Code", help="Standardized code for international shipping and goods declaration", oldname="x_hs_code")
#     type_lot = fields.Selection([('warranty','Warranty'),('expiry','Expiry')], string='Type', default='warranty')
#     warranty = fields.Integer('Warranty')
#     unique_variant = fields.Boolean('Is Unique Variant', default=False)
#     #===========================================================================
#     # COMPUTE ALL VARIANT
#     #===========================================================================
#     product_brand_id = fields.Many2one('product.brand', string='Brand', 
#         )#compute='_compute_variants', inverse='_set_variants', store=True)
#     categ_brand_ids = fields.Many2many('product.brand.category', string="Tags", 
#         )#compute='_compute_variants', inverse='_set_variants', store=True)
#     product_sku = fields.Char('SKU', 
#         )#compute='_compute_variants', inverse='_set_variants', store=True)
#     product_merk_id = fields.Many2one('product.merk', 'Merk', 
#         )#compute='_compute_variants', inverse='_set_variants', store=True)
#     product_type_id = fields.Many2one('product.type', 'Inventory Part Type',
#         )#compute='_compute_variants', inverse='_set_variants', store=True)
#     product_serial_number = fields.Float('Serial Sequence',
#         )#compute='_compute_variants', inverse='_set_variants', store=True ,help="Serial Number")
#     vendor_id = fields.Many2one('res.partner', 'Vendor Access', default=_get_product_partner)
#     tags_ids = fields.Many2many('product.tags', string='Product Tags')
#     type = fields.Selection(default='product')
    poin_ok = fields.Boolean('Point/Non Point')
    poin_value = fields.Integer('Point Value')
    bisnis_poin = fields.Float('Bisnis Poin')
    tgl_produksi = fields.Date('Tgl. Produksi')
    batch_prod = fields.Char('Batch Produksi')
    barcode = fields.Char('QC Code', oldname='ean13', related='product_variant_ids.barcode', readonly=False)
    
    
#     @api.onchange('global_ok')
#     def onchange_global_ok(self):
#         if self.global_ok:
#             self.company_id = False
#     
#     @api.onchange('hs_categ_id')
#     def onchange_hs_code_related(self):
#         if not self.hs_categ_id:
#             return
#         self.hs_code_id = self.hs_categ_id.hs_code and self.hs_categ_id.hs_code.id or False
#         
#     @api.multi
#     def confirm_product_template(self):
#         vals = super(ProductTemplate, self).confirm_product_template()
#         vals['product_merk_id'] = self.product_merk_id and self.product_merk_id.id or False
#         vals['product_type_id'] = self.product_type_id and self.product_type_id.id or False
#         vals['product_brand_id'] = self.product_brand_id and self.product_brand_id.id or False
#         variants = self.env['product.product']
#         for variant in self.product_variant_ids:
#             variants += variant
#         variants.write(vals)
#         return vals
#             
#     @api.multi
#     def draft_product_template(self):
#         vals = super(ProductTemplate, self).draft_product_template()
#         variants = self.env['product.product']
#         for variant in self.product_variant_ids:
#             variants += variant
#         variants.write(vals)
#         return vals
            
class ProductProduct(models.Model):
    _inherit='product.product'
    
#     categ_brand_ids = fields.Many2many('product.brand.category', column1='product_id', column2='categ_brand_id', string='Tags')    
#     product_sku = fields.Char('SKU')
#     product_detail = fields.Char('Detail Description')
#     product_serial_number = fields.Float('Serial Sequence',defaults='00000' ,help="Serial Number")
#     product_brand_id = fields.Many2one('product.brand', string='Brand')
#     
#     @api.model
#     def create(self, vals):
#         if vals.get('product_tmpl_id',[]):
#             product_tmpl=self.env['product.template'].browse(vals['product_tmpl_id'])
#             vals['product_merk_id'] = product_tmpl.product_merk_id and product_tmpl.product_merk_id.id or False
#             vals['product_type_id'] = product_tmpl.product_type_id and product_tmpl.product_type_id.id or False
#             vals['product_brand_id'] = product_tmpl.product_brand_id and product_tmpl.product_brand_id.id or False
#         return super(ProductProduct, self).create(vals)
