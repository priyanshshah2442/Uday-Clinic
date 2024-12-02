// Copyright (c) 2024, Priyansh Shah and contributors
// For license information, please see license.txt
frappe.query_reports["Income Report"] = {
	filters: [
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "Link",
			options: "Party",
			reqd: 1,
		},
		{
			fieldname: "date_range",
			label: __("Date Range"),
			fieldtype: "Check",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			depends_on: "date_range",
			default: frappe.datetime.add_months(frappe.datetime.nowdate(), -1),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			depends_on: "date_range",
			default: frappe.datetime.nowdate(),
		},
		{
			fieldname: "group_by_month",
			label: __("Group By Month"),
			fieldtype: "Check",
			depends_on: "date_range",
			default: 1,
		},
	],
};
