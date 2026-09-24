import re


class CBPLU:
	def __init__(self):
		pass
	def delete_lines_untill_Prod_No(line_array, line_array_pos):
		# while not reading regex match to \d{2}-\d{5}-\d{2}:
		while line_array_pos < len(line_array) and not re.search("\d{2}-\d{5}-\d{2}", line_array[line_array_pos]):
			#	delete line
			line_array.pop(line_array_pos)
			#	don't advance line_array_pos cause we are deleting
			#
			pass
		return

	def format_lines_untill_Totall(line_array, line_array_pos):
		while line_array_pos < len(line_array) and not re.search("Total\d*(,|.)\d*", line_array[
			line_array_pos]):  # not reading regex match to Total\d*(,|.)\d*:
			old_string = line_array[line_array_pos]
			old_string = re.sub(" PLU", "", old_string)
			line_array[line_array_pos + 1] = re.sub("PC EUR", "", line_array[line_array_pos + 1])
			new_string = {
				"Product_no.": "",
				"Product_des": "",
				"U_O_M": "",
				"Quantity": "",
				"Unit Price": "",
				"Total": "",
			}
			new_string["Product_no."] = re.search("\d{2}-\d{5}-\d{2}", old_string).group()
			old_string = re.sub(new_string["Product_no."] + " ", "", old_string)
			new_string["Product_des"] = re.sub(r" (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", "",
			                                   re.search(r".* (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", old_string).group())
			new_string["Product_des"] += " " + line_array[line_array_pos + 1].replace("\n", "")
			new_string["U_O_M"] = re.sub(r".* (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\1", old_string).replace("\n", "")
			new_string["Quantity"] = re.sub(r".* (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\2", old_string).replace("\n",
			                                                                                                    "")
			new_string["Unit Price"] = re.sub(r".* (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\3", old_string).replace("\n",
			                                                                                                      "")
			new_string["Total"] = re.sub(r".* (\d*) (\d*) (\d*\.\d*) (\d*\.\d*)", r"\4", old_string).replace("\n", "")

			line_array.pop(line_array_pos + 1)

			# remove old string
			line_array[line_array_pos] = ""
			# add formated sting
			for i in new_string:
				line_array[line_array_pos] += new_string[i] + "\t"
			line_array[line_array_pos] = line_array[line_array_pos][:-1] + "\n"
			line_array_pos += 1
			pass
		return line_array_pos

	def format_array_to_csv(pages: str, path_to_outputfile):
		# iwas das inputfile zu line_array macht
		line_array = []
		with open(inputfile, "r") as f:
			for line in f.readlines():
				line_array.append(line)
				pass
			pass

		line_array.insert(0, "Product No.	Product Description	U O M	Quantity	Unit Price	Total\n")
		line_array_pos = 1
		while line_array_pos < len(line_array):
			CBPLU.delete_lines_untill_Prod_No(line_array, line_array_pos)
			line_array_pos = CBPLU.format_lines_untill_Totall(line_array, line_array_pos)
		with open(path_to_outputfile, "w+") as f:
			for line in line_array:
				f.write(line)
				pass
			pass
		pass
	pass