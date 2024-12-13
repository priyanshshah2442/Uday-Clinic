// Copyright (c) 2024, Priyansh Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on("Income Recorder", {
	refresh(frm, cdt, cdn) {
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
		set_sub_type_options(frm, cdt, cdn);
		set_method_options(frm, cdt, cdn);
	},
});

frappe.ui.form.on("Income Recorder Items", {
	sources_add(frm, cdt, cdn) {
		set_sub_type_options(frm, cdt, cdn);
	},
	amount(frm, cdt, cdn) {
		set_total_amount(frm);
	},
	type(frm, cdt, cdn) {
		frappe.model.set_value(cdt, cdn, "sub_type", "");
		set_sub_type_options(frm, cdt, cdn);
	},
	sub_type(frm, cdt, cdn) {
		set_method_options(frm, cdt, cdn);
	},
});

function set_total_amount(frm) {
	const total_amount = frm.doc.sources.reduce((acc, item) => {
		return acc + item.amount;
	}, 0);

	frm.set_value("total", total_amount);
}

function set_sub_type_options(frm, cdt, cdn) {
	const doc = frappe.get_doc(cdt, cdn);
	if (!doc.type && cdt === "Income Recorder Items") return;

	let options;
	if (doc.type === "Consultation" || cdt === "Income Recorder") {
		options = frappe.boot.consultation_types;
	} else if (doc.type === "Others") {
		options = frappe.boot.other_income_types;
	} else if (doc.type === "Indoor") {
		options = frappe.boot.indoor_income_types;
	}
	frm.fields_dict.sources.grid.update_docfield_property("sub_type", "options", options);
}

function set_method_options(frm, cdt, cdn) {
	const doc = frappe.get_doc(cdt, cdn);
	if (!doc.type && cdt === "Income Recorder Items") return;

	let options;
	if (doc.sub_type === "Operation" || cdt === "Income Recorder") {
		options = frappe.boot.operation_types;
	} else if (doc.sub_type === "Delivery") {
		options = frappe.boot.delivery_types;
	} else {
		options = [""];
	}
	frm.fields_dict.sources.grid.update_docfield_property("method", "options", options);
}
