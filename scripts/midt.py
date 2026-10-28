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


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_des_string] = self.get_text(0, 1, line_text)
		dict_line[self.prod_des_string] += " " + self.get_text(1, 2, self.line_array[self.line_array_pos + 1])
		dict_line[self.prod_des_string] += " " + self.get_text(2, 1, self.line_array[self.line_array_pos + 2])
		dict_line[self.prod_no_string] = self.get_text(0, 2, line_text)
		dict_line[self.quantity_string] = float(self.get_text(1, 1, self.line_array[self.line_array_pos + 1]).replace(",", "."))
		if dict_line[self.quantity_string].is_integer():
			dict_line[self.quantity_string] = str(int(dict_line[self.quantity_string]))
		dict_line[self.unit_price_string] = self.get_text(1, 3, self.line_array[self.line_array_pos + 1])
		dict_line[self.total_string] = self.get_text(1, 5, self.line_array[self.line_array_pos + 1])
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"MAJBRITH DALGAARD", pdf_text)
