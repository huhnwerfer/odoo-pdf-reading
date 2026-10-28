import re
from .__base__ import PDF


class CAMBRIDGE(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)"
	format_lines_until_pattern = r"Deliver To"
	# Qty	Catalogue No.	Description	Requested Date	Unit Price	Disc %	Total Price
	# 1 43-10020-50 pluriStrainer Mini Cell Strainer, pore size 20 um 25/09/2026 59.50 0.00 59.50
	# 1 PAK
	regex_array = [r"(\d+) (\d{2}-\d{5}-(\d{2})?) (.*) \d{2}/\d{2}/\d{4} (\d*\.\d*) (\d*\.\d*) (\d*\.\d*)", r"(.*)"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.quantity_string] = self.get_text(0, 1, line_text)
		dict_line[self.prod_no_string] = self.get_text(0, 2, line_text)
		dict_line[self.prod_des_string] = re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
			pass
		dict_line[self.unit_price_string] = self.get_text(0, 5, line_text)
		dict_line[self.discount_string] = self.get_text(0, 6, line_text)
		dict_line[self.total_string] = self.get_text(0, 7, line_text)
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"Cambridge", pdf_text) is not None


	def get_order_id(self, pdf_text) -> str:
		order_id = re.search(r"Order No\. (.*)", pdf_text).group(0)
		order_id = re.sub(r"Order No\. (.*)", r"\1", order_id)
		return order_id
