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


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_no_string] = self.get_text(0, 1, line_text)
		dict_line[self.prod_des_string] = self.get_text(0, 3, line_text)
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
			pass
		dict_line[self.quantity_string] = float(self.get_text(0, 4, line_text).replace(",", "."))
		if dict_line[self.quantity_string].is_integer():
			dict_line[self.quantity_string] = str(int(dict_line[self.quantity_string]))
		dict_line[self.unit_price_string] = self.get_text(0, 5, line_text)
		dict_line[self.discount_string] = self.get_text(0, 6, line_text)
		if dict_line[self.discount_string] == "":
			dict_line[self.discount_string] = "0.00% (no discount found)"
		dict_line[self.total_string] = self.get_text(0, 7, line_text)
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"Dominique", pdf_text)
