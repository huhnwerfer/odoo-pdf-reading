import re
from .pdf import PDF

format_lines_until_pattern = r"((CONTINUED)|(Total))|(SPECIAL INSTRUCTIONS: EUR)"

class FUNAKOSHI(PDF):
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
		while self.line_array_pos < len(self.line_array) and not re.search(format_lines_until_pattern, self.line_array[self.line_array_pos]):
			regex_array = [r".*(\d{2}-\d{5}(-\d{2}){0,1}) (.*) (\d+) (\d+) (\d+\.\d+) (\d+\.\d+)", r"(.*) ()"]
			self.csv_array.append(self.csv_line(regex_array))
			self.line_array_pos += self.line_jumper
			self.line_jumper = 2
			pass


	def prod_no(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self, regex_array) -> str:
		prod_string = ""
		prod_string += re.sub(regex_array[0], r"\3", self.line_array[self.line_array_pos])
		next_line = self.line_array[self.line_array_pos + 1]
		if not re.match(format_lines_until_pattern, next_line) and not re.match(r"(\d{2}-\d{5}(-\d{2})?)", next_line):
			self.line_jumper = 2
			if not re.match(r"(ml)|(pkg)|(pc)|(pcs)", next_line):
				prod_string += next_line
				self.line_jumper = 3
		return prod_string


	def u_o_m(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def quantity(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def unit_price(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def total(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\7", self.line_array[self.line_array_pos])


