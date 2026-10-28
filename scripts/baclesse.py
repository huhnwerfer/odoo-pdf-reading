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


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_no_string] = self.get_text(0, 1, line_text)
		dict_line[self.prod_des_string] = re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += " " + self.line_array[self.line_array_pos+i]
			pass
		dict_line[self.quantity_string] = self.get_text(0, 3, line_text)
		dict_line[self.unit_price_string] = self.get_text(0, 4, line_text)
		dict_line[self.total_string] = self.get_text(0, 5, line_text)
		dict_line[self.discount_string] = "0.00 (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"Baclesse", pdf_text)


	def get_order_id(self, pdf_text) -> str:
		order_id = re.search(r"N° de la commande : (.*) PLURISELECT", pdf_text).group(0)
		order_id = re.sub(r"N° de la commande : (.*) PLURISELECT", r"\1", order_id)
		return order_id
