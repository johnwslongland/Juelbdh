// Copyright (c) 2023, J Longland and contributors
// For license information, please see license.txt


frappe.ui.form.on('BDH', {
//  refresh: function(frm) {

//  }
//  after_field_update: function(frm, fieldname) {
//      if fieldname == "sales_order":
//          frm.set_item_code_filters();
//  },
	before_submit: function(frm) {
//        frappe.show_alert("Validate", 5);
		return frm.call({
			method: "validate_child_table",
			doc: frm.doc,
			callback: function(r) {
				if (r.message.table_all_set) {
					frm.set_df_property('approval', 'read_only', 0);
				} else {
					frappe.validated = false;
					frappe.throw("BDH Items table incomplete");
					frappe.validated = false;
				}
			}
		});
	},
	bdh_template: function(frm) {
		if (frm.doc.bdh_template) {
//          frm.save();
			return frm.call({
				method: "get_template",
				doc: frm.doc,
				callback: function() {
 					refresh_field('check_items');
				}
			});
		}
	},
	sales_order: function(frm) {
///     console.log("Sales Order code");
///     frappe.show_alert("Sales Orer Code", 5);
		if (frm.doc.sales_order) {
			return frm.call({
				method: "get_customer",
				doc: frm.doc,
				callback: function(r) {
					refresh_field('customer');
///                 frappe.show_alert("Refresh", 5);
//                  console.log(r.message);
					var Item_Code_Options = r.message.Item_Code_Options;
//                  Item_Code_Options = {'item_code': '1R-004', 'item_code': 'S1C05354'}
///                 console.log(Item_Code_Options);

					frm.set_query('item_code', function() {
						return {
							filters: {
								item_code: ['in', Item_Code_Options]
							},
						};
					});

				}
			});



//          var ItemCodeOptions = frm.doc.item_code_options;
//          frm.set_query('item_code', function() {
//              return {
//                  filters: [
//                      ['item_code', 'item_name', 'in', ItemCodeOptions]
//                  ]
//              };
//          });
		}
	},
	item_code: function(frm) {
		if (frm.doc.item_code) {
			frm.call({
				method: "get_sales_order_item_details",
				doc: frm.doc,
				args: { item_code: frm.doc.item_code },
				callback: function(r) {
					frm.refresh_field('item_name');
					frm.refresh_field('delivery_date');
				}
			});
		}
	}
});


