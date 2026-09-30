import re
from .pdf import PDF


class PLURISELECTUSA(PDF):
	def format_array_to_csv(self):
		while self.line_array_pos < len(self.line_array):
			self.delete_lines_until_()
			self.format_lines_until_()
		return self.csv_array


	def delete_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(r"\d{2}-\d{5}-\d{2}", self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return

	def format_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(r"Total", self.line_array[self.line_array_pos]):
			regex_array = [r"(\d{2}-\d{5}-\d{2}) (.*) (\d*)(.*) (\d*\.\d*) (\d*\.\d*)", r"(.*)"]
			self.csv_array.append(self.csv_line(regex_array))
			self.line_array_pos += self.line_jumper
			self.line_jumper = 1
			pass


	def prod_no(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self, regex_array) -> str:
		prod_string = ""
		prod_string += re.sub(regex_array[0], r"\2", self.line_array[self.line_array_pos])
		if not re.match(r"(\d{2}-\d{5}-\d{2})", self.line_array[self.line_array_pos+1]):
			prod_string += " " + self.line_array[self.line_array_pos+1]
			self.line_jumper = 2
		return prod_string


	def u_o_m(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def quantity(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def unit_price(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\6", self.line_array[self.line_array_pos])

