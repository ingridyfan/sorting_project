import csv
import sys
import array
import time

#categories = []
users = [] #all of the users with all of their information 
qualifications = [] #list of all qualifications entered 
EXIT = -1

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
	print("Below are all categories and their corresponding numbers: ")
	for inx, cat in enumerate(categories):
		print(inx, cat)

def getDate(): 
	print("please enter the date (in mm/dd/yy format) you would like to compare. Remember that any members that have that exact date will not qualify.")
	month = input("month (mm): ")
	day = input("day (dd): ")
	year = input("year (yy): ")
	return str(month) + "/" + str(day) + "/" + str(year)


def checkBeforeOrAfter(inputDate): #checks whether they want all the dates before or after the date they inputed
	while(True): 
		beforeInput = input("if you would like all users BEFORE " + inputDate + ", please enter 1. If you would like all users AFTER, please enter 0: ")
		if(beforeInput == 1):
			return True
		elif(beforeInput == 0):
			return False
		else:
			print("please enter a valid input") #try/catch
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
	print("printing out a list of IDs that have matched your qualifications...")
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
	isUnder = input("if you would like all users under " + str(val) + ", please enter 1. If you would like all users over, please enter 0: ")
	if(isUnder == 1):
		return True
	elif(isUnder == 0):
		return False
	else:
		print("please enter a valid input") #try/catch
	return True

def compare_val_helper(isUnder, val, catNum):
	global users
	newList = []
	if (isUnder):
		for inx, pers in enumerate(users):
			curVal = int(pers[catNum])
			print(curVal)
			if(curVal < val): 
				print("reached")
				newList.append(pers)
	else:
		for inx, pers in enumerate(users):
			curVal = int(pers[catNum])
			if(curVal > val):
				 newList.append(pers)
	return newList

def compar_val(catNum, category):
	global users, qualifications
	val = input("enter the value you would like to compare. Remember that any hit that has this exact value will not qualify: ")
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

def selection(catNum, category):
	global users, qualifications
	arr = []

	print("Please enter either one or more qualifications corresponding to the selected category one at a time. Note that all qualifications within this category must be entered within this round.")
	qualification = raw_input("enter a qualification desired: ")
	while(qualification != ""):
		arr.append(qualification)
		qualifications.append(category + ": " + qualification)
		qualification = raw_input("enter another qualification desired or press enter to continue: ")
	users = select_helper(arr, catNum)
	update_users(len(users))
 
def update_users(sz):
 	print("there are " + str(sz) + " qualifying participants left.")

def main():
	#qualifications: a list that states all the qualifications entered by the user
	#users: a list of all the users that qualified, contains all of their characteristics
	#categories: a list of all the categories available
	#catNums: a list of all the category numbers
	global users, qualifications
	filename = '/Users/ingridyfan/Documents/Stanford/SocLab/sorting project/testingcsv.csv' #TODO: get people to manually enter filename
	categories = [] #all of the categories
	users, categories = readMyFile(filename) #creates an array of the entire sheet
	compare = ["value comparison", "date comparison", "characteristic selection"]

	catNum = 0
	while(catNum != EXIT):
		printCategories(categories) #lists categories and indices for user to read
		catNum = input("enter the category number you wish to select or enter -1 to exit: ")
		if(catNum == -1): 
			break
		else:
			catNums.append(catNum)
		#TODO: if input is invalid? try/catch?
		printCategories(compare)
		comparType = input("enter the comparison type appropriate for this category or enter -1 to choose another category: ")

		if(comparType != -1):
			if(comparType == 0): 
				compar_val(catNum, categories[catNum])
			elif(comparType == 1): 
				compar_date(catNum, categories[catNum])
			elif(comparType == 2):
				selection(catNum, categories[catNum])
			#TODO: if input is invalid?
		print("all qualifications entered so far: ")
		print(qualifications)
		catNum = input("enter any number to continue or -1 to exit: ")
		
	print("all qualifications entered: ")
	print(qualifications)
	getNewList(catNums)
	#TODO: print out all relevant columns instead of just IDs




	#TODO: ARRAY OF IDS TO USERS 


	#TODO: ARRAY OF MULTIPLE SELECTIONS 

	#print(pets)

	#have a whiel loop that takes in category and qualification(s)
	#only break out of the while loop when the person dictates that they are done submitting categories 
		#SPECIAL INSTRUCTIONS IF ITS DATES
	#after breaking out of while loop, ask which categories that want (MID? etc.)
		#return a list of whatever they ask for 

		#export into a csv 
		#spit out how many we added from that qualification 


main()


#readMyFile('/Users/ingridyfan/Documents/Stanford/SocLab/sorting project/testingcsv.csv')


#i want a subset -- give all or a random list of ___ people 


#TODO: HAVE THE PERSON MANUALLY INPUT WHAT KIND OF COMPARISON IT IS
#TODO: HAVE THE PERSON BE ABLE TO HAVE MULTIPLE QUALIFICATIONS WITHIN EACH CATEGORY BEFORE OVERRIDING THE USER LIST

#type of columns: date comparison, value comparison, specific qualification/characteristic






