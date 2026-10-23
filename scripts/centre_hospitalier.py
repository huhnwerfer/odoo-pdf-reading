import re
from .__base__ import PDF


class CENTRE_HOSPITALIER(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)"
	format_lines_until_pattern = r"Montant TTC"
	# CODE QUANTITE PRIX
	# INTERNE DESIGNATION MARCHE COMMANDEE UNITE UNITAIRE H.T.

	# E4015194 REF. 46-10003-15 1 UN 20,000000
	# PLURISTRAINER MINI MEMBRAN,taille des
	# pores 3 µm (1 PAK, 5 pc, stérile)
	# + 20.00 euros frais de port
	# Ref EDI (Autre):0
	# Pt. dist : 3026140138882 - BOC/BS/S/RJ/P
	# L28/ED47
	regex_array = [r".* (\d{2}-\d{5}-(\d{2})?) (\d+) (.*) (\d*,\d*)", r"(.*)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def u_o_m(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		for i in range(1, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos + i])
		return prod_string


	def total(self) -> str:
		return ""


	def discount(self) -> str:
		return "0.00% (no field given)"


	def is_correct_firm(self, pdf_text):
		return re.search(r"CENTRE HOSPITALIER UNIVERSITAIRE", pdf_text)
