import re
from .__base__ import PDF


class BACLESSE(PDF):
	delete_lines_until_pattern = r"(\d*) (.*) (\d{2}-\d{5}-(\{2})?)"
	format_lines_until_pattern = r"Mode livraison : Total"
	# Compte Article Réf. four. Désignation UF Qté PU HT Montant HT Taux CR Projet
	# taxe

	# 60664000 LABO00003 43-50200-03 pluriStrainer 200μm 2174 2 UN 95,000000 190,00EUR 20,00% LP30
	# Motif tarif : Saisie manuelle
	# SELON DEVIS N°2023-424041
	regex_array = [r"\d* .* (\d{2}-\d{5}-\d{0,2}) (.*) \d* (\d*) .* (\d*,\d*) (\d*,\d*)EUR .*", r"(.*)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_string += " " + self.line_array[self.line_array_pos+i]
		return prod_string


	def u_o_m(self) -> str:
		return ""


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def discount(self) -> str:
		return "0.00 (no field given)"


	def is_correct_firm(self, pdf_text):
		return re.search(r"Baclesse", pdf_text)
