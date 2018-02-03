import sys
import csv

def read_input(file_location):
	input_file = open(file_location, "r")
	for mindex, m in enumerate(input_file):
		m = m.replace('{', '')
		m = m.replace('}', '')
		m = m.replace('\n', '')
		temp_set = m.split(', ')
		temp_set = set(temp_set)
		print(temp_set)
if len(sys.argv) == 2:
	read_input(str(sys.argv[1]))
else:
	print("Please run as python ms-apriori.py [input_file].txt")