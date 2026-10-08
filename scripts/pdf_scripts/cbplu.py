import re
from .pdf import PDF


class CBPLU(PDF):
	delete_lines_until_pattern = r"\d{2}-\d{5}-\d{2}"
	format_lines_until_pattern = r"Total\d*(,|.)\d*"
	regex_array = [r"(\d{2}-\d{5}-\d{2}) PLU (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"(.*)(( *PC)|(ML))( EUR)"]


	def prod_no(self) -> str:
		return re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self) -> str:
		prod_des_str = ""
		prod_des_str += re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])
		for i in range(1, self.line_jumper):
			prod_des_str += " " + re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+i])
		return prod_des_str


	def u_o_m(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def quantity(self) -> str:
		return re.sub(self.regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def delete_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return

	def format_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(self.format_lines_until_pattern, self.line_array[
			self.line_array_pos]):  # not reading regex match to Total\d*(,|.)\d*:
			self.csv_array.append(self.csv_line())
			self.line_array_pos += 2
			pass
		return

	def format_array_to_csv(self):
		while self.line_array_pos < len(self.line_array):
			self.delete_lines_until_()
			self.format_lines_until_()
		return self.csv_array
	pass

