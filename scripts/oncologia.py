import re
from .__base__ import PDF


class ONCOLOGIA(PDF):
	delete_lines_until_pattern = r"\d* (\d{6}) \d* (\d+) .* (\d*,\d*) (\d*,\d*)"
	format_lines_until_pattern = r"__+|Total"
	# L_in_e__Y_o_ur_ C_o_de_/D_es_c_rip_tio_n_____O_u_r C_o_de________________Q_ua_n_tity___________U_ni_t P_r._____T_ot_al_ P_ric_e____

	# 010 213362 212496 1 Pcs 340,73 340,73
	# Streck - Cyto-Chex® BCT (1 PAK, (5 ml, 25 Röhrchen,
	# CE-IVD))
	regex_array = [r"\d* (\d{6}) \d* (\d+) .* (\d*,\d*) (\d*,\d*)", r"(.*)"]


	def csv_line(self) -> dict:
		dict_line = {}
		line_text = self.line_array[self.line_array_pos]
		dict_line[self.prod_no_string] = self.get_text(0, 1, 0)
		dict_line[self.quantity_string] = float(self.get_text(0, 2, 0).replace(",", "."))
		if dict_line[self.quantity_string].is_integer():
			dict_line[self.quantity_string] = str(int(dict_line[self.quantity_string]))
			pass
		dict_line[self.unit_price_string] = self.get_text(0, 3, 0)
		dict_line[self.total_string] = self.get_text(0, 4, 0)
		dict_line[self.prod_des_string] = ""
		for i in range(1, self.line_jumper):
			dict_line[self.prod_des_string] += self.get_text(1, 1, i) + " "
			pass
		dict_line[self.discount_string] = "0.00% (no field given)"
		return dict_line


	def is_correct_firm(self, pdf_text):
		return re.search(r"ONCOLOGIA", pdf_text)
