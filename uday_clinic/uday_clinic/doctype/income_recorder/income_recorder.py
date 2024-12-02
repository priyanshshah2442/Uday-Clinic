# Copyright (c) 2024, Priyansh Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form


class IncomeRecorder(Document):
	def validate(self):
		self.validate_duplicate_record()
		self.validate_duplicate_sources()
		self.validate_numbers()
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

	def validate_duplicate_sources(self):
		sources_map = {}
		for row in self.sources:
			if (row.type, row.sub_type or "") in sources_map:
				main_msg_subj = f"{row.type} and {row.sub_type}" if row.sub_type else row.type
				frappe.throw(
					"{} already added at Row: {}".format(
						main_msg_subj,
						frappe.bold(sources_map[(row.type, row.sub_type or "")]),
					)
				)
			sources_map[(row.type, row.sub_type or "")] = row.idx

	def validate_numbers(self):
		for row in self.sources:
			if row.number <= 0:
				frappe.throw(f"Row: {row.idx} Number must be greater than 0")

	def calculate_total(self):
		self.total = sum(d.amount for d in self.sources)
