from odoo.report import report_sxw
from odoo.tools.translate import _
from odoo.osv import osv
from odoo.addons.aos_base import amount_to_text_id
from odoo.addons.report_webkit import webkit_report
from odoo.addons.report_webkit.report_helper import WebKitHelper
from odoo.addons.report_webkit.webkit_report import webkit_report_extender

class purchase_report_webkit(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(purchase_report_webkit, self).__init__(cr, uid, name, context=context)
        self.line_no = 0
        self.localcontext.update({
            'convert':self.convert,
            'blank_line':self.blank_line,
        })
     
    def convert(self, amount, cur=False):
        amt_id = amount_to_text_id.amount_to_text(amount, 'id', cur)
        return amt_id
    
    def blank_line(self, lines):
        return len(lines)

webkit_report.WebKitParser('report.aos.new.purchase','purchase.order', 
                       'aos_purchase/report/aos_print_purchase.mako',
                       parser=purchase_report_webkit)

webkit_report.WebKitParser('report.aos.new.rfq','purchase.order', 
                       'aos_purchase/report/aos_print_rfq.mako',
                       parser=purchase_report_webkit)
