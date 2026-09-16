import pdfplumber
import sys
import os


args = sys.argv[1:]

input_dir = "pdfs/"
txt_dir = "txts/"
output_dir = "outputs/"

regex_list_cbplu=[]

files = []
if args == []:
	for file in os.listdir(input_dir):
		files.append(file)
		pass
	pass
else:
	for file in args:
		print(file)
		files.append(file.strip(input_dir))
		pass
	pass


input_files = []
input_file_to_txts = []
output_files = []
for file in files:
	print(file)
	input_files.append(input_dir + file)
	input_file_to_txts.append(txt_dir + file)
	output_files.append(output_dir + file)
	pass
print(input_files)
print(input_file_to_txts)
print(output_files)

#pdf to txt
for file in range(len(input_files)):
	print(file)
	with pdfplumber.open(input_files[file]) as pdf:
		pages = ""
		for page in pdf.pages:
			pages += page.extract_text()
			pass
		with open(input_file_to_txts[file], "w+") as txt:
			txt.write(pages)
			pass
		pass
	pass


#txt to csv
for file in range(len(input_files)):
	print(file)
	with open(input_file_to_txts[file], "r") as f:
		for line in f.readlines():
			with open(output_files, "a") as f:
				f.write(line)
				pass
			pass
		pass
	pass


def delete_lines_untill_Prod_No(line_array, line_array_pos):
	#while not reading regex match to \d{2}-\d{5}-\d{2}:
	#	delet line
	#	dont advance line_array_pos cause we are deleting
	#
	pass


def format_lines_untill_Totall(line_array, line_array_pos):
	#while not reading regex match to Total\d*(,|.)\d*:
	#	format lines
	#	advance line_array_pos
	#
	return line_array_pos

def format_txt_to_csv(inputfile, outputfile):
	# iwas das inputfile zu line_array macht
	line_array = []
	line_array.insert(0,"Product No.	Product Description	U O M	Quantity	Unit Price	Total")
	line_array_pos = 1
	while line_array_pos < len(line_array):
		delete_lines_untill_Prod_No(line_array, line_array_pos)
		line_array_pos = format_lines_untill_Totall(line_array, line_array_pos)


