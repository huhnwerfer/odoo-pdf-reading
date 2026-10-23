import re
from .__base__ import PDF


class MIDT(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}(-\d{2})?)"
	format_lines_until_pattern = r"Samlet værdi"
	# Pos. Varenr. Betegnelse Lev.-varerenr.
	# Leveringsdato/ Mængde Enhed Pris pr. enhed Nettoværdi
	# Udførelsesperiode

	# 1 pluristrainer mini 70um 43-10070-70
	# 25.09.2026 2 PK 4.460,00 DKK/1 PK 8.920,00 DKK
	# Positionslangtekst:
	# pluristrainer mini 70um
	regex_array = [r"\d (.*) (\d{2}-\d{5}(-\d{2})?)", r"\d{2}\.\d{2}\.\d{4} (\d+) PK(.*) ((\d*\.)*\d*,\d*) .* ((\d*\.)*\d*,\d*).*", r".*\: *(.*)", r"(.*)"]


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])
		prod_string += " " + re.sub(self.regex_array[1], r"\2", self.line_array[self.line_array_pos + 1])
		prod_string += " " + re.sub(self.regex_array[2], r"\1", self.line_array[self.line_array_pos + 2])
		return prod_string


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])


	def quantity(self) -> str:
		quant = float(re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos + 1]))#.replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)


	def unit_price(self) -> str:
		return re.sub(self.regex_array[1], r"\3", self.line_array[self.line_array_pos + 1])


	def total(self) -> str:
		return re.sub(self.regex_array[1], r"\5", self.line_array[self.line_array_pos + 1])


	def discount(self) -> str:
		return "0.00% (no field given)"


	def is_correct_firm(self, pdf_text):
		return re.search(r"MAJBRITH DALGAARD", pdf_text)
