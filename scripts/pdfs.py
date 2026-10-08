from pathlib import Path
import os
import pdfplumber
import re
from .pdf_scripts import * #do not delete, it is being used
MAX_ERROR_PER_PDF = 5
class PDFS:
	scripts = []
	path_to_pdf_scripts = "scripts/pdf_scripts"
	def __init__(self, file_names: list, input_dir: str, output_dir: str):
		self.file_names = file_names
		self.input_dir = input_dir
		self.output_dir = output_dir
		self.what_scripts()
		return


	def pdf_to_array(self, file) -> list:
		with pdfplumber.open(self.input_dir + file) as pdf:
			pages = ""
			for page in pdf.pages:
				pages += page.extract_text()
				pass
			pass
		return pages.splitlines()


	def what_scripts(self):
		for script in os.listdir(self.path_to_pdf_scripts):
			if not "init" in script and not "pdf" in script:
				self.scripts.append(Path(script).stem)
				pass
			pass
		return


	def all_pdfs(self):
		for file_name in self.file_names:
			line_array = self.pdf_to_array(file_name)
			self.which_pdf(file_name, line_array)
			pass
		return


	def which_pdf(self, file_name, line_array):
		for script in self.scripts:
			if script.lower() in file_name.lower():
				with open("txts/" + file_name + ".txt", "w+") as f:
					for line in line_array:
						f.write(line + "\n")
				pass
				instance = globals()[script.upper()]#input the script name as upper() so it matches its own class
				instantiated = instance(line_array)
				csv_array = instantiated.format_array_to_csv()
				csv_status = self.test_csv(csv_array, file_name)
				csv_status_str = ""
				csv_status_str += file_name + " has the following problem lines: \n"
				for line in csv_status:
					csv_status_str += line
					pass
				csv_status_str += "\n"
				errors = len(csv_status)
				match errors:
					case 0:
						self.save_csv_to_file(csv_array, file_name)
					case _ if errors <= MAX_ERROR_PER_PDF:
						self.save_csv_to_file(csv_array, file_name)
						print(csv_status_str)
					case _:
						raise Exception("Formatting has more then " + str(MAX_ERROR_PER_PDF) + " errors\n" + csv_status_str)
				break
			pass
		else:
			print(file_name + " isnt handled yet on its own")
			with open("failing_txts/" + file_name + ".txt", "w+") as f:
				for line in line_array:
					f.write(line + "\n")
			#raise Exception("No such script")
			pass
		return


	def test_csv(self, csv_array, file_name) -> list[str]:
		status: list[str] = []
		if not csv_array[1:]:
			print(file_name + " something went wrong in file " + file_name)
			return False
		for i in range(1, len(csv_array)):
			#if re.match(r"([\d-]*)\t(.*)\t(\d{1,5})\t(\d+\.\d{0,2})", line):
			#Product Number" + "\t" + "Product Description" + "\t" + "U O M" + "\t" + "Quantity" + "\t" + "Unit Price" + "\t" + "Total"
			if re.match(r"(\d{2}-\d{5}(-\d{0,2})?)\t(.+)\t(.*)\t(\d+)\t(.*)\t(.*)", csv_array[i]):
				pass
			else:
				status.append("line " + str(i+1) + ": "+ csv_array[i])
		return status


	def save_csv_to_file(self, csv_array, file_name):
		with open(self.output_dir + file_name + ".csv", "w+") as f:
			for line in csv_array:
				f.write(line)
				pass
			pass
		pass
