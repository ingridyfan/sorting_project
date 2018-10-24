A program that narrows down a list of mturk workers based on desired qualifications and spits out a random subset of all qualified workers

INPUT: a csv type file with the first row being categories, the first column being MID
OUTPUT: a subset of the input file with a list of workers that qualify after the sort

SETUP: 
1. Put the .csv file that you will be reading and the developer file (sorting.py) into the same folder. 


INSTRUCTIONS:
3. Open terminal and navigate to the directory that sorting.py is located in. 

4. Type in the command:
                        python sorting.py "INPUT FILENAME" "EXPORT FILENAME"
                        for example:
                                    python sorting.py workersCSV.csv qualifiedWorkers.csv
    and hit enter
    
5. Follow the instructions that are printed

6. You have three options for selection type in each category:
        a. "Value Comparison" --> Enter a value to get all numbers either greater than or less than the input value
        b. "Date Comparison" --> Enter a date (mm/dd/yy) to get all dates before or after the input date
        c. "Characteristic Selection" --> Enter any characteristic (ex. "1", "Yes", "White") to get all matching characteristics with the input string. More than one characteristic can be selected at a time. 
        
7. When you are done passing in qualifications, at the command:
            "enter any number to continue or -1 to exit:"
    enter -1. The program will then tell you how many participants have qualified. Enter a number n that is less than or equal to the number of qualified participants for the program to randomly select n participants to output into your output csv file. 
    
8. Check your directory for your new exported CSV file under your export file name!  
