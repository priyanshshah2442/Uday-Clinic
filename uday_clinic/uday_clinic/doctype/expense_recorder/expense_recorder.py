# Copyright (c) 2024, Priyansh Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form


class ExpenseRecorder(Document):
	def validate(self):
		self.validate_duplicate_record()
		self.validate_duplicate_types()
		self.validate_amounts()
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

	def validate_duplicate_types(self):
		types_map = {}
		for row in self.records:
			if row.type in types_map:
				frappe.throw(f"Row #{row.idx}: {row.type} already added at Row: {types_map[row.type]}")
			types_map[row.type] = row.idx

	def validate_amounts(self):
		for row in self.records:
			if row.amount <= 0:
				frappe.throw(f"Row #{row.idx}: Amount must be greater than 0")

	def calculate_total(self):
		self.total_amount = sum(d.amount for d in self.records)
