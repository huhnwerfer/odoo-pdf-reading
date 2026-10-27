import re
from .__base__ import PDF


class CAMBRIDGE(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)"
	format_lines_until_pattern = r"Deliver To"
	# Qty	Catalogue No.	Description	Requested Date	Unit Price	Disc %	Total Price
	# 1 43-10020-50 pluriStrainer Mini Cell Strainer, pore size 20 um 25/09/2026 59.50 0.00 59.50
	# 1 PAK
	regex_array = [r"(\d+) (\d{2}-\d{5}-(\d{2})?) (.*) \d{2}/\d{2}/\d{4} (\d*\.\d*) (\d*\.\d*) (\d*\.\d*)", r"(.*)"]


	def write_vars(self):
		self.quantity = re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])
		self.prod_no = re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])
		self.prod_des = re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			self.prod_des += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
			pass
		self.unit_price = re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])
		self.discount = re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])
		self.total = re.sub(self.regex_array[0], r"\7", self.line_array[self.line_array_pos])




	def is_correct_firm(self, pdf_text):
		return re.search(r"Cambridge", pdf_text) is not None
