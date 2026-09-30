from pathlib import Path
import os
import pdfplumber
import re
from .pdf_scripts import * #do not delete, it is being used

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
				instance = globals()[script.upper()]#input the script name as upper() so it matches its own class
				instantiated = instance(line_array)
				csv_array = instantiated.format_array_to_csv()
				if self.test_csv(csv_array, file_name):
					with open(self.output_dir + file_name + ".csv", "w+") as f:
						for line in csv_array:
							f.write(line)
							pass
						pass
					pass
				else:
					pass
					#raise Exception("Some formatting went wrong in file " + file_name)
				break
			pass
		else:
			print(file_name + " isnt handled yet on its own")
			with open("txts/" + file_name + ".txt", "w+") as f:
				for line in line_array:
					f.write(line + "\n")
			#raise Exception("No such script")
			pass
		return


	def test_csv(self, csv_array, file_name) -> bool:
		status = True
		if not csv_array[1:]:
			print(file_name + " something went wrong in file " + file_name)
			return False
		for i in range(1, len(csv_array)):
			#if re.match(r"([\d-]*)\t(.*)\t(\d{1,5})\t(\d+\.\d{0,2})", line):
			if re.match(r"(\d{2}-\d{5}(-\d{2}){0,1})\t(.*)\t(\d*)\t(\d*)\t(\d*\.\d*)\t(\d*\.\d*)", csv_array[i]):
				pass
			else:
				print("something went wrong in file " + file_name + " in line " + str(i+1) + "\nwith the following content:\n"+ csv_array[i])
				status = False
		return status
