// Copyright (c) 2024, Priyansh Shah and contributors
// For license information, please see license.txt

const MONTHS = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
];
const current_month = MONTHS[new Date().getMonth()];

frappe.query_reports["Delivery"] = {
	filters: [
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "Link",
			options: "Party",
			reqd: 1,
		},
		{
			fieldname: "month",
			label: __("Month"),
			fieldtype: "Select",
			options: MONTHS,
			reqd: 1,
			default: current_month,
		},
		{
			fieldname: "year",
			label: __("Year"),
			fieldtype: "Autocomplete",
			options: ["2023", "2024", "2025", "2026"],
			reqd: 1,
			default: new Date().getFullYear(),
		},
		{
			fieldname: "no_of_months",
			label: __("Number of Months"),
			fieldtype: "Select",
			options: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
			reqd: 1,
			default: "6",
		},
		{
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			options: ["Method", "Caste"],
			reqd: 1,
			default: "Method",
		},
	],
};
