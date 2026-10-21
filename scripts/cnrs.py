import re
from .__base__ import PDF


class CNRS(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)"
	format_lines_until_pattern = r"Acronyme"
	# EDP Désignation du matériel Date livr. Réf. Article Qté P.U. H.T. Taux Prix H.T.
	# Rem.

	# EQ4_FE ÜberStrainer laboratory 06/08/2025 43-70005-03 1,00 126,00 0.0 126,00
	# filter, pore size 5 m (1 PAK,
	# 10 pc, sterile)
	# N° de devis : 25133923
	# Acronyme : OPTI-STEM Fonds : 1 Ori. : EQ4-OPTIST AGD : AGDI_254219_01_3629_2022 Dom. Fonc : A1INSB
	regex_array = [r".+? (.*) \d{2}/\d{2}/\d{4} (\d{2}-\d{5}-(\d{2})?) (\d+,\d*) (\d*,\d*) \d*\.\d* (\d*,\d*)", r"(.*)"]


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


	def discount(self) -> str:
		return "0.00% (no field given)"


	def is_correct_firm(self, pdf_text):
		return re.search(r"CNRS", pdf_text)
