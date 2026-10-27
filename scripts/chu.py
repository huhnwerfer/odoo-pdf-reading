import re
from .__base__ import PDF


class CHU(PDF):
	delete_lines_until_pattern = r"\d \d{7}"
	format_lines_until_pattern = r"-----------------------------------"
	# 1 3384656 H 6022401 2 BOITE 1243,00 2 486,0C
	# STRECK CYTO-CHEX BCT TUBES SML Xl00
	# PLATili[[UM
	# 213386
	# Devis 25132817
	regex_array = [r"\d+ \d{7}.*\d{7} (\d+).* (\d+,\d+) ?(.*) (\d*) (\d+,\d+).*", r"(.*)", r"(^(\d{6})|(\d{2}-\d{5}(-\d{2})?))"]


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])


	def discount(self) -> str:
		discount_string = ""
		discount_string += re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])
		if discount_string == "":
			return "0.00% (no discount found)"
		return discount_string


	def total(self) -> str:
		total_string = ""
		total_string += re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])
		total_string += re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])
		return total_string


	def prod_des(self) -> str:
		prod_string = ""
		for i in range(1, self.line_jumper-2):
			prod_string += re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos + i]) + " "
		return prod_string


	def prod_no(self) -> str:
		return re.sub(self.regex_array[2], r"\1", self.line_array[self.line_array_pos+self.line_jumper-2])


	def is_correct_firm(self, pdf_text):
		return re.search(r"C\.H\.U\. LIMOGES|CHU Limoges", pdf_text)



