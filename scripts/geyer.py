import re
from .__base__ import PDF


class GEYER(PDF):
	delete_lines_until_pattern = r"(^\d{2,} \d{6,})"
	format_lines_until_pattern = r"Nettosumme"
	# Pos Artikel Menge Einzelpreis Gesamtpreis
	# EUR EUR

	# 10 12646182 3Pack (à 50 Stück) 65,03 195,09
	# Lieferanten-Artnr: 43-10040-50
	# pluriStrainer Mini, 40µm, 50pcs, 25pcs sterile in bag
	# Liefertermin: 22.09.26
	regex_array = [r"\d{2,} \d{6,} (\d)\w*.* (\d*,\d*) (\d*,\d*)", r".*: (\d{2}-\d{5}-(\d{2})?)", r"(.*)"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.quantity_string] = float(self.get_text(0, 1, line_text).replace(",", "."))
		if dict_line[self.quantity_string].is_integer():
			dict_line[self.quantity_string] = str(int(dict_line[self.quantity_string]))
		dict_line[self.unit_price_string] = self.get_text(0, 2, line_text)
		dict_line[self.total_string] = self.get_text(0, 3, line_text)
		dict_line[self.prod_no_string] = self.get_text(1, 1, self.line_array[self.line_array_pos+1])

		dict_line[self.prod_des_string] = ""
		for i in range(2, self.line_jumper):
			dict_line[self.prod_des_string] += " " + self.get_text(1, 1, self.line_array[self.line_array_pos+i])
			pass
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"Geyer", pdf_text)


	def get_order_id(self, pdf_text) -> str:
		order_id = re.search(r"Bestellung Nr.\s*(\S+)", pdf_text).group(1)
		return order_id
