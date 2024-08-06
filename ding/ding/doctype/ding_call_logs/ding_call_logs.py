# Copyright (c) 2024, manoj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DingCallLogs(Document):
    pass
    # def before_save(self):
    #     if(self.reference_doctype=="Customer"):
    #         doc=frappe.get_doc("Customer",self.reference_docname)
    #         doc.custom_ding_call_ref=self.name
    #         doc.save()

    # def on_trash(self):
    #     if(self.reference_doctype=="Customer"):
    #         doc=frappe.get_doc("Customer",self.reference_docname)
    #         doc.custom_ding_call_ref=None
    #         doc.save()