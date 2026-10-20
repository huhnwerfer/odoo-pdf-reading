import re
from .__base__ import PDF


class CAMBRIDGE(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)"
	format_lines_until_pattern = r"Deliver To"
	#Qty	Catalogue No.	Description	Requested Date	Unit Price	Disc %	Total Price
	regex_array = [r"(\d+) (\d{2}-\d{5}-(\d{2})?) (.*) \d{2}/\d{2}/\d{4} (\d*\.\d*) \d*\.\d* (\d*\.\d*)", r"(.*)"]


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
		return prod_string


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def u_o_m(self) -> str:
		return ""


	def is_correct_firm(self, pdf_text):
		return re.search(r"Cambridge", pdf_text) is not None
