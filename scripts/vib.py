import re
from .__base__ import PDF


class VIB(PDF):
	delete_lines_until_pattern = r"\d{2}-\d{5}(-\d{2})?"
	format_lines_until_pattern = r"Total"
	# 10 44-10050-05 plurimate II 50 ml tubes (unfilled) 25 pieces 4.00 54.00 0.00% 216.00
	# (Project: 1001391 Group: 1184 Requester: Van Gompel Jan)
	regex_array = [r"\d* (\d{2}-\d{5}(-\d{2})?) (.*) (\d*.\d*) (\d*.\d*) .* (\d*.\d*)", r"(.*)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])

	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos + i])
		return prod_string

	def quantity(self) -> str:
		quant = float(re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos]).replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)

	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])

	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def is_correct_firm(self, pdf_text):
		return re.search(r"VIB", pdf_text)
