import re
from .__base__ import PDF


class VIB(PDF):
	delete_lines_until_pattern = r"\d{2}-\d{5}(-\d{2})?"
	format_lines_until_pattern = r"Total"
	# 10 44-10050-05 plurimate II 50 ml tubes (unfilled) 25 pieces 4.00 54.00 0.00% 216.00
	# (Project: 1001391 Group: 1184 Requester: Van Gompel Jan)
	regex_array = [r"\d* (\d{2}-\d{5}(-\d{2})?) (.*) (\d*.\d*) (\d*.\d*) (\d+\.\d+%) (\d*.\d*)", r"(.*)"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_no_string] = self.get_text(0, 1, 0)
		dict_line[self.prod_des_string] = self.get_text(0, 3, 0)
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += " " + self.get_text(1, 1, i)
			pass
		dict_line[self.quantity_string] = float(self.get_text(0, 4, 0).replace(",", "."))
		if dict_line[self.quantity_string].is_integer():
			dict_line[self.quantity_string] = str(int(dict_line[self.quantity_string]))
		dict_line[self.unit_price_string] = self.get_text(0, 5, 0)
		dict_line[self.discount_string] = self.get_text(0, 6, 0)
		dict_line[self.total_string] = self.get_text(0, 7, 0)
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"VIB", pdf_text)
