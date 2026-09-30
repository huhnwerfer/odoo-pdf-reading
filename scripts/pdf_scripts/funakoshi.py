import re
from .pdf import PDF


class FUNAKOSHI(PDF):
	def format_array_to_csv(self):
		self.csv_array.append("Product No.	Product Description	U O M	Quantity	Unit Price	Total\n")
		while self.line_array_pos < len(self.line_array):
			self.delete_lines_untill_()
			self.format_lines_untill_()
		return self.csv_array


	def delete_lines_untill_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(r"\d{2}-\d{5}-\d{2}", self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return

	def format_lines_untill_(self):
		while self.line_array_pos < len(self.line_array) and not re.search(r"((CONTINUED)|(Total))|(SPECIAL INSTRUCTIONS: EUR)", self.line_array[self.line_array_pos]):
			regex_array = [r"(PLS\d{6}\w{0,1}) (\d{2}-\d{5}-\d{2}) (.*) (\d+) (\d+) (\d+\.\d+) (\d+\.\d+)"]
			self.csv_array.append(self.csv_line(regex_array))
			self.line_array_pos += 2
			pass


	def catalog_no(self, regex_array) -> str:
		raise Exception("Function catalog_no is not implemented")


	def prod_no(self, regex_array) -> str:
		raise Exception("Function prod_no is not implemented")
		return ""


	def prod_des(self, regex_array) -> str:
		raise Exception("Function prod_des is not implemented")
		return ""


	def u_o_m(self, regex_array) -> str:
		raise Exception("Function u_o_m is not implemented")
		return ""


	def quantity(self, regex_array) -> str:
		raise Exception("Function quantity is not implemented")
		return ""


	def unit_price(self, regex_array) -> str:
		raise Exception("Function unit_price is not implemented")
		return ""


	def total(self, regex_array) -> str:
		raise Exception("Function total is not implemented")
		return ""

