import re

import pdfplumber

from .pdf_scripts import *

class PDFS:
	def __init__(self, file_names: list, input_dir: str, output_dir: str):
		self.file_names = file_names
		self.input_dir = input_dir
		self.output_dir = output_dir
		pass


	def pdf_to_array(self, file) -> str:
		with pdfplumber.open(self.input_dir + file) as pdf:
			pages = ""
			for page in pdf.pages:
				pages += page.extract_text()
				pass
			pass
		return pages


	def all_pdfs(self):
		for file_name in self.file_names:
			pages = self.pdf_to_array(file_name)
			self.which_pdf(file_name, pages)
			pass
		pass


	def which_pdf(self, file, pages):
		match file:
			case "CBPLU*": # maybe automate this step by looking what python scripts exist in pdf_scripts
				cbplu = CBPLU()
				cbplu.format_array_to_csv(pages)
				pass
			case _:
				pass #try out all of them again maybe one has the same formating? but check against some tests
		pass
	pass
