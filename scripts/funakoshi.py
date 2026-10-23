import re
from .__base__ import PDF


class FUNAKOSHI(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}(-\d{2})?)"
	format_lines_until_pattern = r"((CONTINUED)|(Total))|(SPECIAL INSTRUCTIONS: EUR)"
	# Product No. Catalog No. Description Unit Size Quantity ( E U R ) Amount
	# PLS700810 43-50010-03 pluriStrainer 10μm, Sterile 25 5 57.00 285.00
	# pcs
	regex_array = [r".*(\d{2}-\d{5}(-\d{2}){0,1}) (.*) (\d+) (\d+) (\d+\.\d+) (\d+\.\d+)", r"(.*) ()"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_string += "".join(re.findall(r"^(?!(?:ml|pkg|pc|pcs)$).*", self.line_array[self.line_array_pos+i]))
		return prod_string


	def u_o_m(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\7", self.line_array[self.line_array_pos])


	def discount(self) -> str:
		return "0.00% (no field given)"


	def is_correct_firm(self, pdf_text):
		return re.search(r"Funakoshi", pdf_text)
