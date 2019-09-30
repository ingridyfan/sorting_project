import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import *
# from PIL import ImageTK, Image

import os
import csv
import sys
import pandas as pd
import numpy as np
import time
import timeit
import datetime
from PIL import ImageTk, Image

#import sorting code
import sorting3 as sorting

## Globals
infoButtonPicName = "info.png"
csvName = ""
categories = []
comparisons = ['=', '!=', '<', '>']
comparisonTypes = ['Numerical', 'Text', 'Date']
backgroundColor = "light blue"

class LineItem:
	def __init__(self, categoryDropdownVal, categoryDropdown, comparisonTypeDropdownVal,
		comparisonDropdownVal, valueEntry):
		self.categoryDropdownVal = categoryDropdownVal
		self.categoryDropdown = categoryDropdown
		self.comparisonTypeDropdownVal = comparisonTypeDropdownVal
		self.comparisonDropdownVal = comparisonDropdownVal
		self.valueEntry = valueEntry

def addNewCat():
	global categories
	
	if not categories:
		showSelectCSVDialogBox("Add Another Category")
		return False

	step = len(root.mainWindowFrame.entries)

	catVar = StringVar(root.mainWindowFrame)
	catVar.set(categories[0])
	catMenu = OptionMenu(root.mainWindowFrame, catVar, *categories)
	catMenu.grid(row = 1 + step, column = 0, sticky = 'nsew')

	compTypeVar = StringVar(root.mainWindowFrame)
	compTypeVar.set(comparisonTypes[0])
	compTypeMenu = OptionMenu(root.mainWindowFrame, compTypeVar, *comparisonTypes)
	compTypeMenu.grid(row = 1 + step, column = 1, sticky = 'nsew')

	compVar = StringVar(root.mainWindowFrame)
	compVar.set(comparisons[0])
	compMenu = OptionMenu(root.mainWindowFrame, compVar, *comparisons)
	compMenu.grid(row = 1 + step, column = 2, sticky = 'nsew')

	valEntry = Entry(root.mainWindowFrame)
	valEntry.grid(row = 1 + step, column = 3, sticky = 'nsew')

	root.mainWindowFrame.entries.append(LineItem(catVar, catMenu, compTypeVar, compVar, valEntry))

	return True

def removeLastCat():
	global categories
	global csvName
	global data

	if (csvName == "" or data is None or categories is None):
		print("no data entered")
		showSelectCSVDialogBox("Remove Last Category")
		return

	if len(root.mainWindowFrame.entries) < 2:
		showRemoveLastCatDialogBox();
		return

	for i in range(4):
		widget = root.mainWindowFrame.winfo_children()[-1]
		widget.destroy()

	root.mainWindowFrame.entries.pop()
	# print(len(root.mainWindowFrame.entries))

def showRemoveLastCatDialogBox():
	tk.messagebox.showinfo("Info: Unable to Remove Category", "You must have at least 1 category.")

def showSelectCSVDialogBox(buttonFunction):
	tk.messagebox.showinfo("Info: Please Select CSV File", "Please select a CSV File before clicking the \"" + buttonFunction + "\" button.")

def categoryHelpDialogBox():
	tk.messagebox.showinfo("Category Help", "These are the categories that you may filter on. You may choose a category once you've selected a CSV.")

## TODO: HOW TO FORMAT THE DATE
def comparisonTypeHelpDialogBox():
	tk.messagebox.showinfo("Comparison Type Help",
		"The types of comparisons supported are as follows: \n\n\n"\
		"Numerical: comparison with numbers\n\n"\
		"Text: comparison with text\n\n"
		"Date: comparison with a date, where > is after the date and < is before.\n"\
		"Please format the date as: ") ## fill this out

def valueEntryHelpDialogBox():
	tk.messagebox.showinfo("Value Entry Help", "Type in a value that corresponds to your Comparison Type.\n\n" \
		"Please format the date as: ")

def generalHelpButtonDialogBox():
	tk.messagebox.showinfo("General Help",
		"The following program enables you to filter out a subset of MTurk workers who only have particular traits satisfied.\n\n"\
		"First, select a CSV of the MTurk workers and their traits.\nNext, add constraints that you want satisfied.\n"\
		"Finally, generate and save a new CSV of the desired size of worker information.")


'''checks compatibility of each value input with the comparison type after the generate button is pressed'''
def cat_compatibility(lineItem):
	cat = lineItem.categoryDropdownVal.get()
	catType = lineItem.comparisonTypeDropdownVal.get()
	val = lineItem.valueEntry.get()
	if catType == 'Date':
		try:
			date = time.strptime(val, "%m/%d/%y")
		except ValueError:
			tk.messagebox.showinfo('Invalid Value', 'Invalid date value for the ' + cat + ' category.\n\n Please format all dates in mm/dd/yy. Ex: 05/06/18')
			return False
		except TypeError:
			tk.messagebox.showinfo('Invalid Value', 'Invalid date value for the ' + cat + ' category.\n\n Please format all dates in mm/dd/yy. Ex: 05/06/18')
			return False
	elif catType == 'Numerical':
		try:
			num = float(val)
		except ValueError:
			tk.messagebox.showinfo('Invalid Value', 'Invalid numerical value for the ' + cat + ' category.\n\nPlease enter a numeric value. Ex: 56.2')
			return False

	return True

def generate(subsetSize):
	global categories
	global csvName
	global data

	print("generate button pushed!")

	if (csvName == "" or data is None or categories is None):
		print("no data entered")
		showSelectCSVDialogBox("Generate")
		return

	inputList = []
	for lineItem in root.mainWindowFrame.entries:

		''' if the value input in any column is incompatible with the category type'''
		if not cat_compatibility(lineItem):
			#TODO: clear valueEntry box
			return
		inputList.append((lineItem.categoryDropdownVal.get(), lineItem.comparisonTypeDropdownVal.get(), lineItem.comparisonDropdownVal.get(), str(lineItem.valueEntry.get())))
	print('inputList', inputList)


	# TODO: try catch

	''' pull a dataframe of all qualifying workers '''
	filteredData = sorting.get_filtered_dataframe(data, inputList)

	numRows = len(filteredData.index)
	maxBool = ''
	print('numRows', numRows)

	if subsetSize < 0 or numRows < subsetSize:
		subsetSize = numRows
		maxBool = ' (max)'


	subsetData = sorting.random_selection(filteredData, subsetSize)



	# ''' if the generateAll checkbox is selected '''
	# if (root.generateAllSelected()):
	# 	print ("Selected")

	# else:
	# 	print("Not selected")
	# 	# num = SubsetBonus()

	# 	# subsetSize = 1
	# 	# subsetData = sorting.random_selection(filteredData, subsetSize)

	# 	# sw = SubsetWindow(str(numRows))
	# 	# sw.grab_set();
	# 	# sw.mainloop();
	# 	# sw.grab_release();

	# export(subsetData)
	try:
		pathToSave = filedialog.asksaveasfile(mode='w', defaultextension=".csv", title = "Save new CSV", initialdir = '/',
			filetypes = (("csv files","*.csv"),("all files","*.*")), initialfile = csvName.rsplit('/', 1)[-1].split('.')[0] + '-filtered')
	except PermissionError:
		tk.messagebox.showinfo('Permission Error', 'You don\'t have permission to save this file in that location. Please re-generate and try a different save location.')
		return ''

	if pathToSave:
		sorting.update_invited(subsetData, data, csvName)
		subsetData.to_csv(pathToSave)
		root.loadingLabel['text'] = ("Processed! Generated subset of size " + str(subsetSize) + maxBool + ".")
		return pathToSave.name
		# os.startfile(pathToSave.name)
	else:
		root.loadingLabel['text'] = ("No file saved. Please re-generate.")
		return ''


def resetAll():
	global categories
	global csvName
	global data

	root.fileSelectionFrame.fileSelectionText.config(text="Import from: ")
	root.mainWindowFrame.valueEntry.delete(0, tk.END)
	root.loadingLabel['text'] = ("")

	menu = root.mainWindowFrame.categoryDropdown['menu']
	menu.delete(0, tk.END)

	for i in range(len(root.mainWindowFrame.entries) - 1):
		removeLastCat()

	csvName = ""
	data = None
	categories = None

	root.mainWindowFrame.entries[0].categoryDropdownVal.set("Select CSV first")
	root.mainWindowFrame.entries[0].categoryDropdown.config(state="disabled")

	print (len(root.mainWindowFrame.winfo_children()))

def getCSVName():
	global csvName
	global categories
	global data

	csvName = filedialog.askopenfilename(initialdir = '/',title = "Select CSV",filetypes = (("csv files","*.csv"),("all files","*.*")))
	root.fileSelectionFrame.fileSelectionText.config(text="Import from: " + csvName)

	try:
		data = pd.read_csv(csvName)
		categories = data.columns.values.tolist()

	except OSError as e:
		root.fileSelectionFrame.fileSelectionText.config(text="File failed to read. Please select a CSV file.")
		csvName = ""
		catgories = None

	updateCategories();

def updateCategories():
	global csvName
	global data
	global categories

	menu = root.mainWindowFrame.categoryDropdown['menu']
	menu.delete(0, tk.END)

	if csvName == "" or categories is None:
		print("is none")
		resetAll()
	else:
		root.mainWindowFrame.categoryDropdownDefault.set(categories[0])
		for category in categories:
			menu.add_command(label=category, command=lambda name=category:root.mainWindowFrame.categoryDropdownDefault.set(name))
		root.mainWindowFrame.categoryDropdown.config(state="normal")

class Root(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		mainWindowWidth = 800
		mainWindowHeight = 500

		self.geometry(str(mainWindowWidth) + "x" + str(mainWindowHeight))
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=6)
		self.grid_columnconfigure(2, weight=1)
		self.configure(background=backgroundColor)
		self.title("MTurk Workers Filtering Tool")
		self.minsize(500, 350)

		for row in range(7):
			self.grid_rowconfigure(row, weight=1)

		## Make help button
		self.generalHelpButton = tk.Button(text="?", font=("bold"), command=generalHelpButtonDialogBox).grid(row=0, column=2, sticky='ne')

		## Make file selection frame
		self.fileSelectionFrame = FileSelectionFrame(self)
		self.fileSelectionFrame.grid(row=1, column=1, sticky="new")

		## Make main window frame
		self.mainWindowFrame = MainWindowFrame(self)
		self.mainWindowFrame.grid(row=3, column=1, sticky='nsew')

		## Loading label
		self.loadingLabel = tk.Label(text="", bg=backgroundColor, font=("Helvetica", 20, "italic"))
		self.loadingLabel.grid(row=4,column=1,sticky='se')

		## Make buttons frame
		self.buttonsFrame = ButtonsFrame(self)
		self.buttonsFrame.grid(row=5, column=1, sticky='new')

		## Make checkbox
		# self.checkboxVal = IntVar()
		# self.checkboxVal.set(0)
		# self.checkbox = Checkbutton(self.buttonsFrame, variable = self.checkboxVal, onvalue = 1, offvalue = 0, text = "Download All")
		# self.checkbox.configure(background=backgroundColor)
		# self.checkbox.grid(row=6, column=3, sticky='ns')

		## Names and credits
		tk.Label(text="Ingrid Fan & Kadar Qian. 2019.", bg=backgroundColor).grid(row=7, column=1, sticky='s')

	# def generateAllSelected(self):
	# 	# if (self.checkboxVal.get() == 1):
	# 	# 	print ("True")
	# 	# 	return True
	# 	# print("False")
	# 	# return False
	# 	return self.checkboxVal.get()

class FileSelectionFrame(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.config(borderwidth=1)

		for i in range(2):
			self.grid_columnconfigure(i, weight=1)

		for i in range(2):
			self.grid_rowconfigure(i, weight=1)

		self.fileSelectionLabel = tk.Label(self, text="Please select a CSV file:", bg=backgroundColor)
		self.fileSelectionButton = tk.Button(self, text="Select CSV", command=getCSVName, bg="black")
		self.fileSelectionText = tk.Label(self, text="Import from:", bg="light gray", width=40, height=1)

		self.fileSelectionLabel.grid(row=0, column=0, sticky="new",)
		self.fileSelectionButton.grid(row=0, column=1, sticky='new')
		self.fileSelectionText.grid(row=1, column=0, sticky='we', columnspan=2)


class MainWindowFrame(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		self.grid_columnconfigure(0, weight=4)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(2, weight=4)

		for row in range(4):
			self.grid_columnconfigure(row, weight=1)

		# Create the category, comparison, and value entry drop downs
		tk.Label(self, text="Category").grid(row=0, column=0, sticky='nsw')
		tk.Label(self, text="Comparison Type").grid(row=0, column=1, sticky='nsw')
		tk.Label(self, text="Comparison Operator").grid(row=0, column=2, sticky='nsw')
		tk.Label(self, text="Value").grid(row=0, column=3, sticky='nsw')

		self.categoryHelp = tk.Button(self, text="?", command=categoryHelpDialogBox).grid(row=0, column=0, sticky='nes')
		self.comparisonTypeHelp = tk.Button(self, text="?", command=comparisonTypeHelpDialogBox).grid(row=0, column=1, sticky='nes')
		self.valueEntryHelp = tk.Button(self, text="?", command=valueEntryHelpDialogBox).grid(row=0,column=3, sticky='nes')

		self.categoryDropdownDefault = StringVar(self)
		self.categoryDropdownDefault.set("Select CSV First")
		self.categoryDropdown = OptionMenu(self, self.categoryDropdownDefault, [])
		self.categoryDropdown.config(state="disabled")

		self.comparisonTypeDefault = StringVar(self)
		self.comparisonTypeDefault.set(comparisonTypes[0])
		self.comparisonTypeDropdown = OptionMenu(self, self.comparisonTypeDefault, *comparisonTypes)

		self.comparisonDropdownDefault = StringVar(self)
		self.comparisonDropdownDefault.set(comparisons[0])
		self.comparisonDropdown = OptionMenu(self, self.comparisonDropdownDefault, *comparisons)

		self.valueEntry = Entry(self)

		self.entries = []
		self.entries.append(LineItem(self.categoryDropdownDefault, self.categoryDropdown, self.comparisonTypeDefault, self.comparisonDropdownDefault, self.valueEntry))

		self.categoryDropdown.grid(row=1, column=0, sticky='nsew')
		self.comparisonTypeDropdown.grid(row=1, column=1, sticky='nsew')
		self.comparisonDropdown.grid(row=1, column=2, sticky='nsew')
		self.valueEntry.grid(row=1, column=3, sticky='nsew')

class ButtonsFrame(tk.Frame):
	def __init__(self, parent):
		self.parent = parent
		tk.Frame.__init__(self, parent)

		self.configure(background=backgroundColor)

		for i in range(4):
			self.grid_columnconfigure(i, weight=1)
		for i in range(2):
			self.grid_rowconfigure(i, weight=1)

		self.resetButton = tk.Button(self, text="Reset All", command=self.resetAll)
		self.removeButton = tk.Button(self, text = "Remove Last Category", command = removeLastCat)
		self.addButton = tk.Button(self, text = "Add Another Category", command = self.addNewCat)
		self.generateButton = tk.Button(self, text="Generate", command=self.popup)
		self.fileExportText = tk.Label(self, text="Export to:", bg="light gray", width=40, height=1)
		# self.exportButton = tk.Button(self, text = "Export Subset", command=lambda : generate(int(self.entryValue())))
		# self.exportButton["state"] = "disabled"

		# Print out to buttons window frame
		self.resetButton.grid(row=0, column=0, sticky='nsew')
		self.removeButton.grid(row=0,column=1, sticky='nsew')
		self.addButton.grid(row=0,column=2, sticky='nsew')
		self.generateButton.grid(row=0, column=3, sticky='nsew')
		# self.exportButton.grid(row=0, column =4, sticky='nsew')
		self.fileExportText.grid(row=1, column=0, sticky='we', columnspan=4)
		

	def resetAll(self):
		resetAll()
		self.removeButton["state"] = "disabled"
		self.fileExportText.config(text="Export to:")

	def addNewCat(self):
		if addNewCat():
			self.removeButton["state"] = "normal"

	def popup(self):
		self.w=popupWindow(self.master)
		self.generateButton["state"] = "disabled" 
		self.master.wait_window(self.w.top)
		self.generateButton["state"] = "normal"
		# self.exportButton["state"] = "normal"
		# root.loadingLabel['text'] = ("Generating random subset of size " + self.entryValue())
		exportPath = generate(int(self.entryValue()))
		self.fileExportText.config(text="Export to: " + exportPath)

	def entryValue(self):
		return self.w.value

class popupWindow(object):
	def __init__(self,master):
		top=self.top=Toplevel(master)
		self.l=Label(top,text="Please input the size of your desired random subset of workers.\nIf you would like to export the complete set of qualified workers, please enter a negative value.")
		self.l.pack()
		self.e=Entry(top)
		self.e.pack()
		self.b=Button(top,text='Enter',command=self.cleanup)
		self.b.pack()

	def cleanup(self):
		self.value=self.e.get()
		self.top.destroy()




''' Class definition for subset window generation '''
# class SubsetWindow(tk.Tk):

# 	def __init__(self, *args, **kwargs):
# 		tk.Tk.__init__(self, *args, **kwargs)

# 		windowWidth = 500
# 		windowHeight = 500

# 		self.geometry(str(windowWidth) + "x" + str(windowHeight))
# 		self.grid_columnconfigure(0, weight=1)
# 		self.grid_columnconfigure(1, weight=6)
# 		self.grid_columnconfigure(2, weight=1)
# 		self.configure(background=backgroundColor)
# 		self.title("Download Subset of Workers")
# 		self.minsize(500, 350)

# 		for row in range(7):
# 			self.grid_rowconfigure(row, weight=1)

# 		self.done = tk.Button(self, text="done", command=self.cleanup).grid(row=0, column=0, sticky='nsw')



root = Root()
img = tk.Image("photo", file = "./robb.png")
root.iconphoto(True, img)
root.tk.call('wm', 'iconphoto', root._w, img)
root.mainloop()






