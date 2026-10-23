import re
from .__base__ import PDF


class PLURISELECTUSA(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}(-\d{2})?)|(\d*\.\d*) (\d*\.\d*)"
	format_lines_until_pattern = r"Total"
	# Item Description Qty U/M Rate Amount

	# 60-00051-09 10x RBC Lysis Buffer SAMPLE 1 0.00 0.00
	regex_array = [r"(\d{2}-\d{5}-\d{2}) (.*) (\d*)(.*) (\d*\.\d*) (\d*\.\d*)", r"(.*)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_string += " " + self.line_array[self.line_array_pos+1]
		return prod_string


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def u_o_m(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def discount(self) -> str:
		return "0.00% (no field given)"


	def is_correct_firm(self, pdf_text):
		return re.search(r"Pluriselect-USA", pdf_text)
