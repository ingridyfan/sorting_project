import csv
import sys
import pandas as pd
import timeit

EXIT = -1


#print list helper function
def print_lst(cats):
	for idx, cat in enumerate(cats):
		print (str(idx)+ " " + cat)

#checks that user did not select a value by mistake
def mistaken_input():
	incorrect = input("is this correct? Press enter to continue or any key + enter to abandon current selection: ")

	if incorrect:
		print ('Abandoning current selection.\n')

	return incorrect 

#checks that user inputted a valid input
def valid_input(cats_len, cat_num):

	return cat_num in range(cats_len)

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

#user chooses category and compare type
def user_input(data, categories):
	compare_types = ["VALUE COMPARISON", "DATE COMPARISON", "CHARACTERISTIC SELECTION"]

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

# #compare values
# def select_compar_val(cat_num, cur_cat, data):

# 	val = float(input("Enter the value you would like to compare. Remember that any hit that has this exact value will not qualify: "))
# 	print("Would you like all values under or over " + str(val) + "?")
# 	u_o = int(input("Enter 0 for under and 1 for over: "))
# 	comp_type = 'UNDER'

# 	# TODO: validate input 
# 	if not valid_input(2, u_o):
# 		print("Please enter a valid input [0/1]\n")
# 		return compar_val(cat_num, cur_cat, data)

# 	if u_o:
# 		comp_type = 'OVER'


# 	print("\nYou want to compare all " + cur_cat " values that are " + comp_type + " " + val ".")
# 	if mistaken_input():
# 		return select_comp(cat, compare_types)

# 	return val, u_o

# def comp_director(cat_num, comp_num, cur_cat, data):
# 	if(comp_val == 0): 
# 		return compar_val(cat_num, cur_cat, data)
# 	elif(comp_val == 1): 
# 		return compar_date(cat_num, cur_cat, data)
# 	else:
# 		return selection(cat_num, cur_cat, data)

def sort_fx(data, categories):
	cat_num, comp_num = user_input(data, categories)
	#comp_director(cat_num, comp_num, categories[cat_num], data)




def main():

	#ensures that user enters a filename
	# if len(argv) != 2: 
	# 	print ("Please enter only the filename.")
	# 	return

	#filename = sys.argv[1]

	filename = 'workersCSV.csv' #[EDIT INPUT FILENAME HERE]

	data = pd.read_csv(filename)
	categories = data.columns.values.tolist()


	sort_fx(data, categories)




main() 