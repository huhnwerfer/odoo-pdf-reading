import re
from pathlib import Path
import importlib
import pdfplumber
from scripts import * #do not delete, it is being used

RESET_COLOR = "\033[0m"
RED_COLOR = "\033[31m"
YELLOW_COLOR = "\033[33m"

MAX_ERROR_PER_PDF = 5
class PDFS:
	@staticmethod
	def pdf_to_array(input_dir, file) -> list:
		with pdfplumber.open(input_dir + file) as pdf:
			pages = ""
			for page in pdf.pages:
				pages += page.extract_text()
				pass
			pass
		return pages.splitlines()



	@staticmethod
	def line_array_to_text(line_array) -> str:
		pdf_text = ""
		for line in line_array:
			pdf_text += line + "\n"
		pdf_text = pdf_text.strip()
		return pdf_text


	@staticmethod
	def find_company(line_array, pdf_text):
		subfolder = "scripts"
		folder = Path(__file__).parent / subfolder
		for file in folder.glob("*.py"):
			if file.stem in ("__init__", "__base__"):
				continue
			module = importlib.import_module(f"{subfolder}.{file.stem}")
			# Get the company class from the module
			for name in dir(module):
				obj = getattr(module, name)
				if isinstance(obj, type) and issubclass(obj, PDF) and obj is not PDF:
					company = obj(line_array)
					if company.is_correct_firm(pdf_text):
						return company
					pass
				pass
			pass
		return None


	@staticmethod
	def write_txt_to_file(output_dir, pdf_text, file_name):
		with open(output_dir + file_name + ".txt", "w+") as f:
			f.write(pdf_text)
			pass


	@staticmethod
	def line_array_to_dict_array(company, line_array, file_name) -> list[dict]:
		while company.line_array_pos < len(company.line_array):
			company.delete_lines_until_()
			company.format_lines_until_()
		return company.dict_array


	@staticmethod
	def test_dict_array(dict_array, file_name) -> str:
		error_msg = ""
		if not dict_array:
			raise Exception(f"{file_name} failed: dict_array is empty")

		for index, dictionary in enumerate(dict_array, start=1):

			key = "Product Number"
			value = dictionary[key]
			if value == "":
				error_msg += f"{RED_COLOR}line={index}; {key} is empty\n{RESET_COLOR}"
				pass
			elif not re.fullmatch(r"(\d{2}-\d{5}(-\d{2})?)", value):
				error_msg += f"{RED_COLOR}{key} is invalid. (expected dd-ddddd(-dd)): line={index}; {value}\n{RESET_COLOR}"
				pass

			key = "Quantity"
			value = dictionary[key]
			if value == "":
				error_msg += f"{RED_COLOR}line={index}; {key} is empty\n{RESET_COLOR}"
				pass
			elif not re.fullmatch(r"(\d{1,5})", value):
				error_msg += f"{RED_COLOR}{key} is invalid or to big. (max 99999): line={index}; {value}\n{RESET_COLOR}"
				pass
			pass

			key = "Discount"
			value = dictionary[key]
			if value == "":
				error_msg += f"{RED_COLOR}line={index}; {key} is empty\n{RESET_COLOR}"
				pass
			elif not re.fullmatch(r"(\d+\.\d+%?)", value):
				error_msg += f"{RED_COLOR}{key} is invalid or wrong formatted. (expected d.dd(%)): line={index}; {value}\n{RESET_COLOR}"
				pass
			pass

			key = "Product Description"
			value = dictionary[key]
			if value == "":
				error_msg += f"{YELLOW_COLOR}line={index}; {key} is empty\n{RESET_COLOR}"
				pass
			elif not re.fullmatch(r"(.{6,})", value):
				error_msg += f"{YELLOW_COLOR}{key} is short. (at least 6 char): line={index}; {value}\n{RESET_COLOR}"
				pass
		return error_msg + ""


	@staticmethod
	def dict_array_to_csv_array(dict_array) -> list[str]:
		csv_array = []
		filled_dict_keys = []
		for dictionary in dict_array:
			for k, v in dictionary.items():
				if v != "":
					if k not in filled_dict_keys:
						filled_dict_keys.append(k)
						pass
					pass
				pass
			pass
		csv_array.append("")
		for key in filled_dict_keys:
			csv_array[-1] += key + "\t"
		csv_array[-1] = csv_array[-1].strip() + "\n"
		for dictionary in dict_array:
			csv_array.append("")
			for k in filled_dict_keys:
				csv_array[-1] += dictionary[k] + "\t"
				pass
			csv_array[-1] = csv_array[-1].strip() + "\n"
			pass
		csv_array[-1] = csv_array[-1].strip()
		return csv_array

	@staticmethod
	def write_csv_to_file(output_dir, csv_array, file_name):
		with open(output_dir + file_name + ".csv", "w+") as f:
			for line in csv_array:
				f.write(line)
				pass
			pass
		pass
