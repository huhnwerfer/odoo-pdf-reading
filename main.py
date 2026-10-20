import sys
import os
from pdfs import PDFS



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
		if True: # find out if arg is a pdf and if its a valid path
			# strip path to file and store path and file seperatly
			file_array.append(file)
			pass
		pass
	return input_dir, file_array


def main(arg_array):
	file_names: list
	input_dir = "pdfs/"
	output_dir = "outputs/"
	txts = "txts/"
	failing_txts = "failing_txts/"

	if arg_array == []:
		file_names = no_files_given(input_dir)
		pass
	else:
		input_dir, file_names = files_given(arg_array)
		pass
	for file_name in file_names:
		pdf = PDFS()
		line_array = pdf.pdf_to_array(input_dir, file_name)
		pdf_text = pdf.line_array_to_text(line_array)
		company = pdf.find_company(pdf_text)
		if not company:
			print(f"{file_name} could not be handled.")
			pdf.pdf_to_txt(failing_txts, pdf_text, file_name)
			# write pdf to failing txts
			continue
		print(f"{file_name} is being handled by {company.__class__.__name__}.")
		# write pdf to txts
		company.set_line_array(line_array)
		csv_array = pdf.line_array_to_dict_array(company, line_array, file_name)
		#check if csv_array right format
		pdf.save_csv_to_file(output_dir, csv_array, file_name)
		pass
	return
	pass


if __name__ == "__main__":
	main(sys.argv[1:])
	pass
