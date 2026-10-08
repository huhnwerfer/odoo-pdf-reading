import re
from .pdf import PDF


class ONCOLOGIA(PDF):
	delete_lines_until_pattern = r"\d* (\d{6}) \d* (\d+) .* (\d*,\d*) (\d*,\d*)"
	format_lines_until_pattern = r"__+|Total"
	# 010 213362 212496 1 Pcs 340,73 340,73
	# Streck - Cyto-Chex® BCT (1 PAK, (5 ml, 25 Röhrchen,
	# CE-IVD))
	regex_array = [r"\d* (\d{6}) \d* (\d+) .* (\d*,\d*) (\d*,\d*)", r"(.*)"]

	def format_array_to_csv(self):
		while self.line_array_pos < len(self.line_array):
			self.delete_lines_until_()
			self.format_lines_until_()
		return self.csv_array


	def delete_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return


	def format_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.csv_array.append(self.csv_line())
			self.line_array_pos += self.line_jumper
			self.line_jumper = 1
			pass


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
