import sys
import csv

# List of values and their respective MIS values
list_of_mis = []
# List of given transactions
list_of_transactions = []

# Read and parse input file and store each transaction to list_of_transactions
def read_input(input_location):
	# Open input_location and parse line by line
	input_file = open(input_location, "r")
	for mindex, m in enumerate(input_file):
		m = m.replace('{', '')
		m = m.replace('}', '')
		m = m.replace('\n', '')
		temp_set = m.split(', ')
		temp_set = set(temp_set)
		list_of_transactions.append(temp_set)

def read_parameter(parameter_location):
	parameter_file = open(parameter_location, "r")
	for index, i in enumerate(parameter_file):
		if "MIS" in i:
			i = i[4:-1]
			i = i.split(')')
			item_no = i[0]
			i = str(i)
			i = i.split('=')
			temp_mis = i[1]
			temp_mis = temp_mis.replace('\']', '')
			temp_mis = temp_mis.replace(' ', '')
			list_of_mis.append((item_no, temp_mis))
		elif "SDC" in i:
			i = i.split(' = ')
			i = i[1]
			print("SDC: " + i)
		elif "cannot_be_together" in i:
			i = i.split(': ')
			i = str(i)
			i = i.split(', ')
			i = i[1:]
		elif "must-have" in i:
			i = i.split(': ')
			i = i[1]
			i = str(i)
			i = i.replace('\n', '')
			i = i.split(' or ')

if len(sys.argv) == 3:
	read_input(str(sys.argv[1]))
	read_parameter(str(sys.argv[2]))
	print(str(list_of_mis))
	print(str(list_of_transactions))
else:
	print("Please run as python ms-apriori.py [input_file].txt [parameter_file].txt")