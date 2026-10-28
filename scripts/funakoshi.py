import re
from .__base__ import PDF


class FUNAKOSHI(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}(-\d{2})?)"
	format_lines_until_pattern = r"((CONTINUED)|(Total))|(SPECIAL INSTRUCTIONS: EUR)"
	# Product No. Catalog No. Description Unit Size Quantity ( E U R ) Amount
	# PLS700810 43-50010-03 pluriStrainer 10μm, Sterile 25 5 57.00 285.00
	# pcs
	regex_array = [r".*(\d{2}-\d{5}(-\d{2}){0,1}) (.*) (\d+) (\d+) (\d+\.\d+) (\d+\.\d+)", r"(.*) ()"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_no_string] = self.get_text(0, 1, line_text)
		dict_line[self.prod_des_string] = self.get_text(0, 3, line_text)
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += "".join(re.findall(r"^(?!(?:ml|pkg|pc|pcs)$).*", self.line_array[self.line_array_pos+i]))
			pass
		dict_line[self.u_o_m_string] = self.get_text(0, 4, line_text)
		dict_line[self.quantity_string] = self.get_text(0, 5, line_text)
		dict_line[self.unit_price_string] = self.get_text(0, 6, line_text)
		dict_line[self.total_string] = self.get_text(0, 7, line_text)
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"Funakoshi", pdf_text)


	def get_order_id(self, pdf_text) -> str:
		order_id = re.search(r"No\.\s*(\S+)", pdf_text).group(1)
		return order_id
