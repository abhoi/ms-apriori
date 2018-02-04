import sys
import csv
import re

# List of values and their respective MIS values
mis_dict = {}
# List of given transactions
list_of_transactions = []
# List of cannot_be_together sets
list_of_cbt = []
# List of items
list_of_items = []
# List of sorted items based on the priority
list_of_ordered_items = []
# Support difference constraint (0 <= phi <= 1)
sdc = 0.0
# Support dictionary {item_no: {support_count: }, {support: }, {mis: }}
support_dict = {}
# List of must-have items
list_of_mh = []


# Read and parse input file and store each transaction to list_of_transactions
def read_input(input_location):
	# Open input_location and parse line by line
	input_file = open(input_location, "r")
	for mindex, m in enumerate(input_file):
		m = re.findall(r'\d+', m)
		m = list(map(int, m))
		list_of_transactions.append(m)
		for i in m:
			if i not in list_of_items:
				list_of_items.append(i)

# Read and parse parameter-list and store each value to appropriate lists
def read_parameter(parameter_location):
	parameter_file = open(parameter_location, "r")
	for index, i in enumerate(parameter_file):
		# Parse MIS to mis_dict
		if 'MIS' in i:
			s = re.findall(r'(\d+)', i)
			item_no = int(s[0])
			mis_value = float(s[1] + '.' + s[2])
			mis_dict.update({item_no: mis_value})
		# Parse SDC to sdc
		elif 'SDC' in i:
			s = re.findall(r'\d+\.\d+', i)
			sdc = float(s[0])
		# Parse cannot_be_together to list_of_cbt
		elif 'cannot_be_together' in i:
			s = re.findall(r'{\d+[, \d+]*}', i)
			for e in s:
				e = re.findall(r'\d+', e)
				e = [int(x) for x in e]
				list_of_cbt.append(e)
		# Parse must-have to list_of_mh
		elif 'must-have' in i:
			s = re.findall(r'\d+', i)
			s = [int(x) for x in s]
			list_of_mh = s

# Sort items based on key
def sort_items_on_mis(item_list):
	return sorted(item_list, key = mis_dict.get)

# Calculate support and support-count for each unique item
def calculate_support():
	for transaction in list_of_transactions:
		for item in transaction:
			if item in list(support_dict.keys()):
				details_dict = support_dict[item]
				details_dict['support_count'] = details_dict['support_count'] + 1
			else:
				details_dict = {}
				details_dict['support_count'] = 1
				details_dict['mis'] = mis_dict[item]
				support_dict[item] = details_dict
	
	transaction_len = len(list_of_transactions)
	for item in list(support_dict.keys()):
		details_dict = support_dict[item]
		details_dict['support'] = round(float(details_dict['support_count'])/transaction_len, 2)
		
# Check for command line arguments
if len(sys.argv) == 3:
	read_parameter(str(sys.argv[2]))
	read_input(str(sys.argv[1]))

	list_of_ordered_items = sort_items_on_mis(list_of_items)
	calculate_support()
	print(list_of_items)
	print(mis_dict)
	print(list_of_transactions)
	print(list_of_ordered_items)	
	print(support_dict)

else:
	print("Please run as python ms-apriori.py [input_file].txt [parameter_file].txt")