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

    
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    state = fields.Selection([('draft', 'Not Active'),('confirmed', 'Active')], string='Status', default='draft', readonly=True)
            
    @api.multi
    def confirm_product_template(self):
        vals = {}
        vals['state'] = 'confirmed'
        #print ("===confirm_product_template===",vals)
        variants = self.env['product.product']
        for variant in self.product_variant_ids:
            variants += variant
        variants.write(vals)
        self.write({'state': 'confirmed'})
        return vals
    
    @api.multi
    def draft_product_template(self):
        vals = {}
        vals['state'] = 'draft'
        #print ("===draft_product_template===",vals)
        variants = self.env['product.product']
        for variant in self.product_variant_ids:
            variants += variant
        variants.write(vals)
        self.write({'state': 'draft'})
        return vals
            
class ProductProduct(models.Model):
    _inherit='product.product'
    
    
    state = fields.Selection([('draft', 'Not Active'),('confirmed', 'Active')], string='Status', readonly=True)
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        # TDE FIXME: strange
        if self._context.get('search_default_confirmed'):
            args += [('state', '=', 'confirmed')]
        return super(ProductProduct, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            products = self.env['product.product']
            if operator in positive_operators:
                products = self.search([('default_code', '=', name)] + args, limit=limit)
                if not products:
                    products = self.search([('barcode', '=', name)] + args, limit=limit)
            if not products and operator not in expression.NEGATIVE_TERM_OPERATORS:
                # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
                # on a database with thousands of matching products, due to the huge merge+unique needed for the
                # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
                # Performing a quick memory merge of ids in Python will give much better performance
                products = self.search(args + [('default_code', operator, name)], limit=limit)
                if not limit or len(products) < limit:
                    # we may underrun the limit because of dupes in the results, that's fine
                    limit2 = (limit - len(products)) if limit else False
                    products += self.search(args + [('name', operator, name), ('id', 'not in', products.ids)], limit=limit2)
            elif not products and operator in expression.NEGATIVE_TERM_OPERATORS:
                products = self.search(args + ['&', ('default_code', operator, name), ('name', operator, name)], limit=limit)
            if not products and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    products = self.search([('default_code', '=', res.group(2))] + args, limit=limit)
            # still no results, partner in context: search on supplier info as last hope to find something
            if not products and self._context.get('partner_id'):
                suppliers = self.env['product.supplierinfo'].search([
                    ('name', '=', self._context.get('partner_id')),
                    '|',
                    ('product_code', operator, name),
                    ('product_name', operator, name)])
                if suppliers:
                    products = self.search([('product_tmpl_id.seller_ids', 'in', suppliers.ids)], limit=limit)
            # type get on variant
            #===================================================================
            if not products:
                products = self.search([('attribute_value_ids.name', operator, name)], limit=limit)
            #===================================================================
        else:
            products = self.search(args, limit=limit)
        return products.name_get()
    
    
    @api.multi    
    def confirm_product(self):
        return self.write({'state': 'confirmed'})
        
    @api.multi    
    def draft_product(self):
        return self.write({'state': 'draft'})