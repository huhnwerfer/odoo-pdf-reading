import re
from os import write

from .__base__ import PDF


class CBPLU(PDF):
	delete_lines_until_pattern = r"\d{2}-\d{5}-\d{2}"
	format_lines_until_pattern = r"Total\d*(,|.)\d*"
	# Product No. Product Description U O M Quantity Unit Price Total

	# 42-50000-03 PLU pluriStrainer Funnel, pluriStrainer accessories 25 1 40.30 40.30
	# 25pc with the same LOT. PC EUR
	regex_array = [r"(\d{2}-\d{5}-\d{2}) PLU (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"(.*) ?((PC)|(ML))( EUR)"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_no_string] = self.get_text(0, 1, 0)
		dict_line[self.prod_des_string] = self.get_text(0, 2, 0)
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += " " + self.get_text(1, 1, i)
			pass
		dict_line[self.u_o_m_string] = self.get_text(0, 3, 0) + " " + self.get_text(1, 2, 1)
		dict_line[self.quantity_string] = float(self.get_text(0, 4, 0).replace(",", "."))
		if dict_line[self.quantity_string].is_integer():
			dict_line[self.quantity_string] = str(int(dict_line[self.quantity_string]))
		dict_line[self.unit_price_string] = self.get_text(0, 5, 0)
		dict_line[self.total_string] = self.get_text(0, 6, 0)
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"CBPLU", pdf_text)
