import sys
import os
from pdfs import PDFS


RESET_COLOR = "\033[0m"
RED_COLOR = "\033[31m"
YELLOW_COLOR = "\033[33m"

def no_files_given(input_dir: str) -> list:
	file_array = []
	for file in os.listdir(input_dir):
		file_array.append(file)
		pass

	return file_array


def files_given(arg_array) -> tuple[str, list]:
	# test if files exist and are valid
	file_array = []
	input_dir = ""
	for file in arg_array:
		if True: # find out if arg is a pdf and if it's a valid path
			# strip path to file and store path and file seperatly
			file_array.append(file)
			pass
		pass
	return input_dir, file_array


def main(arg_array):
	file_names: list
	input_dir = "pdfs/"
	output_dir = "outputs/"
	txt_dir = "txts/"
	failing_txt_dir = "failing_txts/"

	if arg_array == []:
		file_names = no_files_given(input_dir)
		pass
	else:
		input_dir, file_names = files_given(arg_array)
		pass
	file_names.sort(key=lambda v: v.upper())
	for file_name in file_names:
		pdf = PDFS()
		line_array = pdf.pdf_to_array(input_dir, file_name)
		pdf_text = pdf.line_array_to_text(line_array)
		company = pdf.find_company(line_array, pdf_text)
		order_id = pdf.get_order_id(company, pdf_text)
		if not company:
			print(f"{RED_COLOR}{file_name} could not be handled.{RESET_COLOR}")
			pdf.write_txt_to_file(failing_txt_dir, pdf_text, file_name)
			continue

		print(f"{file_name} is being handled by {company.__class__.__name__}.")
		pdf.write_txt_to_file(txt_dir, pdf_text, file_name)
		dict_array = pdf.line_array_to_dict_array(company)
		error_msg = pdf.test_dict_array(dict_array, file_name)
		if error_msg != "":
			print(error_msg)
		csv_array = pdf.dict_array_to_csv_array(dict_array)
		csv_array[-1] += "\n" # for test purposes
		csv_array.append("\n") # for test purposes
		csv_array.append("Order ID: " + order_id) # for test purposes
		pdf.write_csv_to_file(output_dir, csv_array, file_name)
		pass
	return


if __name__ == "__main__":
	main(sys.argv[1:])
	pass
