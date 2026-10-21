import re
from .__base__ import PDF


class CENTRE_HOSPITALIER(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)"
	format_lines_until_pattern = r"Montant TTC"
	#E4015194 REF. 46-10003-15 1 UN 20,000000
	regex_array = [r".* (\d{2}-\d{5}-(\d{2})?) (\d+) .* (\d*,\d*)", r"(.*)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		for i in range(1, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos + i])
		return prod_string


	def total(self) -> str:
		return ""


	def u_o_m(self) -> str:
		return ""


	def is_correct_firm(self, pdf_text):
		return re.search(r"CENTRE HOSPITALIER UNIVERSITAIRE", pdf_text)
