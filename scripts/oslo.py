import re
from .__base__ import PDF


class OSLO(PDF):
	delete_lines_until_pattern = r"\d* (.*).* \d{1,2}-\w{2,4}-\d{1,2} (\d*),\d*.* ((\d* ?\d*)*,\d*) ((\d* ?\d*)*,\d*)"
	format_lines_until_pattern = r"Totalt"
	# 1 pluriStrainer Mini 70 23-SEP-26 2,00 STK STK 819,00 1 638,00
	# µm
	# 43-10070-50
	regex_array = [r"\d* (.*).* \d{1,2}-\w{2,4}-\d{1,2} (\d*),\d*.* ((\d* ?\d*)*,\d*) ((\d* ?\d*)*,\d*)", r"(.*)",
	               r"(\d{2}-\d{5}(-\d{2})?)"]


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper - 1):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos + i])
		return prod_string


	def quantity(self) -> str:
		quant = float(re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos]).replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def prod_no(self) -> str:
		return re.sub(self.regex_array[2], r"\1", self.line_array[self.line_array_pos + self.line_jumper - 1])


	def discount(self) -> str:
		return "0.00% (no field given)"


	def is_correct_firm(self, pdf_text):
		return re.search(r"OSLO", pdf_text)
