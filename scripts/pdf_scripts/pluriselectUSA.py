import re
from .pdf import PDF


class PLURISELECTUSA(PDF):
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
		while self.line_array_pos < len(self.line_array) and not re.search(r"Total\d*(,|.)\d*", self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass

