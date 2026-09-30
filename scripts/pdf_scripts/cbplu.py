import re
from .pdf import PDF


class CBPLU(PDF):


	def prod_no(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\1", self.line_array[self.line_array_pos])


	def prod_des(self, regex_array) -> str:
		prod_des_str = ""
		prod_des_str += re.sub(regex_array[0], r"\2", self.line_array[self.line_array_pos]) + " "
		prod_des_str += re.sub(regex_array[1], r"\1", self.line_array[self.line_array_pos+1])
		return prod_des_str


	def u_o_m(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def quantity(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\4", self.line_array[self.line_array_pos])


	def unit_price(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\5", self.line_array[self.line_array_pos])


	def total(self, regex_array) -> str:
		return re.sub(regex_array[0], r"\6", self.line_array[self.line_array_pos])


	def delete_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(r"\d{2}-\d{5}-\d{2}", self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return

	def format_lines_until_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(r"Total\d*(,|.)\d*", self.line_array[
			self.line_array_pos]):  # not reading regex match to Total\d*(,|.)\d*:
			regex_array = [r"(\d{2}-\d{5}-\d{2}) PLU (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"(.*)( *PC)( EUR)"]
			self.csv_array.append(self.csv_line(regex_array))
			self.line_array_pos += 2
			pass
		return

	def format_array_to_csv(self):
		while self.line_array_pos < len(self.line_array):
			self.delete_lines_until_()
			self.format_lines_until_()
		return self.csv_array
	pass

