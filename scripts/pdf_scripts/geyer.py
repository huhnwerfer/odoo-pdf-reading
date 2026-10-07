import re
from .pdf import PDF


class GEYER(PDF):
	delete_lines_until_pattern = r"(^\d{2,} \d{6,})"
	format_lines_until_pattern = r"Nettosumme"
	#10 12646182 3Pack (à 50 Stück) 65,03 195,09
	#Lieferanten-Artnr: 43-10040-50
	#pluriStrainer Mini, 40µm, 50pcs, 25pcs sterile in bag
	#Liefertermin: 22.09.26
	regex_array = [r"\d{2,} \d{6,} (\d)\w*.* (\d*,\d*) (\d*,\d*)", r".*: (\d{2}-\d{5}-(\d{2})?)", r"(.*)"]

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
		quant = float(re.sub(self.regex_array[0], r"\1", self.line_array[self.line_array_pos]).replace(",", "."))
		if quant.is_integer():
			return str(int(quant))
		return str(quant)


	def unit_price(self) -> str:
		return re.sub(self.regex_array[0], r"\2", self.line_array[self.line_array_pos])


	def total(self) -> str:
		return re.sub(self.regex_array[0], r"\3", self.line_array[self.line_array_pos])


	def prod_no(self) -> str:
		return re.sub(self.regex_array[1], r"\1", self.line_array[self.line_array_pos+1])


	def prod_des(self) -> str:
		prod_string = ""
		counter = 2
		while not (re.search(self.delete_lines_until_pattern, self.line_array[self.line_array_pos+counter]) or re.search(self.format_lines_until_pattern, self.line_array[self.line_array_pos+counter])):
			prod_string += " " + re.sub(self.regex_array[2], r"\1", self.line_array[self.line_array_pos+counter])
			counter += 1
		self.line_jumper = counter
		return prod_string
