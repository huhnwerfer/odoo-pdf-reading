import re
from .__base__ import PDF


class CHU(PDF):
	delete_lines_until_pattern = r"\d \d{7}"
	format_lines_until_pattern = r"-----------------------------------"
	# 1 3384656 H 6022401 2 BOITE 1243,00 2 486,0C
	# STRECK CYTO-CHEX BCT TUBES SML Xl00
	# PLATili[[UM
	# 213386
	# Devis 25132817
	regex_array = [r"\d+ \d{7}.*\d{7} (\d+).* (\d+,\d+) ?(.*) (\d*) (\d+,\d+).*", r"(.*)", r"(^(\d{6})|(\d{2}-\d{5}(-\d{2})?))"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.quantity_string] = self.get_text(0, 1, line_text)
		dict_line[self.unit_price_string] = self.get_text(0, 2, line_text)
		dict_line[self.discount_string] = self.get_text(0, 3, line_text)
		if dict_line[self.discount_string] == "":
			dict_line[self.discount_string] = "0.00% (no discount found)"
		dict_line[self.total_string] = self.get_text(0, 4, line_text) + self.get_text(0, 5, line_text)
		dict_line[self.prod_des_string] = ""
		for i in range(1, self.line_jumper-2):
			dict_line[self.prod_des_string] += re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i]) + " "
			pass
		dict_line[self.prod_no_string] = self.get_text(2, 1, self.line_array[self.line_array_pos+self.line_jumper-2])
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"C\.H\.U\. LIMOGES|CHU Limoges", pdf_text)


	def get_order_id(self, pdf_text) -> str:
		order_id = re.search(r"N°d'engagement: ?(.*)", pdf_text).group(0)
		order_id = re.sub(r"N°d'engagement: ?(.*)", r"\1", order_id)
		return order_id
