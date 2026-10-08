import re
from .pdf import PDF


class CNRS(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)"
	format_lines_until_pattern = r"Acronyme"
	#EQ4_FE ÜberStrainer laboratory 06/08/2025 43-70005-03 1,00 126,00 0.0 126,00
	regex_array = [r".+? (.*) \d{2}/\d{2}/\d{4} (\d{2}-\d{5}-(\d{2})?) (\d+,\d*) (\d*,\d*) \d*\.\d* (\d*,\d*)", r"(.*)"]

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


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
		return prod_string


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])


	def quantity(self) -> str:
		quant = float(re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos]).replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def u_o_m(self) -> str:
		return ""
