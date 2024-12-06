# Copyright (c) 2024, Priyansh Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder.functions import (
	Extract,
	Sum,
)
from frappe.utils import get_last_day, getdate
from pypika import Order

from uday_clinic.utils import MONTHS_MAP, REVERSE_MONTHS_MAP


def execute(filters=None):
	filters = frappe._dict(filters)
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	expense_types = frappe.get_all("Expense Types", order_by="creation asc")
	columns = [
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

	columns.extend(
		[
			{
				"label": row.name,
				"fieldname": frappe.scrub(row.name),
				"fieldtype": "Currency",
				"width": 120,
			}
			for row in expense_types
		]
	)

	columns.append(
		{
			"label": "Total",
			"fieldname": "total",
			"fieldtype": "Currency",
			"width": 120,
		}
	)

	return columns


def get_data(filters):
	result = _get_data(filters)
	return list(process_result(result).values())


def _get_data(filters):
	EXPENSE_RECORDER = frappe.qb.DocType("Expense Recorder")
	EXPENSE_RECORDER_ITEMS = frappe.qb.DocType("Expense Recorder Items")
	start_date, end_date = get_start_and_end_date(
		REVERSE_MONTHS_MAP[filters.month], int(filters.year), int(filters.no_of_months)
	)
	query = (
		frappe.qb.from_(EXPENSE_RECORDER)
		.join(EXPENSE_RECORDER_ITEMS)
		.on(EXPENSE_RECORDER.name == EXPENSE_RECORDER_ITEMS.parent)
		.select(
			EXPENSE_RECORDER_ITEMS.type,
			Sum(EXPENSE_RECORDER_ITEMS.amount).as_("amount"),
			Extract("month", EXPENSE_RECORDER.date).as_("month"),
			Extract("year", EXPENSE_RECORDER.date).as_("year"),
		)
		.groupby(
			Extract("month", EXPENSE_RECORDER.date),
			Extract("year", EXPENSE_RECORDER.date),
			EXPENSE_RECORDER_ITEMS.type,
		)
		.where(EXPENSE_RECORDER.party == filters.party)
		.where(EXPENSE_RECORDER.date >= start_date)
		.where(EXPENSE_RECORDER.date <= end_date)
		.orderby(Extract("year", EXPENSE_RECORDER.date).as_("year"), order=Order.desc)
		.orderby(Extract("month", EXPENSE_RECORDER.date).as_("month"), order=Order.desc)
	)

	return query.run(as_dict=True)


def process_result(result):
	data = {}

	for row in result:
		month = row.month
		year = row.year
		if (month, year) not in data:
			data[(month, year)] = {
				"month": MONTHS_MAP[month],
				"year": year,
				"total": 0,
				"is_expense": True,
			}

		data[(month, year)].update(
			{
				frappe.scrub(row.type): row.amount,
				"total": data[(month, year)]["total"] + row.amount,
			}
		)

	return data


def get_start_and_end_date(month, year, no_of_months):
	no_of_months -= 1
	if month - no_of_months <= 0:
		start_month = month - no_of_months + 12
		start_year = year - 1
	else:
		start_month = month - no_of_months
		start_year = year

	start_date = getdate(f"{start_year}-{start_month}-01")
	end_date = get_last_day(getdate(f"{year}-{month}-01"))

	return start_date, end_date
