from odoo import models, api, _, fields
from odoo.exceptions import UserError, AccessError

class LoadCoaTemplate(models.TransientModel):
    _name = "load.coa.template"
    _description = "Load Coa Template"

    chart_template_id = fields.Many2one('account.chart.template', string='Template',
        domain="[('visible','=', True)]")
    #company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    
    @api.multi
    def install_coa(self):
        context = dict(self._context or {})
        companies = self.env['res.company'].browse(context.get('active_ids'))
        company_to_install = self.env['res.company']
        for comp in companies:
            if not comp.chart_template_id:
                company_to_install += comp
        if company_to_install:
            for company in company_to_install:
                company.with_context(chart_template_id=self.chart_template_id).load_for_current_company(10.0, 10.0)
        return {'type': 'ir.actions.act_window_close'}
    