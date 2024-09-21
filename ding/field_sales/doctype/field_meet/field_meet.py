# Copyright (c) 2024, manoj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FieldMeet(Document):
	def before_save(self):
		if self.get_from == "Customer":
			field = 'mobile_no'
		elif self.get_from == "Lead":
			field = 'mobile_no'
		elif self.get_from == "Suspect":
			field = 'mobile_no'
		elif self.get_from == "Prospect":
			field = 'mobile_no'
		mobile_number = frappe.db.get_value(self.get_from, {"name": self.party_name}, field)
		if mobile_number:
			doc = frappe.get_value("Customer",{"mobile_no":mobile_number},"name")
			if doc:
				customer_doc = frappe.get_doc("Customer",doc)
				customer_doc.append('custom_meet_log_item', {
						"document":self.get_from,
						"party_name":self.party_name,
						"check_in_time":self.check_in_time,
						"check_out_time":self.check_out_time,
						"duration":self.duration,
						'comment':self.comment,
						"rate_meeting":self.rate_meeting,

						})
				customer_doc.save()

			doc1 = frappe.get_value("Lead",{"mobile_no":mobile_number},"name")
			if doc1:
				lead_doc = frappe.get_doc("Lead",doc1)
				lead_doc.append('custom_meet_log_item', {
						"document":self.get_from,
						"party_name":self.party_name,
						"check_in_time":self.check_in_time,
						"check_out_time":self.check_out_time,
						"duration":self.duration,
						'comment':self.comment,
						"rate_meeting":self.rate_meeting,

						})
				lead_doc.save()

			doc2 = frappe.get_value("Suspect",{"mobile_no":mobile_number},"name")
			if doc2:
				suspect_doc = frappe.get_doc("Suspect",doc2)
				suspect_doc.append('meet_log_item', {
						"document":self.get_from,
						"party_name":self.party_name,
						"check_in_time":self.check_in_time,
						"check_out_time":self.check_out_time,
						"duration":self.duration,
						'comment':self.comment,
						"rate_meeting":self.rate_meeting,

						})
				suspect_doc.save()

			doc3 = frappe.get_value("Prospect",{"mobile_no":mobile_number},"name")
			if doc3:
				prospect_doc = frappe.get_doc("Prospect",doc3)
				prospect_doc.append('meet_log_item', {
						"document":self.get_from,
						"party_name":self.party_name,
						"check_in_time":self.check_in_time,
						"check_out_time":self.check_out_time,
						"duration":self.duration,
						'comment':self.comment,
						"rate_meeting":self.rate_meeting,

						})
				prospect_doc.save()