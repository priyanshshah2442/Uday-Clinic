# Copyright (c) 2024, Priyansh Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form
from frappe.utils.formatters import format_value


class IncomeRecorder(Document):
	def validate(self):
		self.validate_duplicate_record()
		self.validate_amount()
		self.calculate_total()

	def validate_duplicate_record(self):
		if name := frappe.db.exists(
			self.doctype,
			{
				"date": self.date,
				"party": self.party,
				"name": ("!=", self.name),
			},
		):
			frappe.throw(
				"Record {} already created for party {} on {}".format(
					get_link_to_form(self.doctype, name),
					frappe.bold(self.party),
					frappe.bold(self.date),
				)
			)

	def calculate_total(self):
		self.total = sum(d.amount for d in self.sources)

	def validate_amount(self):
		for row in self.sources:
			if row.amount <= 0:
				frappe.throw(
					"Row: #{} Amount must be greater than {}".format(
						row.idx, format_value(0, {"fieldtype": "Currency"})
					)
				)


@frappe.whitelist()
def get_options():
	options = {}
	options["consultation_types"] = frappe.get_all("Consultation Types", pluck="name")
	options["delivery_types"] = frappe.get_all("Delivery Types", pluck="name")
	options["operation_types"] = frappe.get_all("Operation Types", pluck="name")
	options["other_income_types"] = frappe.get_all("Other Income Types", pluck="name")
	options["indoor_income_types"] = frappe.get_all("Indoor Income Types", pluck="name")

	return options
