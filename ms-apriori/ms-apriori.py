import sys
import csv
import re
from itertools import chain, combinations
import itertools

# List of values and their respective MIS values
mis_dict = {}
# List of given transactions
list_of_transactions = []
# List of cannot_be_together sets
list_of_cbt = []
# List of items
list_of_items = []
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
		# Find all ints, put into a list, then append them to list_of_items
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

# Calculate support and support-count for each unique item
def calculate_support():
	# Calculate the support count of each item in transaction
	for transaction in list_of_transactions:
		for item in transaction:
			if item in list(support_dict.keys()):
				support_dict[item]['support_count'] += 1
			else:
				support_dict.update({item: {'support_count': 1, 'support': 0, 'mis': mis_dict[item]}})

	# For each unique item in support-dict, calculate support for each item
	for item in list(support_dict.keys()):
		support_dict[item]['support'] = round(float(support_dict[item]['support_count']) / len(list_of_transactions), 3)
	# Sort list_of_items based on mis values
	list_of_items.sort(key=lambda x: mis_dict.get(x), reverse=False)

# First pass to generate seeds L
def init_pass(M, T):
	# Generate empty seed L
	L = []
	# Store value of minimum MIS for each itemset
	min_mis = 0.0
	for i in M:
		# If support >= mis first item, then append to L
	 	if (support_dict.get(i).get('support') >= support_dict.get(i).get('mis')) and min_mis == 0.0:
	 		min_mis = support_dict.get(i).get('mis')
	 		L.append(i)
	 	# For every element after first item, append if support >= min_mis
	 	elif min_mis != 0.0:
	 		if (support_dict.get(i).get('support') >= min_mis):
	 			L.append(i)
	# Generate 1-itemsets using L
	generate_F1_itemsets(L)

# Generate F1 item-sets
def generate_F1_itemsets(L):
	# For each item in L, if support < mis, prune it from L
	for i in L:
		if (support_dict.get(i).get('support') < support_dict.get(i).get('mis')):
			L.remove(i)
	generate_item_sets(L)

# Generate F(k-1) item-sets
def generate_item_sets(L):
	k = 2
	# Declare Fk
	freq_item_set = []
	# Declare dictionary to hold c.count
	Ck_count_dict = {}
	# For k >= 2 and while Fk != empty
	while (k == 2 or len(freq_item_set) > 1):
		# If k == 2, run generate 2-itemsets
		if k == 2:
			print("Level 2 candidate generation")
			Ck = level2_candidate_gen(L, sdc) # k = 2
			print(Ck)
			# Update c.count as 0 for each item
			for c in Ck:
				Ck_count_dict.update({str(c): 0})
		# If k > 2, generate Fk itemset from Fk-1 itemsets
		else:
			print("Level k > 2 candidate generation")
			Ck = MScandidate_gen(freq_item_set, sdc)

		# For each transaction t in T
		for t in list_of_transactions:
			# For each candidate c in Ck
			for c in Ck:
				# If c is contained in t, increment c.count by 1
				if set(c).issubset(set(t)):
					Ck_count_dict[str(c)] += 1
		# For each candidate c in Ck, if support of c >= c[0].mis, append to Fk
		for c in Ck:
			if Ck_count_dict.get(str(c)) / len(list_of_transactions) >= support_dict.get(c[0]).get('mis'):
				freq_item_set.append(c)
				# Used for rule generation (f-a)
				# if set(c[1:]).issubset(set(t)):
				# 	if str(c[1:]) in Ck_count_dict:
				# 		Ck_count_dict[str(c[1:])] += 1
				# 	else:
				# 		Ck_count_dict.update({str(c[1:]): 1})
		print(Ck_count_dict)
		print(freq_item_set)
		# Increment k
		k += 1

def level2_candidate_gen(L, sdc):
	c2 = []
	for l in L:
		l_mis = 0.0
		l_supp = 0.0
		if support_dict.get(l).get('support') >= support_dict.get(l).get('mis'):
			l_mis = support_dict.get(l).get('mis')
			l_supp = support_dict.get(l).get('support')
			for h in L[L.index(l) + 1:]:
				if (support_dict.get(h).get('support')) >= l_mis and ((support_dict.get(h).get('support') - l_supp) <= sdc):
					c2.append([l, h])
	return c2

def MScandidate_gen(freq_item_set, sdc):
	Ck = []
	f1 = []
	f2 = []
	combinations = []
	print("freq_item_set: " + str(freq_item_set))
	for i in range(len(freq_item_set)):
		f1 = freq_item_set[i][0:-1]
		for j in range(i + 1, len(freq_item_set)):
			f2 = freq_item_set[j][0:-1]
			if (f1 == f2) and (support_dict.get(freq_item_set[i][-1]).get('support') - support_dict.get(freq_item_set[j][-1]).get('support') <= sdc):
				# freq_item_set[i].append(freq_item_set[j][-1])
				## PROBLEM freq_item_set[i] should not append ^
				# MAKE ANOTHER COPY THEN STORE IN CK
				# c = freq_item_set[i].append(freq_item_set[j][-1])
				# c.append(freq_item_set[j][-1])
				# freq_item_set[i].append(freq_item_set[j][-1])
				temp_list = list(freq_item_set)
				c1 = list(temp_list[i])
				c2 = temp_list[j][-1]
				c1.append(c2)
				print(c1)
				Ck.append(c1)
				# Generate (k-1) subsets s for each c
	print("freq_item_set2: " + str(freq_item_set))
	i = 0
	while i < len(Ck):
		subsets = list(itertools.combinations(Ck[i], len(Ck[i]) - 1))
		print("Ck: " + str(Ck))
		for s in subsets:
			s = list(s)
			print(s)
			if (Ck[i][0] in s) or (support_dict.get(Ck[i][1]).get('mis') == support_dict.get(Ck[i][0]).get('mis')):
				if s not in freq_item_set:
					print("removing: " + str(Ck[i]))
					Ck.remove(Ck[i])
		i += 1
	print("Ck after removal: " + str(Ck))
	sys.exit(0)

# Check for command line arguments
if len(sys.argv) == 3:
	# Parse input and parameter files
	read_parameter(str(sys.argv[2]))
	read_input(str(sys.argv[1]))

	# Actual algorithm start
	calculate_support()
	init_pass(list_of_items, list_of_transactions)
else:
	print("Please run as python ms-apriori.py [input_file].txt [parameter_file].txt")