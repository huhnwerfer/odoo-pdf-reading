class PDF:
	def __init__(self, line_array: list):
		self.line_array = line_array
		self.csv_array = []
		self.csv_array.append("Product Number" + "\t" + "Product Description" + "\t" + "U O M" + "\t" + "Quantity" + "\t" + "Unit Price" + "\t" + "Total" + "\n")
		self.line_array_pos = 0
		self.new_string = {}
		self.line_jumper = 1
		pass


	def csv_line(self, regex_array) -> str:
		csv_string = ""
		csv_string += self.prod_no(regex_array) + "\t"
		csv_string += self.prod_des(regex_array) + "\t"
		csv_string += self.u_o_m(regex_array) + "\t"
		csv_string += self.quantity(regex_array) + "\t"
		csv_string += self.unit_price(regex_array) + "\t"
		csv_string += self.total(regex_array) + "\t"
		return csv_string[:-1] + "\n"


	def prod_no(self, regex_array) -> str:
		raise Exception("Function prod_no is not implemented")
		return ""


	def prod_des(self, regex_array) -> str:
		raise Exception("Function prod_des is not implemented")
		return ""


	def u_o_m(self, regex_array) -> str:
		raise Exception("Function u_o_m is not implemented")
		return ""


	def quantity(self, regex_array) -> str:
		raise Exception("Function quantity is not implemented")
		return ""


	def unit_price(self, regex_array) -> str:
		raise Exception("Function unit_price is not implemented")
		return ""


	def total(self, regex_array) -> str:
		raise Exception("Function total is not implemented")
		return ""


	def delete_lines_until_(self):
		raise Exception("Function delete_lines_untill_prod_no is not implemented")


	def format_lines_until_(self):
		raise Exception("Function format_lines_untill_totall is not implemented")


	def format_array_to_csv(self):
		raise Exception("Function format_array_to_csv is not implemented")

