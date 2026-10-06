import re
from .pdf import PDF


class PLURISELECTUSA(PDF):
	delete_lines_until_pattern = r"\d{2}-\d{5}-\d{2}"
	format_lines_until_pattern = r"Total"
	regex_array = [r"(\d{2}-\d{5}-\d{2}) (.*) (\d*)(.*) (\d*\.\d*) (\d*\.\d*)", r"(.*)"]

	def format_array_to_csv(self):
		while self.line_array_pos < len(self.line_array):
			self.delete_lines_until_()
			self.format_lines_until_()
		return self.csv_array


	def delete_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return

	def format_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.csv_array.append(self.csv_line())
			self.line_array_pos += self.line_jumper
			self.line_jumper = 1
			pass


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])
		if not re.match(self.delete_lines_until_pattern, self.line_array[self.line_array_pos+1]):
			prod_string += " " + self.line_array[self.line_array_pos+1]
			self.line_jumper = 2
		return prod_string


	def u_o_m(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])

