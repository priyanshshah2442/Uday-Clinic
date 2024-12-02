// Copyright (c) 2024, Priyansh Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on("Income Recorder", {
	refresh(frm) {
		frm.set_query("type", "sources", () => {
			return {
				filters: {
					is_group: 1,
				},
			};
		});

		frm.set_query("sub_type", "sources", (frm, cdt, cdn) => {
			return {
				filters: {
					is_group: 0,
					parent_income_types: frappe.get_doc(cdt, cdn).type,
				},
			};
		});
	},
});

frappe.ui.form.on("Income Recorder Items", {
	amount(frm, cdt, cdn) {
		set_total_amount(frm);
	},
	sub_type(frm, cdt, cdn) {
		const doc = frappe.get_doc(cdt, cdn);
		if (!doc.sub_type) return;

		if (!doc.type) {
			frappe.model.set_value(cdt, cdn, "sub_type", "");
			frappe.throw(`Row ${doc.idx}: Please select Type first`);
		}
	},
});

function set_total_amount(frm) {
	const total_amount = frm.doc.sources.reduce((acc, item) => {
		return acc + item.amount;
	}, 0);

	frm.set_value("total", total_amount);
}
