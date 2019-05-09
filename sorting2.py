import csv
import sys
import pandas as pd
import numpy as np
import time
import timeit
import datetime

EXIT = -1

#print list helper function
def print_lst(cats):
	for idx, cat in enumerate(cats):
		print (str(idx)+ " " + cat)

#checks that user did not select a value by mistake
def mistaken_input():
	incorrect = input("Is this correct? Press enter to continue or any key + enter to abandon current selection: ")

	if incorrect:
		print ('Abandoning current selection.\n')

	return incorrect 

#checks that user inputted a valid input
def valid_input(upper_bound, val):

	return val in range(upper_bound)


#user chooses category and compare type
def user_input(data, categories):
	compare_types = ["VALUE COMPARISON", "DATE COMPARISON", "CHARACTERISTIC SELECTION"]
	
	#user chooses category helper fx
	def select_cat(categories):

		catNum = int(input("Enter the category number you wish to select OR enter -1 to exit: "))

		if catNum == -1: #EXIT
			return catNum

		#invalid input
		if not valid_input(len(categories), catNum): 
			print ("\n[ERROR] Please enter a valid category number!")
			return select_cat(categories)

		print ("\nYou have selected the category: " + categories[catNum])

		if mistaken_input():
			return select_cat(categories)

		return catNum

	#user chooses comparison type helper fx
	def select_comp(cat, compare_types):
		comp_num = int(input("Enter the comparison type number appropriate for the " + cat + " category OR enter -1 to choose another category: "))

		if comp_num == -1:
			return comp_num

		if not valid_input(len(compare_types), comp_num):
			print ("\n[ERROR] Please enter a valid category number!")
			return select_comp(cat, compare_types)

		print ("\nYou have selected the category: " + compare_types[comp_num])

		#mistaken input
		if mistaken_input():
			return select_comp(cat, compare_types)

		return comp_num


	#choose category
	print_lst(categories)
	cat_num = select_cat(categories)
	
	if cat_num == EXIT: 
		return -1, -1 

	print_lst(compare_types)
	comp_num = select_comp(categories[cat_num], compare_types)

	#user regrets category selection
	if comp_num == -1:
		user_input(data, categories)

		
	return cat_num, comp_num 

#value comparison
def comp_val(cat_num, cur_cat, data, qualifs):
	#user inputs value comparison input and under/over boolean
	def select_comp_val(cur_cat):
		print("\nRemember that any hit that has the exact value entered will not qualify.")
		val = float(input("Please enter the numerical value you would like to compare: "))
		print("Would you like all values UNDER or OVER " + str(val) + "?")
		u_o = int(input("Enter 0 for UNDER and 1 for OVER: "))
		comp_type = 'UNDER'

		# TODO: validate input without user having to start all over
		if not valid_input(2, u_o):
			print("Please enter a valid input [0/1]\n")
			return select_comp_val(cat_num, cur_cat, data)

		if u_o:
			comp_type = 'OVER'


		print("\nYou want to compare all " + cur_cat + 
			" values that are " + comp_type + " " + str(val) + ".")

		if mistaken_input():
			return select_comp_val(cur_cat)

		return val, u_o


	val, u_o = select_comp_val(cur_cat)

	#over
	to_drop = []
	if u_o: 
		#add to list of qualifications
		qualifs.append(cur_cat + " over " + str(val))

		for index, row in data.iterrows():
			cur = row[cur_cat]
			if float(cur) <= val or cur != cur:
				to_drop.append(index)
	#under
	else:
		qualifs.append(cur_cat + " under " + str(val))

		for index, row in data.iterrows():
			cur = row[cur_cat]
			if float(cur) >= val or cur != cur:
				to_drop.append(index)

	return data.drop(to_drop)

#date comparison
def comp_date(cat_num, cur_cat, data, qualifs):
	def get_date():
		print("\nPlease enter the date (in mm/dd/yy format) you would like to compare. Remember that any hits that have that exact date will not qualify.")
		month = int(input("month (mm): "))
		day = int(input("day (dd): "))
		year = int(input("year (yy): "))

		if not valid_input(12, month - 1) or not valid_input(31, day - 1) or not valid_input(100, year - 1):
			print ("\n[ERROR] Please enter a valid month (mm), day (dd), and year (yy)!")
			return select_comp_date()

		return str(month) + "/" + str(day) + "/" + str(year)

	def select_comp_date():
		input_date = get_date()

		print("Would you like all values BEFORE or AFTER " + str(input_date) + "?")
		b_a = int(input("Enter 0 for BEFORE and 1 for AFTER: "))
		comp_type = 'BEFORE'

		# TODO: validate input without user having to start all over
		if not valid_input(2, b_a):
			print("Please enter a valid input [0/1]\n")
			return select_comp_date(cur_cat)

		if b_a:
			comp_type = 'AFTER'

		print("\nYou want to select all workers with " + cur_cat + 
			" dates that are " + comp_type + " " + str(input_date) + ".")

		if mistaken_input():
			return select_comp_date(cur_cat)

		return input_date, b_a

	str_date, b_a = select_comp_date()
	date = time.strptime(str_date, "%d/%m/%y")
	to_drop = []

	#after
	if b_a:
		qualifs.append(cur_cat + " after " + str_date)

		for index, row in data.iterrows():
			#cur_date = row[cur_cat]
			cur_date = time.strptime(row[cur_cat], "%m/%d/%y")

			if cur_date != cur_date or cur_date < date:

				to_drop.append(index)

	#before
	else:
		qualifs.append(cur_cat + " before " + str_date)

		for index, row in data.iterrows():
			cur_date = row[cur_cat]
			if cur_date != cur_date or time.strptime(cur_date, "%m/%d/%y") > date:
				to_drop.append(index)

	return data.drop(to_drop)

#selection
def select(cat_num, cur_cat, data, qualifs):
	def get_selection_val(cur_cat):
		#all entered vals
		vals = []

		print("\nNote that all qualifications selected within this category must be entered within this round.")
		print("Please enter qualifications corresponding to the selected category--one at a time.")

		while True:
			val = str(input("\nEnter a qualification desired or press enter to quit: "))
			
			if not val:
				break

			vals.append(val.lower())
			print("Added the qualification " + val + ".")


		print ( "\nYou have entered the following qualifications: ")
		print_lst(vals)

		if mistaken_input():
			return get_selection_val(cur_cat)

		return vals

	vals = get_selection_val(cur_cat)
	qualifs.append(cur_cat + "of " + str(vals))
	to_drop = []

	for index, row in data.iterrows():
		cur_val = row[cur_cat]
		if cur_val != cur_val or str(cur_val).lower() not in vals:
			to_drop.append(index)

	print (to_drop)
	return data.drop(to_drop)

#directs to correct comparison function
def comp_director(cat_num, comp_num, cur_cat, data, qualifs):
	if(comp_num == 0): 
		return comp_val(cat_num, cur_cat, data, qualifs)
	elif(comp_num == 1): 
		return comp_date(cat_num, cur_cat, data, qualifs)
	else:
		return select(cat_num, cur_cat, data, qualifs)


def sort_fx(data, categories):

	#counts number of workers that qualify so far
	def count_workers(data):
		num_qualified = len(data.index)
		print ("\n there are " + str(num_qualified) + "workers that meet all qualifications entered so far")

		return num_qualified

	#keep only columns that are relevant to qualifications 
	def remove_irrelevant_cols(data, selected, categories):
		always_relevant = set(['Invited', 'MID', 'MTURK_ID'])

		irrelevant_cols = list(set(categories) - set(selected) - always_relevant)

		return data.drop(columns=irrelevant_cols)

	#descriptive list of qualifications
	qualifs = []

	#categories selected
	selected = []

	while (True):

		cat_num, comp_num = user_input(data, categories)
		cur_cat = categories[cat_num]


		if cat_num == -1 or comp_num == -1:
			break

		selected.append(cur_cat)

		#update data
		data = comp_director(cat_num, comp_num, cur_cat, data, qualifs)

		if not count_workers: 
			sys.exit('There are no workers that qualify for this list of qualifications. Exiting the program.')

		#continue or nah
		stop = input("\nPlease press enter if you'd like to proceed with another qualification or input any key + enter to exit: ")
		if stop:
			break

	#print qualifications
	print ("\nAll qualifications entered: ")
	print_lst(qualifs)

	return remove_irrelevant_cols(data, selected, categories)

#update invited column in original dataset
def update_invited(subset, data, date, filename):

	MIDs = subset['MID'].tolist()

	for idx, row in data.iterrows():
		if row['MID'] in MIDs:
			data.ix[idx, 'Invited'] = date

	newOriginal = "new_" + filename
	data.to_csv(newOriginal)

	print ("\nCheck the file " + newOriginal + " for a csv of your updated workers csv.")
	

def main():

	
	#ensures that user enters a filename

	# args = sys.argv[1:]
	# if len(args) != 1:
	# 	sys.exit('Please enter only the filename.')

	filename = 'newworkersCSV.csv' #[EDIT INPUT FILENAME HERE]

	#filename = args[0]

	data = pd.read_csv(filename)
	categories = data.columns.values.tolist()

	#only newly relevant categories and rows 
	# subset = sort_fx(data, categories)
	print (subset)

	now = datetime.datetime.now()
	date = now.strftime("%m-%d-%y")


	#update invited 
	update_invited(subset, data, date.replace('-', '/'), filename)

	#output subset to new csv
	output_name = 'qualified_workers_' + str(date) + '.csv'
	subset.to_csv(output_name)

	print("\nQualified Workers CSV exported as the file: " + output_name)

	#TODO: 
	#update invited column in data

# Python boilerplate
# if __name__ == '__main__':
# 	main() 