
from odoo import api, fields, models, _, SUPERUSER_ID

class ResCompany(models.Model):
    _inherit = "res.company"
    _description = 'Res Company'

    intercompany_user_id = fields.Many2one('res.users', string="Intercompany User", default=SUPERUSER_ID,
           help="Responsible user for creation of documents triggered by intercompany rules.")    
    sale_journal = fields.Many2one('account.journal', string="Sale Journal")
    purchase_journal = fields.Many2one('account.journal', string="Purchase Journal")
    auto_validation = fields.Selection([('draft', 'draft'), ('validated', 'validated')])
    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse",
        help="Default value to set on Purchase(Sales) Orders that will be created based on Sale(Purchase) Orders made to this company")
    
    @api.model
    def _find_company_from_partner(self, partner_id):
        company = self.sudo().search([('partner_id', '=', partner_id)], limit=1)
        return company or False