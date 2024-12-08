// Copyright (c) 2024, Priyansh Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on("Income Recorder", {
	refresh(frm) {
		frm.set_query("sub_type", "sources", (frm, cdt, cdn) => {
			return {
				filters: {
					income_category: frappe.get_doc(cdt, cdn).type,
				},
			};
		});
		frm.fields_dict.date.datepicker.update({
			maxDate: new Date(),
		});
	},
});

frappe.ui.form.on("Income Recorder Items", {
	amount(frm, cdt, cdn) {
		set_total_amount(frm);
	},
	type(frm, cdt, cdn) {
		frappe.model.set_value(cdt, cdn, "sub_type", "");
	},
});

function set_total_amount(frm) {
	const total_amount = frm.doc.sources.reduce((acc, item) => {
		return acc + item.amount;
	}, 0);

	frm.set_value("total", total_amount);
}
