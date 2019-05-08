import csv
import sys
import array
import time
import random
import pandas as pd
import datetime

#categories = []
users = [] #all of the users with all of their information 
qualifications = [] #list of all qualifications entered 
EXIT = -1
MID_NUM = 1 #THIS SHOULD BE UPDATED IF THE CSV IS UPDATED
catNums = [MID_NUM]

def readMyFile(filename):
	global users
	with open(filename, 'rU') as csvfile: #import file here
		csvreader = csv.reader(csvfile) #reads file
		for inx, row in enumerate(csvreader):
        		if(inx == 0): 
        			categories = row[:]
        		else: users.append(row)

        return users, categories

def getCatIndex(categories, category):
	return categories.index(category)

def printCategories(categories):
	print("\nBelow are all categories and their corresponding numbers: ")
	for inx, cat in enumerate(categories):
		print(inx, cat)

def getDate(): 
	print("\nPlease enter the date (in mm/dd/yy format) you would like to compare. Remember that any members that have that exact date will not qualify.")
	month = input("month (mm): ")
	day = input("day (dd): ")
	year = input("year (yy): ")
	return str(month) + "/" + str(day) + "/" + str(year)


def checkBeforeOrAfter(inputDate): #checks whether they want all the dates before or after the date they inputed
	while(True): 
		beforeInput = input("If you would like all users BEFORE " + inputDate + ", please enter 1. If you would like all users AFTER, please enter 0: ")
		if(beforeInput == 1):
			return True
		elif(beforeInput == 0):
			return False
		else:
			print("\n[ERROR] Please enter a valid input") #try/catch
	return True

def compare_date_helper(beforeBool, date, catNum):
	global users
	newList = []

	if (beforeBool):
		for inx, pers in enumerate(users):
			curDate = time.strptime(pers[catNum], "%m/%d/%y")
			if(curDate < date): 
				newList.append(pers)
	else:
		for inx, pers in enumerate(users):
			curDate = time.strptime(pers[catNum], "%m/%d/%y")
			if(curDate > date):
				 newList.append(pers)
	return newList

def getIDs(): #TODO: automatically give list in a csv format 
	global users
	print("\nPrinting out a list of IDs that have matched your qualifications...")
	for user in enumerate(users):
		cur = user[1]
		print(cur[0])

def compar_date(catNum, category):
	global users, qualifications
	validDate = False
	#TODO: MAKE SURE THAT INPUTDATE IS VALID 
	inputDate = getDate()
	dateComp = time.strptime(inputDate, "%d/%m/%y") #converts input to python date format 
	beforeBool = checkBeforeOrAfter(inputDate)
	if(beforeBool):
		qualifications.append(category + " before " + inputDate) #TODO: adapt for all types with dates
	else:
		qualifications.append(category + " after " + inputDate)
	users = compare_date_helper(beforeBool, dateComp, catNum)
	update_users(len(users))

def check_under_or_over(val):
	isUnder = input("\nIf you would like all users under " + str(val) + ", please enter 1. If you would like all users over, please enter 0: ")
	if(isUnder == 1):
		return True
	elif(isUnder == 0):
		return False
	else:
		print("\n[ERROR] Please enter a valid input") #try/catch
	return True

def compare_val_helper(isUnder, val, catNum):
	global users
	newList = []
	if (isUnder):
		for inx, pers in enumerate(users):
			curVal = int(pers[catNum])
			print(curVal)
			if(curVal < val): 
				#print("reached")
				newList.append(pers)
	else:
		for inx, pers in enumerate(users):
			curVal = int(pers[catNum])
			if(curVal > val):
				 newList.append(pers)
	return newList

def compar_val(catNum, category): #selects within value comparison categories
	global users, qualifications
	val = input("Enter the value you would like to compare. Remember that any hit that has this exact value will not qualify: ")
	isUnder = check_under_or_over(val)
	if(isUnder):
		qualifications.append(category + " under " + str(val)) #TODO: adapt for all types with dates
	else:
		qualifications.append(category + " over " + str(val))
	users = compare_val_helper(isUnder, val, catNum)
	update_users(len(users))

def select_helper(qualifs, catNum):
	global users
	temp = []
	for index in range(len(qualifs)):
		qualif = qualifs[index]
		for inx, pers in enumerate(users):
			if(pers[catNum] == qualif):
				temp.append(pers)
	return temp

def selection(catNum, category): #selects within characteristic selection categories
	global users, qualifications
	arr = []

	print("\nPlease enter either one or more qualifications corresponding to the selected category one at a time. Note that all qualifications within this category must be entered within this round.")
	qualification = raw_input("\nenter a qualification desired: ")
	while(qualification != ""):
		arr.append(qualification)
		qualifications.append(category + ": " + qualification)
		qualification = raw_input("\nenter another qualification desired or press enter to continue: ")
	users = select_helper(arr, catNum)
	update_users(len(users))
 
def comp_director(comp_val, catNum, category):
	if(comp_val == 0): 
		compar_val(catNum, category)
	elif(comp_val == 1): 
		compar_date(catNum, category)
	elif(comp_val == 2):
		selection(catNum, category)

def update_users(sz): #how many qualifying participants left
	if(sz == 0): 
		print("\n[ERROR] Oh no! You have no qualifying participants left.")
		return
 	print("\nthere are " + str(sz) + " qualifying participants left.")

def wrap_helper_selection_num(sz): #how many users to select from list
	num = sz + 1
	while(num > sz):
		num = input("Enter the number of qualifying workers you would like to select: ")
		if(num > sz): 
			print("\n[ERROR] Please enter a value equal to or less than " + str(sz) + ": ")
	return num

def wrap_helper_random_selection(num):
	global users, qualifications
	rand_smpl = [ users[i] for i in sorted(random.sample(xrange(len(users)), num)) ]
	return rand_smpl

def wrap_helper_del(subset, cat_sz):
	global catNums
	arr = []
	for idx, row in enumerate(subset): 
		arr_row = []
		for i in range (cat_sz):
			if i in catNums:
				arr_row.append(row[i])
		arr.append(arr_row)
	return arr

def wrap_up(cat_sz):
	global users, qualifications
	print("\nall qualifications entered: ")
	print(qualifications)
	#print(users)
	sz = len(users)
	update_users(sz)
	num = wrap_helper_selection_num(sz)
	subset = wrap_helper_random_selection(num)
	print("\nReturning " + str(num) + " randomly selected qualified workers.")
	return wrap_helper_del(subset, cat_sz)

def invalid_input(val, all_vals): 
	if(val > (all_vals - 1)): 
		return True
	return False

# def updateInvitedDate(filename, qualified):
# 	#parse in line by line
# 	#edit invited for each person in qualified
# 	#write it to a new file
# 	#
def toCSV(categories, catNum, qualified):
	#to csv

	#csvfile = "/Users/ingridyfan/Documents/Stanford/SocLab/sorting project/qualifiedWorkers.csv" #this is the full path name
	
	#csvfile = 'qualifiedWorkers.csv' #[UNCOMMENT THIS TO EDIT THE SCRIPT]
	csvfile = sys.argv[2] 

	catNums.sort()
	finalCats = [categories[x] for x in catNums] #gets the row of all relevant categories
	with open(csvfile, "wb") as f:
    		writer = csv.writer(f)
    		writer.writerows([finalCats])
    		writer.writerows(qualified)

	print ("Check the file " + csvfile +" for a csv of your qualified workers!")


def overwrite(filename, qualified):
	midList = [elem[0] for elem in qualified]

	now = datetime.datetime.now()
	date = now.strftime("%m/%d/%y")
	data = pd.read_csv(filename)


	for idx, mid in enumerate(data['MID']):
		if data.ix[idx, 'MID'] in midList:
			data.ix[idx, 'Invited'] = date

	newOriginal = "new" + filename
	data.to_csv(newOriginal)

	print ("Check the file " + newOriginal + " for a csv of your updated workers csv.")



def main():
	#qualifications: a list that states all the qualifications entered by the user
	#users: a list of all the users that qualified, contains all of their characteristics
	#categories: a list of all the categories available
	#catNums: a list of all the category numbers

	global users, qualifications

	#filename = '/Users/ingridyfan/Documents/Stanford/SocLab/sorting project/testingcsv.csv' 

	#filename = 'workersCSV.csv' #[EDIT INPUT FILENAME HERE]

	#ensures that user enters a filename
	if len(argv) < 2: 
		print ("Please enter a filename.")
		return


	filename = sys.argv[1]

	categories = [] #all of the categories
	users, categories = readMyFile(filename) #creates an array of the entire sheet
	compare = ["value comparison", "date comparison", "characteristic selection"]


	catNum = 0
	while(catNum != EXIT): #choose category within this loop
		printCategories(categories) #lists categories and indices for user to read
		catNum = input("Enter the category number you wish to select OR enter -1 to exit: ")
		if(catNum == -1): 
			break

		elif(invalid_input(catNum, len(categories))): 
			print ("\n[ERROR] Please enter a valid category number!")
			catNum = 0
			continue
			
		else:
			catNums.append(catNum)
			print ("\nYou have selected the category: " + categories[catNum])
		
		printCategories(compare)

		comparType = 0
		while(comparType != -1):
			comparType = input("Enter the comparison type appropriate for the " + categories[catNum] + " category OR enter -1 to choose another category: ")
			if(comparType != -1): #directs to appropriate type of comparison
				if(invalid_input(comparType, len(compare))):
					print("\n[ERROR] Please enter a valid number corresponding to a comparison type!")
					comparType = 0
					continue
				else:
					comp_director(comparType, catNum, categories[catNum])
					break

		if not users: 
			print "No users qualify. Ending program."
			return
		print ("\nAll qualifications entered so far: ")
		print (qualifications)

		catNum = input("enter any number to continue or -1 to exit: ") #ERROR CHECK THAT A NUMBER WAS INPUTTED



	qualified = wrap_up(len(categories))
	print (qualified)

	toCSV(categories, catNums, qualified)
	overwrite(filename, qualified)

#overwrite csv
	# midList = [elem[0] for elem in qualified]
	# print midList

	# now = datetime.datetime.now()
	# date = now.strftime("%m/%d/%y")
	# filename = 'workersCSV.csv'
	# data = pd.read_csv(filename)


	# for idx, mid in enumerate(data['MID']):
	# 	if data.ix[idx, 'MID'] in midList:
	# 		print "reached"
	# 		data.ix[idx, 'Invited'] = date

	# print data['Invited']

	# newOriginal = "new" + filename
	# data.to_csv(newOriginal)


main()

#TO_DO: take in arguments that become the inport and export files
#TO_DO: BE ABLE TO AUTOMATICALLY FIND THE M_TURK ID COLUMN WITHOUT HAVING TO HARD CODE IT IN
#TO_DO: BE ABLE TO INPUT A CHARACTERISTIC THAT THEY ~DONT~ WANT IN THE LIST
#T0_DO: BE ABLE TO HAVE A SENTINAL VALUE THAT THEY CAN ENTER TO SELECT ALL PARTICIPANTS LEFT IF THEY MESSED UP
#TO_DO: HOW TO BACK UP?




