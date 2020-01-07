# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from datetime import datetime 
from odoo.tools.misc import formatLang, format_date
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError

from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase

RANGE_VALUE = [('greater','>'), ('less','<'), ('equal_to','='), ('between','-')]

# class ProductTemplate(models.Model): 
#     _inherit = 'product.template'
#     
#     range_operation = fields.Selection(RANGE_VALUE, string='Operation')
#     min_range_qty = fields.Float('Minimum Range Qty', digits=dp.get_precision('Product Unit of Measure'))
#     max_range_qty = fields.Float('Maximum Range Qty', digits=dp.get_precision('Product Unit of Measure'))
    
    
class PurchaseOrder(models.Model): 
    _inherit = 'purchase.order'
    
#     @api.model
#     def _default_warehouse_id(self):
#         company = self.env.user.company_id.id
#         warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
#         return warehouse_ids
    
    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    } 
    
    @api.one
    @api.depends('order_line', 'order_line.point_total')
    def _compute_point(self):
        self.point_amount_total = sum([line.point_total for line in self.order_line])
    
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the purchase order without removing it.") 
    show_range = fields.Boolean('Show Range', related='partner_id.show_range', store=True)
    customer_ref = fields.Char('Nama Mitra Usaha', related='company_id.partner_id.customer_ref')
    pilih_alamat = fields.Selection([('sama','Alamat sesuai data'),('baru','Alamat baru')], string='Pilih Alamat', default='sama')
    street = fields.Text('Alamat Manual')
    #wh_picking_type_id = fields.Many2one('stock.warehouse', 'Deliver To', states=Purchase.READONLY_STATES, required=True,help="This will determine operation type of incoming shipment")
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',
        required=True, states=Purchase.READONLY_STATES)
    company_address_id = fields.Many2one('res.partner', related='company_id.partner_id', string='Alamat',
        help="Put an address if you want to deliver directly from the vendor to the customer. "
             "Otherwise, keep empty to deliver to your own company.")
    point_amount_total = fields.Monetary(string='Total BV', compute='_compute_point', store=True)
    partner_category_id = fields.Many2one('res.partner.category', string="Partner Tags", required=False, states=READONLY_STATES)
    partner_group_id = fields.Many2one('product.pricelist.group', string="Pricelist User", required=True, states=READONLY_STATES)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist Wilayah', required=True, states=READONLY_STATES, help="Pricelist for current sales order.")
    
    @api.onchange('pilih_alamat')
    def _onchange_pilih_alamat(self):
        if self.pilih_alamat == 'sama':
            self.dest_partner_id = self.company_id.partner_id and self.company_id.partner_id.id
        else:
            self.dest_partner_id = False
            
    
#     @api.onchange('partner_id')
#     def onchange_partner_id(self):
#         super(PurchaseOrder, self).onchange_partner_id()
#         self.partner_category_id = self.partner_id.category_id and self.partner_id.category_id.id or False
#         #self.partner_group_id = self.partner_id.partner_group_id and self.partner_id.partner_group_id.id or False
#         self.pricelist_id = False
        
    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            #self.partner_group_id = False
            #self.pricelist_id = False
            self.fiscal_position_id = False
            self.payment_term_id = False
            self.currency_id = self.env.user.company_id.currency_id.id
        else:
            self.fiscal_position_id = self.env['account.fiscal.position'].with_context(company_id=self.company_id.id).get_fiscal_position(self.partner_id.id)
            self.payment_term_id = self.partner_id.property_supplier_payment_term_id.id
            self.currency_id = self.partner_id.property_purchase_currency_id.id or self.env.user.company_id.currency_id.id
        self.partner_group_id = self.company_id.partner_group_ids and self.company_id.partner_group_ids.id
        self.pricelist_id = self.company_id.pricelist_ids and self.company_id.pricelist_ids.id
        self.partner_id = self.company_id.purchase_partner_id and self.company_id.purchase_partner_id.id
            
        return {}
    
    @api.multi
    @api.onchange('warehouse_id')
    def _onchange_warehouse_id(self):
        for order in self:
            for line in order.order_line:
                line.warehouse_id = order.warehouse_id and order.warehouse_id.id
                line.location_id = order.warehouse_id.lot_stock_id.id
                line.virtual_available = line.with_context(location=line.location_id)._compute_quantities()
                line.range_qty = line.with_context(virtual_available=line.virtual_available)._compute_range_message()
                #print ('----nnnn---',line,order.warehouse_id,line.location_id,line.virtual_available,line.range_qty)
        
class PurchaseOrderLine(models.Model): 
    _inherit = 'purchase.order.line'
            
#     def _get_message_values(self):
#         """ Return the source, destination and picking_type applied on a stock
#         rule. The purpose of this function is to avoid code duplication in
#         _get_message_dict functions since it often requires those data.
#         """
#         qty_available = 0.0
#         virtual_available = self.virtual_available or 0.0
#         #operation = '<'
#         return qty_available, virtual_available#, operation
    
    def _get_message_dict(self):
        """ Return a dict with the different possible message used for the
        rule message. It should return one message for each stock.rule action
        (except push and pull). This function is override in mrp and
        purchase_stock in order to complete the dictionary.
        """
        message_dict = {}
        #virtual_available = self._compute_quantities()
#         qty_available, virtual_available = self._get_message_values()
        #min = formatLang(self.env, min, currency_obj=False)
        #max = formatLang(self.env, max, currency_obj=False)
        #{'value':{'operation':typeseller}}
        if self._context.get('virtual_available'):
            virtual_available = self._context.get('virtual_available')
        else:
            virtual_available = self.virtual_available
        operation = 'Indent'
        range_available = 0.0
        max_range = {'1': 1000, '2':10000, '3':100000, '4':1000000}
        i = 1
        for max in [1000, 10000, 100000, 1000000]:
            if virtual_available <= 0.0:
                range_available = max_range[str(i)]
                operation = 'Indent'
                break
            elif virtual_available > 0.0 and virtual_available < max:
                #print ('===max==',max,str(i))
                range_available = max_range[str(i)]
                operation = '<'
                break
            elif virtual_available >= max_range['4']:
                range_available = max_range['4']
                operation = '>='
                #break
            i+=1
        #print ('===virtual_available===',operation,self.virtual_available,virtual_available,range_available)
        message_dict = {
            'operation':  _('%s') % (operation),
            'range_available': _('%s') % (int(range_available)),
        }
        return message_dict
                    
    #@api.depends('virtual_available')
            
    #@api.depends('product_id.stock_move_ids.product_qty', 'product_id.stock_move_ids.state')
    #warehouse_id.lot_stock_id
                    #print ('==_compute_quantities=',location_id,move.virtual_available)
    
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    location_id = fields.Many2one(
        'stock.location', 'Location', compute_sudo=True, required=False,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.")
    virtual_available = fields.Float(
        'Forecast Quantity', #compute='_compute_quantities', store=False,
        digits=dp.get_precision('Product Unit of Measure'),
        help="Forecast quantity (computed as Quantity On Hand "
             "- Outgoing + Incoming)\n"
             "In a context with a single Stock Location, this includes "
             "goods stored in this location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")
    range_qty = fields.Char(
        'Range Stock',# compute='_compute_range_message', store=False,
        help="Current quantity of products.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")
    poin_ok = fields.Boolean('P/N', related='product_id.poin_ok')
    point_total = fields.Float('Total BV')
    
    
    @api.multi
    def _get_display_price(self, product):
        # TO DO: move me in master/saas-16 on sale.order
        # awa: don't know if it's still the case since we need the "product_no_variant_attribute_value_ids" field now
        # to be able to compute the full price

        # it is possible that a no_variant attribute is still in a variant if
        # the type of the attribute has been changed after creation.
#         no_variant_attributes_price_extra = [
#             ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
#                 lambda ptav:
#                     ptav.price_extra and
#                     ptav not in product.product_template_attribute_value_ids
#             )
#         ]
#         if no_variant_attributes_price_extra:
#             product = product.with_context(
#                 no_variant_attributes_price_extra=no_variant_attributes_price_extra
#             )

        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            return product.with_context(pricelist=self.order_id.pricelist_id.id).price
        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

        final_price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)
        if currency != self.order_id.pricelist_id.currency_id:
            base_price = currency._convert(
                base_price, self.order_id.pricelist_id.currency_id,
                self.order_id.company_id or self.env.user.company_id, self.order_id.date_order or fields.Date.today())
        # negative discounts (= surcharge) are included in the display price
        return max(base_price, final_price)
    
    #@api.onchange('location_id')
    def _compute_locations(self):
        #for move in self:
#         if not self.product_id:
#             return
#         virtual_available = 0.0
#         location_id = False
#         if self.sudo().location_id.usage == 'internal':
#             location_id = self.sudo().location_id.id
#         if location_id:
#             res = self.product_id.sudo().with_context(location=location_id)._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), self._context.get('from_date'), self._context.get('to_date'))
#             if res[self.product_id.id].get('virtual_available'):
#                 virtual_available = res[self.product_id.id]['virtual_available']
#         print ('--virtual_available--',self.sudo().location_id,virtual_available)
        location_id = False
        if self.order_id.warehouse_id:
            location_id = self.order_id.warehouse_id and self.order_id.warehouse_id.lot_stock_id.id
        return location_id
    
    #@api.onchange('location_id')
    def _compute_quantities(self):
        #for move in self:
        if not self.product_id:
            return
        virtual_available = 0.0
        location_id = False
        if self._context.get('location'):
            location_id = self.sudo()._context.get('location').id
        #print ('----',location_id)
        if not location_id and self.sudo().location_id.usage == 'internal':
            location_id = self.sudo().location_id.id
        if location_id:
            res = self.product_id.sudo().with_context(location=location_id)._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), self._context.get('from_date'), self._context.get('to_date'))
            if res[self.product_id.id].get('virtual_available'):
                virtual_available = res[self.product_id.id]['virtual_available']
        #print ('--virtual_available--',self.sudo().location_id,self._context.get('location'),virtual_available)
        return virtual_available
        
    #@api.onchange('location_id')
    def _compute_range_message(self):
        #for pline in self:
        message_dict = self._get_message_dict()
        message = message_dict.get('operation') and message_dict['operation'] or ""
        if message_dict['operation'] == 'indent':
            message = message_dict['operation']
        elif message_dict['operation'] in ('<', '>='):
            message = message_dict['operation'] + ' ' + message_dict['range_available']
        #print ('--_get_message_dict--',message)
        return message

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        if not self.product_id:
            return
        params = {'order_id': self.order_id}
        
        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_qty'] = self.product_uom_qty or 1.0
            
        if not self.order_id.pricelist_id:
            raise UserError(_('You should define pricelist for this order.'))
        
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_qty') or self.product_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )
#         seller = self.product_id._select_seller(
#             partner_id=self.partner_id,
#             quantity=self.product_qty,
#             date=self.order_id.date_order and self.order_id.date_order.date(),
#             uom_id=self.product_uom,
#             params=params)

#         if seller or not self.date_planned:
#             self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
# 
#         if not seller:
#             if self.product_id.seller_ids.filtered(lambda s: s.name.id == self.partner_id.id):
#                 self.price_unit = 0.0
#             return
        

        price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), self.product_id.supplier_taxes_id, self.taxes_id, self.company_id)# if seller else 0.0
        if self.order_id.pricelist_id and self.order_id.partner_id:
            price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(self.product_id), self.product_id.supplier_taxes_id, self.taxes_id, self.company_id)# if seller else 0.0
#         if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
#             price_unit = seller.currency_id._convert(
#                 price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

#         if seller and self.product_uom and seller.product_uom != self.product_uom:
#             price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.price_unit = self.product_qty = 0.0
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        result['domain'] = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}

        product_lang = self.product_id.with_context(
            lang=self.partner_id.lang,
            partner_id=self.partner_id.id,
        )
        self.name = product_lang.display_name
        if product_lang.description_purchase:
            self.name = product_lang.description_purchase
        self.warehouse_id = self.sudo().order_id.warehouse_id.id
        self.location_id = self.sudo()._compute_locations()#self.order_id.warehouse_id.lot_stock_id.id
        #print ('===self.location_id===',self.location_id)
        self.virtual_available = self.sudo().with_context(location=self.location_id)._compute_quantities()
        #print ('---sss--',self.virtual_available)
        self.range_qty = self.sudo().with_context(virtual_available=self.virtual_available)._compute_range_message()
        self._compute_tax_id()

        self._suggest_quantity()
        self._onchange_quantity()
        self.point_total = self.product_id.bisnis_poin
        return result