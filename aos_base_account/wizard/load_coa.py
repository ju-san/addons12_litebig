from odoo import models, api, _, fields
from odoo.exceptions import UserError

class LoadCoaTemplate(models.TransientModel):
    _name = "load.coa.template"
    _description = "Load Coa Template"

    chart_template_id = fields.Many2one('account.chart.template', string='Template',
        domain="[('visible','=', True)]")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    
    @api.multi
    def install_coa(self):
        if self.chart_template_id and self.chart_template_id != self.company_id.chart_template_id:
            self.chart_template_id.load_for_current_company(10.0, 10.0)
        return {'type': 'ir.actions.act_window_close'}
