// Copyright (c) 2023, techno lead llc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Company Loan Management', {
	refresh: function(frm) {
		
		if (frm.doc.show == 0) {
			frm.add_custom_button(__("Create Journal Entry"), function() {
				frappe.call({
					method: "customizations.customizations.doctype.company_loan_management.company_loan_management.loan_journal_entries",
					args: {
						start_date: frm.doc.posting_date,
						credit: frm.doc.credit_account,
						debit: frm.doc.debit_account,
						total: frm.doc.amount
					}
				}).then((r) => {
					if(r.message == "ok") {
						frm.set_value("show", 1);
						refresh_field("show");
						frm.save()
						frappe.show_alert({
							message:__('Hi, Journal Entry Generated Successfully'),
							indicator:'green'
						}, 5);
						setTimeout(() => {
							location.reload()
						}, 5000);
						
						
						
					}
					console.log("Response", r)
				})
			
			});

		} else {}
			
	}
});

frappe.ui.form.on('Repayments', {


	add_jv:function(frm, cdt, cdn){
		var d = locals[cdt][cdn];
		// console.log("Date: ", d.date, " Amount: ", d.amount, " Interest: ",d.interest, " Total: ", d.total)
		frappe.call({
			method: "customizations.customizations.doctype.company_loan_management.company_loan_management.create_journal_entries",
			args: {
				start_date: d.date,
				credit: frm.doc.repayment_credit_account,
				debit: frm.doc.repayment_debit_account,
				interest: frm.doc.repayment_interest_account,
				total: d.total,
				interest_total:d.interest,
				credit_total: d.amount
			}
		}).then((r) => {
			if(r.message == "ok") {
				
				
				frappe.show_alert({
					message:__('Hi, Journal Entry Generated Successfully'),
					indicator:'green'
				}, 5);
				setTimeout(() => {
					
					location.reload()
				}, 5000);
				
				
				
			}
			console.log("Response", r)
		})
	}
})
