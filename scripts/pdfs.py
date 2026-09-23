import re
input_files = []
txt_files = []
output_files = []

class PDFS:
	def all_pdfs(self):
		for i in range(len(txt_files)):
			if re.search("CBPLU", txt_files[i]):
				CBPLU.format_txt_to_csv(txt_files[i], output_files[i])
