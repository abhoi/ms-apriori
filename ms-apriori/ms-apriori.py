import sys
import csv

# List of values and their respective MIS values
mis_dict = {}
# List of given transactions
list_of_transactions = []
# List of items
list_of_items = []
# List of sorted items based on the priority
list_of_ordered_items = []
# Support difference constraint (phi)
SDC = 0.0
# Support Dictionary - Contains MIS and Support count for all items
support_dict = {}

# Read and parse input file and store each transaction to list_of_transactions
def read_input(input_location):
	# Open input_location and parse line by line
	input_file = open(input_location, "r")
	for mindex, m in enumerate(input_file):
		m = m.replace('{', '')
		m = m.replace('}', '')
		m = m.replace('\n', '')
		temp_set = m.split(', ')
		temp_set = map(int, temp_set)
		temp_set = list(temp_set)
		list_of_transactions.append(temp_set)
		for i in temp_set:
			if i in list_of_items:
				continue
			else:
				list_of_items.append(i)

# Read and parse parameter-list and store each value to appropriate lists
def read_parameter(parameter_location):
	parameter_file = open(parameter_location, "r")
	for index, i in enumerate(parameter_file):
		# Parse MIS to list_of_mis
		if "MIS" in i:
			i = i[4:-1]
			i = i.split(')')
			item_no = i[0]
			i = str(i)
			i = i.split('=')
			temp_mis = i[1]
			temp_mis = temp_mis.replace('\']', '')
			temp_mis = temp_mis.replace(' ', '')
			mis_dict.update({int(item_no): float(temp_mis)})
		# Parse and store SDC
		elif "SDC" in i:
			i = i.split(' = ')
			i = i[1]
			SDC = i
		# Custom arguments
		elif "cannot_be_together" in i:
			# PARSE THIS and STORE
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


def sort_items_on_mis(item_list):
	return sorted(item_list, key = mis_dict.get)

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