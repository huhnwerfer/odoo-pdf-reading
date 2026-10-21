import re
from .__base__ import PDF


class ONCOLOGIA(PDF):
	delete_lines_until_pattern = r"\d* (\d{6}) \d* (\d+) .* (\d*,\d*) (\d*,\d*)"
	format_lines_until_pattern = r"__+|Total"
	# 010 213362 212496 1 Pcs 340,73 340,73
	# Streck - Cyto-Chex® BCT (1 PAK, (5 ml, 25 Röhrchen,
	# CE-IVD))
	regex_array = [r"\d* (\d{6}) \d* (\d+) .* (\d*,\d*) (\d*,\d*)", r"(.*)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def quantity(self) -> str:
		quant = float(re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos]).replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		for i in range(1, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
		return prod_string


	def is_correct_firm(self, pdf_text):
		return re.search(r"ONCOLOGIA", pdf_text)
