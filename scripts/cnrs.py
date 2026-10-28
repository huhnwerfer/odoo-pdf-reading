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


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_des_string] = self.get_text(0, 1, line_text)
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += " " + self.get_text(1, 1, self.line_array[self.line_array_pos+i])
		dict_line[self.prod_no_string] = self.get_text(0, 2, line_text)
		dict_line[self.quantity_string] = float(self.get_text(0, 4, line_text).replace(",", "."))
		if dict_line[self.quantity_string].is_integer():
			dict_line[self.quantity_string] = str(int(dict_line[self.quantity_string]))
		dict_line[self.unit_price_string] = self.get_text(0, 5, line_text)
		dict_line[self.total_string] = self.get_text(0, 6, line_text)
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"CNRS", pdf_text)


	def get_order_id(self, pdf_text) -> str:
		order_id = re.search(r"N° COM : (.*).*", pdf_text).group(0)
		order_id = re.sub(r"N° COM : (.*?)( |$).*", r"\1", order_id)
		return order_id
