class PDF:
	def __init__(self, line_array: list):
		self.line_array = line_array
		self.csv_array = []
		self.csv_array.append("Product Number" + "\t" + "Product Description" + "\t" + "U O M" + "\t" + "Quantity" + "\t" + "Unit Price" + "\t" + "Total" + "\n")
		self.line_array_pos = 0
		self.new_string = {}
		self.line_jumper = 1
		pass


	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)

		error_string = ""
		var = "format_lines_until_pattern"
		if var not in cls.__dict__:
			error_string += f"{cls.__name__} muss {var} definieren\n"
			pass

		var = "delete_lines_until_pattern"
		if var not in cls.__dict__:
			error_string += f"{cls.__name__} muss {var} definieren\n"
			pass

		var = "regex_array"
		if var not in cls.__dict__:
			error_string += f"{cls.__name__} muss {var} definieren"
			pass

		if error_string:
			raise TypeError(error_string)




	def csv_line(self) -> str:
		csv_string = ""
		csv_string += self.prod_no() + "\t"
		csv_string += self.prod_des() + "\t"
		csv_string += self.u_o_m() + "\t"
		csv_string += self.quantity() + "\t"
		csv_string += self.unit_price() + "\t"
		csv_string += self.total() + "\t"
		return csv_string[:-1] + "\n"


	def prod_no(self) -> str:
		raise Exception("Function prod_no is not implemented")
		return ""


	def prod_des(self) -> str:
		raise Exception("Function prod_des is not implemented")
		return ""


	def u_o_m(self) -> str:
		return ""


	def quantity(self) -> str:
		raise Exception("Function quantity is not implemented")
		return ""


	def unit_price(self) -> str:
		return ""


	def total(self) -> str:
		return ""


	def delete_lines_until_(self):
		raise Exception("Function delete_lines_untill_prod_no is not implemented")


	def format_lines_until_(self):
		raise Exception("Function format_lines_untill_totall is not implemented")


	def format_array_to_csv(self):
		raise Exception("Function format_array_to_csv is not implemented")

