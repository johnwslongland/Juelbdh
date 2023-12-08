# Copyright (c) 2023, J Longland and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


def get_template_details(template):
	if not template:
		return []
##  frappe.msgprint("Detail")
	return frappe.get_all(
		"BDH Template Parameter Item",
		fields=[
			"bdh_parameter",
		],
		filters={"parenttype": "BDH Template", "parentfield": "bdh_parameters"},
		order_by="idx",
	)



class BDH(Document):

	item_code_options = []


	@frappe.whitelist()
	def validate_child_table(self):
		all_set = all(item.parameter and item.done and item.employee and item.date for item in self.check_items)
		return all_set
#		all_set = True
#		for item in self.check_items:
#			if not (item.parameter and item.done and item.employee and item.date):
#				all_set = False
#		return {
#			"table_all_set": all_set
#		}



	@frappe.whitelist()
	def get_template(self):
#	   frappe.msgprint("Get Template")
		self.set("check_items", [])
		parameters = get_template_details(self.bdh_template)
		for d in parameters:
			child = self.append("check_items", {"parameter": d.bdh_parameter})
			child.update(d)


	@frappe.whitelist()
	def get_customer(self):
		if self.sales_order:
			sales_order_doc = frappe.get_doc("Sales Order", self.sales_order)
			self.customer = sales_order_doc.customer
			options = self.set_item_code_filters()

			return {
				"Item_Code_Options": options
			}



	@frappe.whitelist()
	def set_item_code_filters(self):
		if self.sales_order:
			# Filter item codes based on the selected sales_order
			item_codes = frappe.get_all("Sales Order Item",
				filters={"parent": self.sales_order},
				fields=["item_code"]
			)
			item_code_list = [item.item_code for item in item_codes]

			# Get the item_code_options and initialize it as an empty list if it's None
			item_code_options = self.get("item_code")
			if item_code_options is None:
				item_code_options = []

#		   item_code_options[:] = []  # Clear existing options
			for item_code in item_code_list:
				item_code_options.append(item_code)

#		   frappe.msgprint(item_code_options)
			return item_code_options

	@frappe.whitelist()
	def get_sales_order_item_details(self, item_code):
		if self.sales_order:
			sales_order_items = frappe.get_all("Sales Order Item",
				filters={"parent": self.sales_order, "item_code": item_code},
				fields=["item_name", "delivery_date"]
			)
			if sales_order_items:
				self.item_name = sales_order_items[0].item_name
				self.delivery_date = sales_order_items[0].delivery_date


