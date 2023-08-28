# Copyright (c) 2023, techno lead llc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from frappe.utils import formatdate

class CompanyLoanManagement(Document):
	def validate(self):
		self.loan()

	
	def loan(self):
		if self.number_of_installment:
			numbers = self.number_of_installment
			self.repayment = []
			months_to_add = 1
			start_date = datetime.strptime(self.first_installment_date, '%Y-%m-%d')
			new_date = start_date - relativedelta(months=months_to_add)
			for a in range(numbers):
				row = self.append("repayment",{})
				new_date = new_date + relativedelta(months=months_to_add)
				row.date = new_date
				row.interest = self.interest_amount / numbers
				row.amount = self.amount / numbers
				row.total = row.interest + row.amount
				row.add_jv = "Add JV"


@frappe.whitelist()
def create_journal_entries(**args):
	a = 5
	credit = args.get('credit')
	debit = args.get('debit')
	interest = args.get('interest')
	date = args.get('start_date')
	c_date = datetime.strptime(date, "%Y-%m-%d")
	total = args.get('total')
	intrest_total = float(total) * 2
	reference_number = "HASJDG123I2GJEH"
	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Journal Entry"
	je.posting_date = c_date
	je.cheque_no = reference_number
	je.cheque_date = c_date
	je.append(
		"accounts",
			{
				"account": interest,
				"credit_in_account_currency": intrest_total
			},
		)
	je.append(
		"accounts",
			{
				"account": credit,
				"debit_in_account_currency": total
			},
		)
	je.append(
		"accounts",
			{
				"account":debit,
				"debit_in_account_currency": total
			},
		)
	je.save()
	return "ok"

@frappe.whitelist()
def loan_journal_entries(**args):
	credit = args.get('credit')
	debit = args.get('debit')
	date = args.get('start_date')
	c_date = datetime.strptime(date, "%Y-%m-%d")
	total = args.get('total')
	reference_number = "HASJDG123I2GJEH"
	je = frappe.new_doc("Journal Entry")
	je.voucher_type = "Journal Entry"
	je.posting_date = c_date
	je.cheque_no = reference_number
	je.cheque_date = c_date
	je.append(
		"accounts",
			{
				"account": debit,
				"debit_in_account_currency": total
			},
		)
	je.append(
		"accounts",
			{
				"account": credit,
				"credit_in_account_currency": total
			},
		)
	je.save()
	return "ok"
