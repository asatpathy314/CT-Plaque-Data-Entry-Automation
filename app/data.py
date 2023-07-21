import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import csv
import re
import shutil
import os

#Convert text to REDCap data value
def translateTextToIdentifier(inputVessel, lookupTable):
    outputString = "12"
    for row in lookupTable:
        if inputVessel.lower() == row[1].lower():
            outputString = row[0]
            return int(outputString)
    return int(outputString)

#Return column of a 2D array as a 1D array
def returnColAsArray(TwoDArray, n):
    return [i[n] for i in TwoDArray]

#Remove Non-Numeric characters from a string (periods are kept as decimals)
def removeNonNumeric(inputString):
    pattern = r"[^\d.]"
    return re.sub(pattern, "", inputString)

#Convert a .csv file to a 2D Array (yes I know I could've used csv.reader() I'm just an idiot)
def convertTo2DArray(csvFilePath):
    csvArray = [i.split(",") for i in open(csvFilePath, "r").readlines()]
    def addBlank(arr1D, targetLen):
        while(len(arr1D)<targetLen):
            arr1D.append("")
        return arr1D
    def strip(string):
        return string.strip("\n")            
    csvArray = [list(map(strip, addBlank(i, len(csvArray[0])))) for i in csvArray]
    return csvArray

#Get rid of the elements in .txt input that don't need to be in array.
def stripArrayElements(arr):
    strippedArray = [element.strip() for element in arr if element != "\n" and ":" not in element]   
    return strippedArray

#Populate the .csv database import format with the input from the .txt file
def update_csv_file(input_file_path, format_file_path, target_record_id):
    
    lookupTable = [["1", "D1"], ["2", "D2"], ["3", "D3"], ["4", "OM1"], ["5", "OM2"], ["6", "OM3"], ["7", "Ramus"],
                   ["8", "L-PLB"], ["9", "L-PDA"], ["10", "R-PLB"], ["11", "R-PDA"], ["13", "LM"], ["14", "LAD"],
                   ["15", "LCX"], ["16", "RCA"]]
    
    txtArrayList = [i for i in open(input_file_path, 'r').readlines()]
    txtArrayList = stripArrayElements(txtArrayList)
    csv2DArray = convertTo2DArray(format_file_path)

    #Find target column
    try:
        targetColumn = csv2DArray[1].index(target_record_id)
    except ValueError:
        print("Invalid record ID, check that the record ID is present and spelled correctly in the format .csv file")
    
    #Initialize tracker variables
    indexOfLoggedData = []
    otherCounter = 0
    csvFirstCol = [i[0] for i in csv2DArray]
    i=0

    #Begin while loop
    while i < len(txtArrayList):
        tempIndex = translateTextToIdentifier(txtArrayList[i], lookupTable)
        
        #For any of the four major vessels. Feel free to remove this and edit the lookup table accordingly if you would rather treat all the vessels the same.
        if tempIndex in range(13, 17):
            for j in range(csvFirstCol.index("ncpvolume_"+str(txtArrayList[i]).lower()), csvFirstCol.index("ncpvolume_"+str(txtArrayList[i]).lower())+26):
                i+=1
                if csv2DArray[j][targetColumn] != "":
                    csv2DArray[j][targetColumn] = str(float(csv2DArray[j][targetColumn]) + float(removeNonNumeric(txtArrayList[i])))
                else:
                    csv2DArray[j][targetColumn] = removeNonNumeric(txtArrayList[i])

        #Any other less commonly contoured vessels
        else:
           otherIndex = csvFirstCol.index("ncpvolume_" + str(otherCounter+1))
           csv2DArray[otherIndex-2][targetColumn] = str(tempIndex)
           if tempIndex==12:
              csv2DArray[otherIndex-1][targetColumn] = 1
           
           if txtArrayList[i] in indexOfLoggedData:
                
                otherIndex = csvFirstCol.index("ncpvolume_" + str(indexOfLoggedData.index(txtArrayList[i])+1))
                for j in range(otherIndex, otherIndex+26):
                    i += 1
                    csv2DArray[j][targetColumn] = str(float(csv2DArray[j][targetColumn])+float(removeNonNumeric(txtArrayList[i])))   
           else:
                for j in range(otherIndex, otherIndex+26):
                    i+=1
                    csv2DArray[j][targetColumn] = removeNonNumeric(txtArrayList[i])
           otherCounter += 1
           indexOfLoggedData.append(txtArrayList[i-26])
        i += 1
               
    if otherCounter > 0:
        csv2DArray[csvFirstCol.index("numbertoreport")][targetColumn] = str(otherCounter)
        csv2DArray[csvFirstCol.index("numbertoreport")-1][targetColumn] = 1

    return csv2DArray
    


#GUI Maker
def start_program():
    input_file_path = input_file_entry.get()
    format_file_path = format_file_entry.get()
    target_record_id = record_id_entry.get()

def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)


def browse_format_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    format_file_entry.delete(0, tk.END)
    format_file_entry.insert(0, file_path)

def download_file():
    input_file_path = input_file_entry.get()
    format_file_path = format_file_entry.get()
    target_record_id = record_id_entry.get()
    csv_data = update_csv_file(input_file_path, format_file_path, target_record_id)

    # Create a temporary CSV file for download
    temp_file_path = "updated_data.csv"
    with open(temp_file_path, 'w', newline='', encoding='utf-8') as outputFile:
        writer = csv.writer(outputFile)
        writer.writerows(csv_data)

    # Move the temporary file to the downloads folder
    downloads_folder = tk.filedialog.askdirectory(initialdir="~/Downloads")
    destination_file_path = os.path.join(downloads_folder, "updated_data.csv")
    shutil.copy2(temp_file_path, destination_file_path)

    # Remove the temporary file
    os.remove(temp_file_path)

#Initialization
root = tk.Tk()
root.title("CT Data Automaton")
root.resizable(False,False)

# Input File Path
input_file_label = tk.Label(root, text="Input File Path:")
input_file_label.grid(row=0, column=0, sticky="E")
input_file_entry = tk.Entry(root)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)
browse_input_button = tk.Button(root, text="Browse", command=browse_input_file)
browse_input_button.grid(row=0, column=2, padx=5)

# Format File Path
format_file_label = tk.Label(root, text="Format File Path:")
format_file_label.grid(row=1, column=0, sticky="E")
format_file_entry = tk.Entry(root)
format_file_entry.grid(row=1, column=1, padx=10, pady=5)
browse_format_button = tk.Button(root, text="Browse", command=browse_format_file)
browse_format_button.grid(row=1, column=2, padx=5)

# Target Record ID
record_id_label = tk.Label(root, text="Target Record ID:")
record_id_label.grid(row=2, column=0, sticky="E")
record_id_entry = tk.Entry(root)
record_id_entry.grid(row=2, column=1, padx=10, pady=5)

# Start Button
start_button = tk.Button(root, text="Create File", command=start_program)
start_button.grid(row=5, column=0, columnspan=2, pady=10)

# Download Button
download_button = tk.Button(root, text="Download", command=download_file)
download_button.grid(row=5, column=1, columnspan=2, pady=10)

# Result Label
root.mainloop()
