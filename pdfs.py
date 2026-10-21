from pathlib import Path
import importlib
import pdfplumber
from scripts import * #do not delete, it is being used


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
	def find_company(pdf_text):
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
					company = obj()
					if company.is_correct_firm(pdf_text):
						return company
					pass
				pass
			pass
		return None


	def line_array_to_dict_array(self, company, line_array, file_name) -> list[dict]:
		#csv_array = company.format_array_to_csv()
		while company.line_array_pos < len(company.line_array):
			company.delete_lines_until_()
			company.format_lines_until_()
		return company.dict_array
		#return company.csv_array
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
		return company.line_array_to_dict_array(line_array)


	@staticmethod
	def pdf_to_txt(output_dir, pdf_text, file_name):
		with open(output_dir + file_name + ".txt", "w+") as f:
			f.write(pdf_text)
			pass


	def which_script(self, file_name, line_array):
		for script in self.scripts:
			if script.lower() in file_name.lower():
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

	@staticmethod
	def save_csv_to_file(output_dir, csv_array, file_name):
		with open(output_dir + file_name + ".csv", "w+") as f:
			for line in csv_array:
				f.write(line)
				pass
			pass
		pass

	def dict_array_to_csv_array(self, dict_array) -> list[str]:
		csv_array = []
		filled_dict_keys = []
		for dictionary in dict_array:
			for k, v in dictionary.items():
				if v is not "":
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
