import re


class CBPLU:
	def __init__(self, line_array: list):
		self.line_array = line_array
		self.csv_array = []
		self.line_array_pos = 0
		pass
	def delete_lines_untill_prod_no(self):
		# while not reading regex match to \d{2}-\d{5}-\d{2}:
		while self.line_array_pos < len(self.line_array) and not re.search(r"\d{2}-\d{5}-\d{2}", self.line_array[self.line_array_pos]):
			self.line_array_pos += 1
			pass
		return

	def format_lines_untill_totall(self):
		while self.line_array_pos < len(self.line_array) and not re.search(r"Total\d*(,|.)\d*", self.line_array[
			self.line_array_pos]):  # not reading regex match to Total\d*(,|.)\d*:
			this_line = self.line_array[self.line_array_pos]
			next_line = self.line_array[self.line_array_pos + 1]
			new_string = {
				"Product_no.": "",
				"Product_des": "",
				"U_O_M": "",
				"Quantity": "",
				"Unit Price": "",
				"Total": "",
			}
			new_string["Product_no."] = re.sub(r"(\d{2}-\d{5}-\d{2})( PLU) (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\1", this_line)
			new_string["Product_des"] = re.sub(r"(\d{2}-\d{5}-\d{2})( PLU) (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\3", this_line)
			new_string["Product_des"] += re.sub(r"(.*)( *PC)( EUR)", r" \1", next_line)
			new_string["U_O_M"] = re.sub(r"(\d{2}-\d{5}-\d{2})( PLU) (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\4", this_line)
			new_string["Quantity"] = re.sub(r"(\d{2}-\d{5}-\d{2})( PLU) (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\5", this_line)
			new_string["Unit Price"] = re.sub(r"(\d{2}-\d{5}-\d{2})( PLU) (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\6", this_line)
			new_string["Total"] = re.sub(r"(\d{2}-\d{5}-\d{2})( PLU) (.*) (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\7", this_line)
			self.csv_array.append("")
			for i in new_string:
				self.csv_array[-1] += new_string[i] + "\t"
			self.csv_array[-1] = self.csv_array[-1][:-1] + "\n"
			self.line_array_pos += 2
			pass
		return

	def format_array_to_csv(self):
		self.csv_array.append("Product No.	Product Description	U O M	Quantity	Unit Price	Total\n")
		while self.line_array_pos < len(self.line_array):
			self.delete_lines_untill_prod_no()
			self.format_lines_untill_totall()
		return self.csv_array
	pass

