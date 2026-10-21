import re
from .__base__ import PDF


class CBPLU(PDF):
	delete_lines_until_pattern = r"\d{2}-\d{5}-\d{2}"
	format_lines_until_pattern = r"Total\d*(,|.)\d*"
	# Product No. Product Description U O M Quantity Unit Price Total

	# 42-50000-03 PLU pluriStrainer Funnel, pluriStrainer accessories 25 1 40.30 40.30
	# 25pc with the same LOT. PC EUR
	regex_array = [r"(\d{2}-\d{5}-\d{2}) PLU (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"(.*)(( *PC)|(ML))( EUR)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_des_str = ""
		prod_des_str += re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_des_str += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
		return prod_des_str


	def u_o_m(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos]) + " " + re.sub(self.regex_array[1], r"\2", self.line_array[self.line_array_pos+1])


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def discount(self) -> str:
		return "0.00% (no field given)"


	def is_correct_firm(self, pdf_text):
		return re.search(r"CBPLU", pdf_text)
