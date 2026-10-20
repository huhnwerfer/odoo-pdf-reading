import re
from .__base__ import PDF


class GEYER(PDF):
	delete_lines_until_pattern = r"(^\d{2,} \d{6,})"
	format_lines_until_pattern = r"Nettosumme"
	#10 12646182 3Pack (à 50 Stück) 65,03 195,09
	#Lieferanten-Artnr: 43-10040-50
	#pluriStrainer Mini, 40µm, 50pcs, 25pcs sterile in bag
	#Liefertermin: 22.09.26
	regex_array = [r"\d{2,} \d{6,} (\d)\w*.* (\d*,\d*) (\d*,\d*)", r".*: (\d{2}-\d{5}-(\d{2})?)", r"(.*)"]


	def quantity(self) -> str:
		quant = float(re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos]).replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def prod_no(self) -> str:
		return re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+1])


	def prod_des(self) -> str:
		prod_string = ""
		for i in range(2, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[2], r"\1", self.line_array[self.line_array_pos+i])
		return prod_string


	def is_correct_firm(self, pdf_text):
		return re.search(r"Geyer", pdf_text)
