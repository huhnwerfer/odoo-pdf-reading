import re
from .__base__ import PDF


class PLURISELECTUSA(PDF):
	delete_lines_until_pattern = r"\d{2}-\d{5}-\d{2}"
	format_lines_until_pattern = r"Total"
	regex_array = [r"(\d{2}-\d{5}-\d{2}) (.*) (\d*)(.*) (\d*\.\d*) (\d*\.\d*)", r"(.*)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def count_lines(self):
		self.line_jumper = 1
		while not (re.search(r"(\d*\.\d*) (\d*\.\d*)", self.line_array[self.line_array_pos + self.line_jumper]) or re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos + self.line_jumper]) or re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos + self.line_jumper])):
			self.line_jumper += 1


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


	def is_correct_firm(self, pdf_text):
		return re.search(r"Pluriselect-USA", pdf_text)
