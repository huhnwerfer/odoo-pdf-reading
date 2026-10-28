import re
from .__base__ import PDF


class OSLO(PDF):
	delete_lines_until_pattern = r"\d* (.*).* \d{1,2}-\w{2,4}-\d{1,2} (\d*),\d*.* ((\d* ?\d*)*,\d*) ((\d* ?\d*)*,\d*)"
	format_lines_until_pattern = r"Totalt"
	# 1 pluriStrainer Mini 70 23-SEP-26 2,00 STK STK 819,00 1 638,00
	# µm
	# 43-10070-50
	regex_array = [r"\d* (.*).* \d{1,2}-\w{2,4}-\d{1,2} (\d*),\d*.* ((\d* ?\d*)*,\d*) ((\d* ?\d*)*,\d*)", r"(.*)", r"(\d{2}-\d{5}(-\d{2})?)"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_des_string] = self.get_text(0, 1, 0)
		for i in range(1, self.line_jumper - 1):
			dict_line[self.prod_des_string] += " " + self.get_text(1, 1, i)
			pass
		dict_line[self.quantity_string] = float(self.get_text(0, 2, 0).replace(",", "."))
		if dict_line[self.quantity_string].is_integer():
			dict_line[self.quantity_string] = str(int(dict_line[self.quantity_string]))
		dict_line[self.unit_price_string] = self.get_text(0, 3, 0)
		dict_line[self.total_string] = self.get_text(0, 5, 0)
		dict_line[self.prod_no_string] = self.get_text(2, 1, self.line_jumper - 1)
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"OSLO", pdf_text)


	def get_order_id(self, pdf_text) -> str:
		order_id = re.search(r"Order (\S+)", pdf_text).group(1)
		return order_id
