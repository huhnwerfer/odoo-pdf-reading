import re
class PDF:
	test = None
	format_lines_until_pattern = None
	delete_lines_until_pattern = None
	regex_array = None
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
		if cls.format_lines_until_pattern is None:
			error_string += f"{cls.__name__} muss format_lines_until_pattern definieren\n"
			pass

		if cls.delete_lines_until_pattern is None:
			error_string += f"{cls.__name__} muss delete_lines_until_pattern definieren\n"
			pass

		if cls.regex_array is None:
			error_string += f"{cls.__name__} muss regex_array definieren\n"
			pass

		if error_string:
			raise TypeError(error_string)




	def csv_line(self) -> str:
		self.count_lines()
		csv_string = ""
		csv_string += self.prod_no() + "\t"
		csv_string += self.prod_des() + "\t"
		csv_string += self.u_o_m() + "\t"
		csv_string += self.quantity() + "\t"
		csv_string += self.unit_price() + "\t"
		csv_string += self.total() + "\t"
		return csv_string[:-1] + "\n"


	def count_lines(self):
		self.line_jumper = 1
		while not (re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos + self.line_jumper]) or re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos + self.line_jumper])):
			self.line_jumper += 1


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

