import re
class PDF:
	format_lines_until_pattern = None
	delete_lines_until_pattern = None
	regex_array = []

	def __init__(self, line_array: list[str]):
		self.line_array: list[str] = line_array
		self.dict_array = []
		self.line_array_pos = 0
		self.new_string = {}
		self.line_jumper = 1

		self.prod_no_string = "Product Number"
		self.quantity_string = "Quantity"
		self.discount_string = "Discount"
		self.prod_des_string = "Product Description"
		self.u_o_m_string = "U O M"
		self.unit_price_string = "Unit Price"
		self.total_string = "Total"
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
		raise Exception(f"{self.__class__.__name__}: Function csv_line is not implemented (pls implement prod_no, quantity_string, discount and prod_des)")


	def count_lines(self):
		self.line_jumper = 1
		while not (re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos + self.line_jumper]) or re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos + self.line_jumper])):
			self.line_jumper += 1
			pass
		pass


	def get_text(self, regex_array_pos: int, capture_group: int, regex_text_or_pos) -> str:
		if isinstance(regex_text_or_pos, int):
			return re.sub(self.regex_array[regex_array_pos], fr"\{capture_group}", self.line_array[self.line_array_pos + regex_text_or_pos])
		return re.sub(self.regex_array[regex_array_pos], fr"\{capture_group}", regex_text_or_pos)


	def delete_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return


	def format_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.count_lines()
			self.dict_array.append(self.csv_line())
			self.line_array_pos += self.line_jumper
			self.line_jumper = 1
			pass
		return


	def is_correct_firm(self, pdf_text):
		raise Exception(f"In {self.__class__.__name__} function is_correct_firm is not implemented")


	def get_order_id(self, pdf_text) -> str:
		raise Exception(f"In {self.__class__.__name__} function get_order_id is not implemented")
		order_id = re.sub(r".*(.*)", r"\1", pdf_text)
		return order_id
