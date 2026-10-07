import re
from .pdf import PDF


class DOMINIQUE(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)|(^\d{6} )"
	format_lines_until_pattern = r"(Please confirm this)|(Total)"
	#43-50020-03 PLURISTRAINER 20µm x25 149019 2 57,0000 114,00
	regex_array = [r"(\d{2}-\d{5}-(\d{2})?|\d{6}) (.*) \d{5,}\w* (\d+) (\d*,\d*).* (\d*,\d*).*", r"(.*)"]

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
		prod_string += re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])
		counter = 1
		while not (re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos+counter]) or re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos+counter])):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+counter])
			self.line_jumper += 1
			counter += 1
		return prod_string


	def quantity(self) -> str:
		quant = float(re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos]).replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])
