# Copyright (c) 2024, Priyansh Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import Interval
from frappe.query_builder.functions import (
	CurDate,
	Extract,
	Sum,
)


def execute(filters=None):
	filters = frappe._dict(filters)
	validate_filters(filters)
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def validate_filters(filters):
	if filters.date_range:
		if not filters.from_date:
			frappe.throw("From Date are required")

		if not filters.to_date:
			frappe.throw("To Date are required")

		if filters.from_date > filters.to_date:
			frappe.throw("From Date must be before To Date")


def get_columns(filters):
	columns = []
	if not filters.date_range or (filters.date_range and filters.group_by_month):
		columns.extend(
			[
				{
					"label": "Month",
					"fieldname": "month",
					"fieldtype": "Data",
					"width": 120,
				},
				{
					"label": "Year",
					"fieldname": "year",
					"fieldtype": "Data",
					"width": 120,
				},
			]
		)
	else:
		columns.append(
			{
				"label": "Date",
				"fieldname": "date",
				"fieldtype": "Date",
				"width": 120,
			}
		)

	columns.extend(
		[
			{
				"label": "Type",
				"fieldname": "type",
				"fieldtype": "Data",
				"width": 120,
			},
			{
				"label": "Sub Type",
				"fieldname": "sub_type",
				"fieldtype": "Data",
				"width": 120,
			},
			{
				"label": "Number",
				"fieldname": "number",
				"fieldtype": "Int",
				"width": 120,
			},
			{
				"label": "Amount",
				"fieldname": "amount",
				"fieldtype": "Currency",
				"width": 120,
			},
		]
	)

	return columns


def get_data(filters):
	INCOME_RECORDER = frappe.qb.DocType("Income Recorder")
	INCOME_RECORDER_ITEMS = frappe.qb.DocType("Income Recorder Items")

	query = (
		frappe.qb.from_(INCOME_RECORDER)
		.join(INCOME_RECORDER_ITEMS)
		.on(INCOME_RECORDER.name == INCOME_RECORDER_ITEMS.parent)
		.select(
			INCOME_RECORDER_ITEMS.type,
			INCOME_RECORDER_ITEMS.sub_type,
			Sum(INCOME_RECORDER_ITEMS.amount).as_("amount"),
			Sum(INCOME_RECORDER_ITEMS.number).as_("number"),
			Extract("month", INCOME_RECORDER.date).as_("month"),
			Extract("year", INCOME_RECORDER.date).as_("year"),
		)
		.where(INCOME_RECORDER.date > CurDate() - Interval(years=1))
		.groupby(
			Extract("month", INCOME_RECORDER.date).as_("month"),
			Extract("year", INCOME_RECORDER.date).as_("year"),
			INCOME_RECORDER_ITEMS.type,
			INCOME_RECORDER_ITEMS.sub_type,
		)
	)

	return query.run(as_dict=True)
