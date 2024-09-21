# Copyright (c) 2024, manoj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


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
    @frappe.whitelist()	
    def show_data(self):
        current_user = frappe.session.user
        current_date = datetime.now().date()
        
        logs = frappe.db.get_all(
            "Ding Call Logs", 
            filters={
                'call_handler': current_user,
                'follow_up_date_time': ['between', [str(current_date) + ' 00:00:00', str(current_date) + ' 23:59:59']]
            }, 
            fields=['call_handler', 'follow_up_date_time', 'note','reference_doctype','reference_docname','disposition']
        )
        
        formatted_logs = []
        for log in logs:
            follow_up_date_time = log.get('follow_up_date_time')
            if follow_up_date_time:
                follow_up_date_time_str = follow_up_date_time.strftime('%Y-%m-%d, %H:%M:%S')
            else:
                follow_up_date_time_str = 'None'
            
            # formatted_log = f"Username = {log['call_handler']} Time = {follow_up_date_time_str} Document = {log['call_handler']} Party Name = {log['reference_docname']}"
            formatted_log = f"Document = {log['reference_doctype']} Party Name = {log['reference_docname']}"
            formatted_logs.append(formatted_log)
        
        final_output = "<br>".join(formatted_logs)
        frappe.msgprint(final_output)

    def before_save(self):
        if self.reference_doctype == "Customer":
            field = 'mobile_no'
        elif self.reference_doctype == "Lead":
            field = 'mobile_no'
        elif self.reference_doctype == "Suspect":
            field = 'mobile_no'
        elif self.reference_doctype == "Prospect":
            field = 'mobile_no'
        mobile_number = frappe.db.get_value(self.reference_doctype, {"name": self.reference_docname}, field)
        if mobile_number:
            doc = frappe.get_value("Customer",{"mobile_no":mobile_number},"name")
            if doc:
                customer_doc = frappe.get_doc("Customer",doc)
                customer_doc.append('custom_ding_call_item', {
                        "call_handler":self.call_handler,
                        "duration":self.duration,
                        "reference_document_type":self.reference_doctype,
                        "reference_name":self.reference_docname,

                        })
                customer_doc.save()

            doc1 = frappe.get_value("Lead",{"mobile_no":mobile_number},"name")
            if doc1:
                lead_doc = frappe.get_doc("Lead",doc1)
                lead_doc.append('custom_ding_call_item', {
                        "call_handler":self.call_handler,
                        "duration":self.duration,
                        "reference_document_type":self.reference_doctype,
                        "reference_name":self.reference_docname,

                        })
                lead_doc.save()

            doc2 = frappe.get_value("Suspect",{"mobile_no":mobile_number},"name")
            if doc2:
                suspect_doc = frappe.get_doc("Suspect",doc2)
                suspect_doc.append('ding_call_item', {
                        "call_handler":self.call_handler,
                        "duration":self.duration,
                        "reference_document_type":self.reference_doctype,
                        "reference_name":self.reference_docname,

                        })
                suspect_doc.save()

            doc3 = frappe.get_value("Prospect",{"mobile_no":mobile_number},"name")
            if doc3:
                prospect_doc = frappe.get_doc("Prospect",doc3)
                prospect_doc.append('ding_call_item', {
                       "call_handler":self.call_handler,
                        "duration":self.duration,
                        "reference_document_type":self.reference_doctype,
                        "reference_name":self.reference_docname,

                        })
                prospect_doc.save()

        