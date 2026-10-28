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


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_no_string] = self.get_text(0, 1, line_text)
		dict_line[self.quantity_string] = self.get_text(0, 3, line_text)
		dict_line[self.u_o_m_string] = self.get_text(0, 4, line_text)
		dict_line[self.unit_price_string] = self.get_text(0, 5, line_text)
		dict_line[self.prod_des_string] = ""
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i]) + " "
			pass
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def prod_des(self) -> str:
		prod_string = ""
		for i in range(1, self.line_jumper):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos + i])
		return prod_string


	def is_correct_firm(self, pdf_text):
		return re.search(r"CENTRE HOSPITALIER UNIVERSITAIRE", pdf_text)
