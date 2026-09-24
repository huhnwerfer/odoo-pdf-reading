import pdfplumber
import sys
import os
import re
from scripts import *



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
			# strip pathj to file and store path and file seperatly
			file_array.append(file)
			pass
		pass
	return input_dir, file_array


def main(arg_array):
	files: list
	input_dir = "pdfs/"
	output_dir = "outputs/"

	if arg_array == []:
		files = no_files_given(input_dir)
		pass
	else:
		input_dir, files = files_given(arg_array)
		pass

	pdfs = PDFS(files, input_dir, output_dir)
	pdfs.all_pdfs()
	pass


if __name__ == "__main__":
	main(sys.argv[1:])
	pass
