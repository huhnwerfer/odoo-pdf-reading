import re
from .__base__ import PDF


class DOMINIQUE(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)|(^\d{6} )"
	format_lines_until_pattern = r"(Please confirm this)|(Total)"
	# Your Part n° Description Our Part n° Quantity Unit price Discount Total Delivery Date
	# dd/mm/yyyy
	# France - RFE : adresse de facturation électronique : 325204725_AC
	# Hors France : Please send invoice to : invoice.dd@dutscher.com

	# 43-50020-03 PLURISTRAINER 20µm x25 149019 2 57,0000 114,00
	regex_array = [r"(\d{2}-\d{5}-(\d{2})?|\d{6}) (.*) \d{5,}\w* (\d+) (\d*,\d*) ?(.*) (\d*,\d*).*", r"(.*)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
		return prod_string


	def quantity(self) -> str:
		quant = float(re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos]).replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def discount(self) -> str:
		discount_string = ""
		discount_string += re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])
		if discount_string == "":
			return "0.00% (no discount found)"
		return discount_string


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\7", self.line_array[self.line_array_pos])


	def is_correct_firm(self, pdf_text):
		return re.search(r"Dominique", pdf_text)
