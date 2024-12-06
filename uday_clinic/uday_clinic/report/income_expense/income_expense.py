# Copyright (c) 2024, Priyansh Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder.functions import (
	Extract,
	Sum,
)
from frappe.utils import get_last_day, getdate
from pypika import Order

from uday_clinic.uday_clinic.report.expense.expense import (
	get_columns as get_expense_columns,
)
from uday_clinic.uday_clinic.report.expense.expense import (
	get_data as get_expense_data,
)
from uday_clinic.uday_clinic.report.income.income import (
	get_columns as get_income_columns,
)
from uday_clinic.uday_clinic.report.income.income import (
	get_data as get_income_data,
)
from uday_clinic.utils import MONTHS_MAP, REVERSE_MONTHS_MAP


def execute(filters=None):
	filters = frappe._dict(filters)
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns():
	return [
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
		{
			"fieldname": "total_income",
			"label": "Total Income",
			"fieldtype": "Currency",
			"width": 120,
		},
		{
			"fieldname": "total_expense",
			"label": "Total Expense",
			"fieldtype": "Currency",
			"width": 120,
		},
	]


def get_data(filters):
	income_data = get_income_data(filters)
	expense_data = get_expense_data(filters)

	data = {}

	for row in income_data + expense_data:
		month = row["month"]
		year = row["year"]
		key = "total_income" if row.get("is_income") else "total_expense"
		data.setdefault((month, year), {}).update({"month": month, "year": year, key: row["total"]})

	return list(data.values())
