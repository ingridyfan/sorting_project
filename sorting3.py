import csv
import sys
import pandas as pd
import numpy as np
import time
import timeit
import datetime

#CONSTS
NUMCOMP = "Numerical"
DATECOMP = "Date"
TEXTCOMP = "Text"

''' 
The following code is for dropping all irrelevant rows in the CSV

Call the function get_filtered_dataframe

Input: 
	filename of the CSV
	List of Tuples with the format...
		(Category Name, Comparison Type, Operator, Value)
all of the string type. 

Output: a pandas dataframe of the complete csv with all irrelevant values dropped
'''

#compare num values
def comp_num(entry, data):
	cat = entry[0]
	operator = entry[2]
	val = float(entry[-1])
	to_drop = []

	if operator == '=':
		for index, row in data.iterrows():
			cur = row[cat]
			if float(cur) != val or cur != cur:
				to_drop.append(index)
	elif operator == '!=':
		for index, row in data.iterrows():
			cur = row[cat]
			if float(cur) == val or cur != cur:
				to_drop.append(index)
	elif operator == '>':
		for index, row in data.iterrows():
			cur = row[cat]
			if float(cur) <= val or cur != cur:
				to_drop.append(index)
	elif operator == '<':
		for index, row in data.iterrows():
			cur = row[cat]
			if float(cur) >= val or cur != cur:
				to_drop.append(index)

	return data.drop(to_drop)

#compare string values
def comp_text(entry, data):
	cat = entry[0]
	operator = entry[2]
	val = str(entry[-1])
	to_drop = []

	if operator == '=':
		for index, row in data.iterrows():
			cur = row[cat]
			if str(cur) != val or cur != cur:
				to_drop.append(index)
	elif operator == '!=':
		for index, row in data.iterrows():
			cur = row[cat]
			if str(cur) == val or cur != cur:
				to_drop.append(index)

	return data.drop(to_drop)

#compare date values
def comp_date(entry, data):

	cat = entry[0]
	val = time.strptime(entry[-1], "%m/%d/%y")
	operator = entry[2]
	to_drop = []

	if operator == '=':
		for index, row in data.iterrows():
			cur = time.strptime(row[cat], "%m/%d/%y")
			if cur != val or cur != cur:
				to_drop.append(index)
	elif operator == '!=':
		for index, row in data.iterrows():
			cur = time.strptime(row[cat], "%m/%d/%y")
			if cur == val or cur != cur:
				to_drop.append(index)
	elif operator == '>':
		for index, row in data.iterrows():
			cur = time.strptime(row[cat], "%m/%d/%y")
			if cur <= val or cur != cur:
				to_drop.append(index)
	elif operator == '<':
		for index, row in data.iterrows():
			cur = time.strptime(row[cat], "%m/%d/%y")
			if cur >= val or cur != cur:
				to_drop.append(index)

	return data.drop(to_drop)

#comparison directory
def comp_director(entry, data):
	cur_comp = entry[1]

	print ("comp type: " + cur_comp)

	if(cur_comp == NUMCOMP): 
		return comp_num(entry, data)

	elif(cur_comp == DATECOMP): 
		return comp_date(entry, data)

	else:
		return comp_text(entry, data)

#call to drop 
def get_filtered_dataframe(data, entries):
	
	def remove_irrelevant_cols(data, selected, categories):
		always_relevant = set(['Invited', 'MID', 'MTURK_ID'])

		irrelevant_cols = list(set(categories) - set(selected) - always_relevant)

		return data.drop(columns=irrelevant_cols)

	subset = data.copy()
	
	for entry in entries:
		subset = comp_director(entry, subset)

	selected = [x[0] for x in entries]

	subset = remove_irrelevant_cols(subset, selected, data.columns.values.tolist())

	################################################################
	##### uncomment this out to update the invited column ##########
	################################################################
	# update_invited(subset, data, filename)

	print (subset.head(3))
	return subset


def test():
	data = pd.read_csv('newworkersCSV.csv')
	test = get_filtered_dataframe(data, [('ANES_POL', 'Numerical', '=', '3'), ('Q32_Browser', 'Text', '=', 'Chrome'), ('Invited', 'Date', '>', '02/26/18')])

'''updates invited column in the original csv'''
def update_invited(subset, data, filename):
	now = datetime.datetime.now()
	date = now.strftime("%m-%d-%y").replace('-', '/')

	MIDs = subset['MID'].tolist()

	for idx, row in data.iterrows():
		if row['MID'] in MIDs:
			data.ix[idx, 'Invited'] = date

	newOriginal = filename + "_" + str(date)
	data.to_csv(newOriginal)

'''takes in num of workers that the user would like to select and creates a 
subset of the qualified workers of that size '''
def random_selection(subset, num):
	if len(subset) > num:
		return subset.sample(n = num, random_state = 1)
	return subset 

test()