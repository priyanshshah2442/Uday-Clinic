import frappe


def set_bootinfo(bootinfo):
	bootinfo["consultation_types"] = frappe.get_all("Consultation Types", pluck="name")
	bootinfo["delivery_types"] = frappe.get_all("Delivery Types", pluck="name")
	bootinfo["operation_types"] = frappe.get_all("Operation Types", pluck="name")
	bootinfo["other_income_types"] = frappe.get_all("Other Income Types", pluck="name")
	bootinfo["indoor_income_types"] = frappe.get_all("Indoor Income Types", pluck="name")
