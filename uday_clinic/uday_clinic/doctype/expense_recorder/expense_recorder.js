// Copyright (c) 2024, Priyansh Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Recorder", {
	refresh(frm) {
		frm.fields_dict.date.datepicker.update({
			maxDate: new Date(),
		});
	},
});

frappe.ui.form.on("Expense Recorder Items", {
	amount(frm, cdt, cdn) {
		set_total_amount(frm);
	},
});

function set_total_amount(frm) {
	const total_amount = frm.doc.records.reduce((acc, item) => {
		return acc + item.amount;
	}, 0);

	frm.set_value("total_amount", total_amount);
}
