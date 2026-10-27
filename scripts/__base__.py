import re
class PDF:
	format_lines_until_pattern = None
	delete_lines_until_pattern = None
	regex_array = None

	def __init__(self, line_array: list):
		self.line_array = line_array
		self.dict_array = []
		self.line_array_pos = 0
		self.new_string = {}
		self.line_jumper = 1

		self.prod_no = ""
		self.quantity = ""
		self.discount = ""
		self.prod_des = ""
		self.u_o_m = ""
		self.unit_price = ""
		self.total = ""
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


	def csv_line(self) -> dict:
		dict_line = {}
		self.count_lines()
		self.write_vars()
		dict_line["Product Number"] = self.prod_no
		dict_line["Quantity"] = self.quantity
		dict_line["Discount"] = self.discount
		dict_line["Product Description"] = self.prod_des
		dict_line["U O M"] = self.u_o_m
		dict_line["Unit Price"] = self.unit_price
		dict_line["Total"] = self.total
		return dict_line


	def count_lines(self):
		self.line_jumper = 1
		while not (re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos + self.line_jumper]) or re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos + self.line_jumper])):
			self.line_jumper += 1
			pass
		pass


	def write_vars(self):
		raise Exception(f"{self.__class__.__name__}: Function write_vars is not implemented (pls implement prod_no, quantity, discount and prod_des)")


	def prod_no(self) -> str:
		raise Exception(f"{self.__class__.__name__}: Function prod_no is not implemented")
		return ""


	def quantity(self) -> str:
		raise Exception(f"{self.__class__.__name__}: Function quantity is not implemented")
		return ""


	def discount(self) -> str:
		raise Exception(f"{self.__class__.__name__}: Function discount is not implemented")
		return ""


	def prod_des(self) -> str:
		raise Exception(f"{self.__class__.__name__}: Function prod_des is not implemented")
		return ""


	def u_o_m(self) -> str:
		return ""


	def unit_price(self) -> str:
		return ""


	def total(self) -> str:
		return ""


	def delete_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return


	def format_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.dict_array.append(self.csv_line())
			#self.csv_array.append(self.csv_line())     anstelle von dieser zeile iwie das dict zum dict_array appenden
			self.line_array_pos += self.line_jumper
			self.line_jumper = 1
			pass
		return


	def format_array_to_csv(self):
		while self.line_array_pos < len(self.line_array):
			self.delete_lines_until_()
			self.format_lines_until_()
		return self.csv_array


	def is_correct_firm(self, pdf_text):
		raise Exception(f"In {self.__class__.__name__} function is_correct_firm is not implemented")
