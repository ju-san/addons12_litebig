# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
from odoo.osv.orm import browse_record
from odoo.osv import expression

ADDRESS_FIELDS = ('street', 'street2', 'rt', 'rw', 'kecamatan_id', 'kabupaten_id', 'zip', 'city', 'state_id', 'country_id')


class PartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    code = fields.Char(string='Tag Code', required=True)
    
class ResPartner(models.Model):    
    _name = "res.partner"
    _inherit = ['res.partner', 'mail.thread']

    def _compute_partner_docs_count(self):
        Attachment = self.env['ir.attachment']
        for task in self:
            task.doc_count = Attachment.search_count([
                ('res_model', '=', 'res.partner'), ('res_id', '=', task.id)
            ])
            
#     @api.model
#     def create(self, vals):
#         if not vals.get('ref', False):
#             if vals.get('is_company', False):
#                 if vals.get('customer', False):
#                     vals['ref'] = self.env['ir.sequence'].next_by_code('customer.code') or 'New'
#                 elif vals.get('supplier', False):
#                     vals['ref'] = self.env['ir.sequence'].next_by_code('supplier.code') or 'New'
#                 else:
#                     vals['ref'] = self.env['ir.sequence'].next_by_code('employee.code') or 'New'
#         return super(ResPartner, self).create(vals)
    
#     @api.model
#     def _default_branch(self):
#         return self.env.user.branch_id
        
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'draft':
            return 'aos_nasa_partner.mt_partner_created'
        if 'state' in init_values and self.state == 'validate':
            return 'aos_nasa_partner.mt_partner_validated'
        elif 'state' in init_values and self.state == 'reject':
            return 'aos_nasa_partner.mt_partner_rejected'
        return super(ResPartner, self)._track_subtype(init_values)
    
    
#     brand_id = fields.Many2many('res.partner.brand', column1='partner_id',
#                 column2='brand_id', string='Brands')
#     type_id = fields.Many2many('res.partner.type', column1='partner_id',
#                 column2='type_id', string='Types')
    #branch_id = fields.Many2one('res.branch', string='Branch', default=_default_branch)
    #===========================================================================
    # RELATED INFO
    #===========================================================================
    doc_count = fields.Integer(compute='_compute_partner_docs_count', string="Number of documents attached")
    state_name = fields.Char(related='state_id.name', string="State Name", readonly=True)
    country_name = fields.Char(related='country_id.name', string="Country Name", readonly=True)
    title_name = fields.Char(related='title.name', string="Title Name", readonly=True)
    title_shortcut = fields.Char(related='title.shortcut', string="Title Shortcut", readonly=True)
    #===========================================================================
    # PERSONAL INFO
    #===========================================================================
    name = fields.Char('Kode ST/SC')
    attn = fields.Char('Attention')
    aktive_ok = fields.Boolean('Aktif/Tidak')
    customer_ref = fields.Char('Nama ST/SC/Distributor')
    vendor_ref = fields.Char('Nama Vendor')
    npwp_personal = fields.Char('NPWP Pribadi')
    npwp_badan = fields.Char('NPWP Badan')
    
    nama_ibu = fields.Char('Nama Ibu Kandung')
    nama_pasangan = fields.Char('Nama Pasangan')
    jml_anak = fields.Integer('NPWP Badan')
    status_nikah = fields.Selection([('belum','Belum Menikah'),
                                     ('menikah','Menikah'),
                                     ('cerai','Cerai')], string='Status Pernikahan')
    tgl_lahir_pasangan = fields.Date('Tgl Lahir')
    t4_lahir_pasangan = fields.Char('Tempat Lahir Pasangan')
    nama_pewaris = fields.Char('Nama Pewaris')
    tgl_lahir_pewaris = fields.Date('Tgl Pewaris')
    t4_lahir_pewaris = fields.Char('Tempat Lahir Pewaris')
    t4_ambil_bonus = fields.Char('Tempate Pengambilan Bonus')
    point_value = fields.Integer('Point Value')
    name_upline = fields.Char('Name Upline')
    number_upline = fields.Char('Nomor Upline')
    #ref = fields.Char('Kode Mitra')
    #ktp = fields.Char('KTP')
    sim_number = fields.Char('SIM')
    sim_type = fields.Selection([('sima','SIM A'),('simb1','SIM BI'),('simb2','SIM BII'),('simc','SIM C'),('simd','SIM D')], string='SIM')
    sim_number2 = fields.Char('SIM 2')
    sim_type2 = fields.Selection([('sima','SIM A'),('simb1','SIM BI'),('simb2','SIM BII'),('simc','SIM C'),('simd','SIM D')], string='SIM 2')
    sim_number3 = fields.Char('SIM 3')
    sim_type3 = fields.Selection([('sima','SIM A'),('simb1','SIM BI'),('simb2','SIM BII'),('simc','SIM C'),('simd','SIM D')], string='SIM 3')
    passport_number = fields.Char('Passport Number')
    passport_expire = fields.Date('Passport Expire')
    race_id = fields.Many2one('res.race', string="Race/RAS")
    religion_id = fields.Many2one('res.religion', string="Religion")
    birthday = fields.Date('Birthday')
    birthplace = fields.Char('Birthplace')
    #===========================================================================
    # LEGAL DOCUMENT
    #===========================================================================
    no_nppkp = fields.Char('NPPKP', help='Nomor Pengukuhan Pengusaha Kena Pajak')
    no_siup = fields.Char('No SIUP', help='Nomor Surat Izin Usaha Perdagangan')
    no_tdp = fields.Char('No TDP', help='Nomor Tanda Daftar Perusahaan')
    no_akta = fields.Char('No Akta Pendirian', help='Nomor Akta Pendirian Perusahaan')
    check_nppkp = fields.Boolean('Check NPPKP', help='Check Pengukuhan Pengusaha Kena Pajak')
    check_siup = fields.Boolean('Check SIUP', help='Check Surat Izin Usaha Perdagangan')
    check_tdp = fields.Boolean('Check TDP', help='Check Tanda Daftar Perusahaan')
    check_akta = fields.Boolean('Check Akta Pendirian', help='Check Akta Pendirian Perusahaan')
    #===========================================================================
    state = fields.Selection([('draft','Draft'),
                              ('validate','Validate'),
                              ('reject','Rejected')], track_visibility='onchange', 
                             default='draft', string='Status') 
    
#     _sql_constraints = [
#         ('npwp_uniq', 'unique(npwp)', 'The npwp of the customer must be unique!'),
#     ]

#     @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name', 'ref')
#     def _compute_display_name(self):
#         diff = dict(show_address=None, show_address_only=None, show_email=None)
#         names = dict(self.with_context(**diff).name_get())
#         for partner in self:
#             partner.display_name = names.get(partner.id)


#     @api.model
#     def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
#         restricted_customer = self.env.user.has_group('sales_person_customer_access.group_restricted_customer')
#         if restricted_customer:
#             args = [('salesperson_ids','in',self.env.user.id)] + list(args)
#         return super(ResPartner, self)._search(args, offset, limit, order, count, access_rights_uid)
            
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('ref', '=ilike', name + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        partners = self.search(domain + args, limit=limit)
        return partners.name_get()
    
    def _get_name(self):
        """ Utility method to allow name_get to be overrided without re-browse the partner """
        partner = self
        name = partner.name or ''

        if partner.company_name or partner.parent_id:
            if not name and partner.type in ['invoice', 'delivery', 'other']:
                name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
            if not partner.is_company:
                name = "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
        if self._context.get('show_address_only'):
            name = partner._display_address(without_company=True)
        if self._context.get('show_address'):
            name = name + "\n" + partner._display_address(without_company=True)
        name = name.replace('\n\n', '\n')
        name = name.replace('\n\n', '\n')
        if self._context.get('address_inline'):
            name = name.replace('\n', ', ')
        if self._context.get('show_email') and partner.email:
            name = "%s <%s>" % (name, partner.email)
        if self._context.get('html_format'):
            name = name.replace('\n', '<br/>')
        if self._context.get('show_vat') and partner.vat:
            name = "%s - %s" % (name, partner.vat)
        return name    
    
    
#     @api.multi
#     def name_get(self):
#         res = []
#         for partner in self:
#             name = partner._get_name()
#             res.append((partner.id, name))
#         return res

#     @api.multi
#     @api.depends('name', 'ref')
#     def name_get(self):
#         result = []
#         for partner in self:
#             name = partner.name
#             if partner.ref:
#                 name = partner.name + ' (' + partner.ref + ')' 
#             result.append((partner.id, name))
#         return result
    
    @api.multi
    def attachment_partner_view(self):
        self.ensure_one()
        domain = [
            ('res_model', '=', 'res.partner'), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the partner.</p><p>
                        Send messages or log internal notes with attachments to link
                        documents to your partner.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }
        
    @api.multi
    def attachment_legal_view(self):
        context = self._context
        self.ensure_one()
        domain = [('res_model', '=', 'res.partner'), ('res_id', 'in', self.ids)]
        if context.get('legal_type') == 'NPPKP':
            domain += [('name','ilike','NPPKP')]
        elif context.get('legal_type') == 'SIUP':
            domain += [('name','ilike','SIUP')]
        elif context.get('legal_type') == 'TPD':
            domain += [('name','ilike','TPD')]
        elif context.get('legal_type') == 'AKTA':
            domain += [('name','ilike','AKTA')]
        elif context.get('legal_type') == 'NPWP':
            domain += [('name','ilike','NPWP')]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the partner legal company.</p><p>
                        Send messages or log internal notes with attachments to link
                        documents to your partner.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }
    
#     @api.model
#     def mail_reminder(self):
#         today = datetime.now()
#         partners = self.env['res.partner'].search([])
#         for part in partners:
#             if part.birthday:
#                 daymonth = datetime.strptime(part.birthday, "%Y-%m-%d")
#                 if today.day == daymonth.day and today.month == daymonth.month:
#                     self.send_birthday_wish(part.id)
#         return
# 
#     @api.model
#     def send_birthday_wish(self, partner_id):
#         su_id = self.env['res.partner'].browse(SUPERUSER_ID)
#         customer_template_id = self.env['ir.model.data'].get_object_reference('aos_nasa_partner', 'partner_birthday_notification')[1]
#         template_browse = self.env['mail.template'].browse(template_id)
#         email_to = self.env['res.partner'].browse(partner_id).email
#         if template_browse:
#             values = template_browse.generate_email(partner_id, fields=None)
#             values['email_to'] = email_to
#             values['email_from'] = su_id.email
#             values['res_id'] = False
#             if not values['email_to'] and not values['email_from']:
#                 pass
#             mail_mail_obj = self.env['mail.mail']
#             msg_id = mail_mail_obj.create(values)
#             if msg_id:
#                 mail_mail_obj.send(msg_id)
#             return True
    
    @api.multi
    def draft_partner(self):
        return self.write({'state': 'draft', 'active':False})
    
    @api.multi
    def validate_partner(self):
        return self.write({'state': 'validate', 'active':True})
    
    @api.multi
    def reject_partner(self):
        return self.write({'state': 'reject', 'active':False})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
