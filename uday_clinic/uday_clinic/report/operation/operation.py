# Copyright (c) 2024, Priyansh Shah and contributors
# For license information, please see license.txt
from datetime import datetime

import frappe
from frappe.query_builder.functions import (
	Extract,
	IfNull,
	Sum,
)
from frappe.utils import get_last_day, getdate
from pypika import Order

from uday_clinic.utils import MONTHS_MAP, REVERSE_MONTHS_MAP


def execute(filters=None):
	filters = frappe._dict(filters)
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data


def get_columns(filters):
	columns = [
		{
			"fieldname": "month",
			"label": "Month",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"fieldname": "year",
			"label": "Year",
			"fieldtype": "Data",
			"width": 120,
		},
	]

	fields = frappe.get_all("Operation Types", pluck="name", order_by="creation")

	columns.extend(
		[
			{
				"fieldname": frappe.scrub(field.lower()),
				"label": field,
				"fieldtype": "Int",
				"width": 120,
			}
			for field in fields
		]
	)
	columns.append(
		{
			"fieldname": "total",
			"label": "Total",
			"fieldtype": "Int",
			"width": 120,
		}
	)
	return columns


def get_data(filters):
	result = _get_data(filters)
	print(result)
	return list(process_result(result, filters).values())


def _get_data(filters):
	INCOME_RECORDER = frappe.qb.DocType("Income Recorder")
	INCOME_RECORDER_ITEMS = frappe.qb.DocType("Income Recorder Items")
	start_date, end_date = get_start_and_end_date(
		REVERSE_MONTHS_MAP.get(filters.month),
		int(filters.year or datetime.now().year),
		int(filters.no_of_months or 6),
	)
	if not start_date or not end_date:
		return []

	query = (
		frappe.qb.from_(INCOME_RECORDER)
		.join(INCOME_RECORDER_ITEMS)
		.on(INCOME_RECORDER.name == INCOME_RECORDER_ITEMS.parent)
		.select(
			INCOME_RECORDER_ITEMS.type,
			INCOME_RECORDER_ITEMS.sub_type,
			INCOME_RECORDER_ITEMS.method,
			Extract("month", INCOME_RECORDER.date).as_("month"),
			Extract("year", INCOME_RECORDER.date).as_("year"),
			Sum(IfNull(INCOME_RECORDER_ITEMS.number, 0)).as_("number_of_operation"),
		)
		.groupby(
			Extract("month", INCOME_RECORDER.date),
			Extract("year", INCOME_RECORDER.date),
		)
		.where(INCOME_RECORDER.party == filters.party)
		.where(INCOME_RECORDER.date >= start_date)
		.where(INCOME_RECORDER.date <= end_date)
		.where(INCOME_RECORDER_ITEMS.type == "Indoor")
		.where(INCOME_RECORDER_ITEMS.sub_type == "Operation")
		.orderby(Extract("year", INCOME_RECORDER.date).as_("year"), order=Order.desc)
		.orderby(Extract("month", INCOME_RECORDER.date).as_("month"), order=Order.desc)
	)

	query = query.groupby(INCOME_RECORDER_ITEMS.method)

	return query.run(as_dict=True)


def process_result(result, filters):
	data = {}

	for row in result:
		month = row.month
		year = row.year
		if (month, year) not in data:
			data[(month, year)] = {
				"month": MONTHS_MAP[month],
				"year": year,
				"total": 0,
			}

		column_name = frappe.scrub(row.method.lower())

		data[(month, year)].update(
			{
				column_name: row.number_of_operation,
				"total": data[(month, year)]["total"] + row.get("number_of_operation", 0),
			}
		)

	return data


def get_start_and_end_date(month, year, no_of_months):
	if not month:
		return None, None

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
