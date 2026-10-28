import re
from .__base__ import PDF


class PLURISELECTUSA(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}(-\d{2})?)|(\d*\.\d*) (\d*\.\d*)"
	format_lines_until_pattern = r"Total"
	# Item Description Qty U/M Rate Amount

	# 60-00051-09 10x RBC Lysis Buffer SAMPLE 1 0.00 0.00
	regex_array = [r"(\d{2}-\d{5}(?:-\d{2})?) (.*) (\d*)(.*) (\d*\.\d*) (\d*\.\d*)", r"(.*)"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_no_string] = self.get_text(0, 1, 0)
		dict_line[self.prod_des_string] = self.get_text(0, 2, 0)
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += " " + self.get_text(1, 1, i)
			pass
		dict_line[self.quantity_string] = self.get_text(0, 3, 0)
		dict_line[self.u_o_m_string] = self.get_text(0, 4, 0)
		dict_line[self.unit_price_string] = self.get_text(0, 5, 0)
		dict_line[self.total_string] = self.get_text(0, 6, 0)
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"Pluriselect-USA", pdf_text)


	def get_order_id(self, pdf_text) -> str:
		order_id = re.search(r"\d+/\d+/\d+ (\S+)", pdf_text).group(1)
		return order_id
