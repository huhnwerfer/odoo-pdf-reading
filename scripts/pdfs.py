from pathlib import Path
import os
import pdfplumber
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
			if not "init" in script:
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
				instance = globals()[script.upper()]#input the script as upper()
				instantiated = instance(line_array)
				csv_array = instantiated.format_array_to_csv()
				with open(self.output_dir + file_name + ".csv", "w+") as f:
					for line in csv_array:
						f.write(line)
						pass
					pass
				pass
				break
			pass
		else:
			#raise Exception("No such script")
			pass
		return

