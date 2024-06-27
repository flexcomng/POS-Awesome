# Copyright (c) 2024, Youssef Restom and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class MarkdownOptions(Document):
	def autoname(self):
		self.name = self.markdown_option

