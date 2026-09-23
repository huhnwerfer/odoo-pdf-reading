import pdfplumber
import sys
import os
import re
from scripts.pdfs import PDFS


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
txt_files = []
output_files = []
for file in files:
	print(file)
	input_files.append(input_dir + file)
	txt_files.append(txt_dir + file + ".txt")
	output_files.append(output_dir + file + ".csv")
	pass
print(input_files)
print(txt_files)
print(output_files)

#pdf to txt
for file in range(len(input_files)):
	print(file)
	with pdfplumber.open(input_files[file]) as pdf:
		pages = ""
		for page in pdf.pages:
			pages += page.extract_text()
			pass
		with open(txt_files[file], "w+") as txt:
			txt.write(pages)
			pass
		pass
	pass


pdfs = PDFS()
pdfs.input_files = input_files
pdfs.txt_files = txt_files
pdfs.output_files = output_files
pdfs.all_pdfs()

####################################################### aalll of this for the CBPLU_\d*.pdf




#format_txt_to_csv("CBPLU_4100128240.pdf.txt", "CBPLU_4100128240.csv")
