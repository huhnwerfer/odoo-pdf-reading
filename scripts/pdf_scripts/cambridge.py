import re
from .pdf import PDF


class CAMBRIDGE(PDF):
	delete_lines_until_pattern = r"(\d{2}-\d{5}-(\d{2})?)"
	format_lines_until_pattern = r"Deliver To"
	#Qty	Catalogue No.	Description	Requested Date	Unit Price	Disc %	Total Price
	regex_array = [r"(\d+) (\d{2}-\d{5}-(\d{2})?) (.*) \d{2}/\d{2}/\d{4} (\d*\.\d*) \d*\.\d* (\d*\.\d*)", r"(.*)"]
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

	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_string = ""
		prod_string += re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])
		counter = 1
		while not (re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos+counter]) or re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos+counter])):
			prod_string += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+counter])
			self.line_jumper += 1
			counter += 1
		return prod_string


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def u_o_m(self) -> str:
		return ""
