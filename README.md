# CT Plaque Data Entry Automation

This program is designed to automate CT plaque data entry from the CIRCLE cvi CT module into a REDCap database. It provides a user-friendly GUI interface to streamline the data transfer process.

## Requirements

To use this program, you need to have the following installed:

1. Python 3.x
2. tkinter library
3. csv library
4. re library
5. shutil library
6. os library

## How to Use

1. Create a REDCap database that follows the variable naming conventions practiced in the sample import database file.

2. Download the database import format on your new database.

3. Copy and paste all the data for the patient you're working with from the CT Plaque analysis module on CIRCLE cvi into a .txt file without any modifications.

4. Launch the program and use the GUI to provide the necessary file paths and target record ID:

   - Browse and select the .txt file containing the CT plaque data from the "Input File Path" entry.
   - Browse and select the .csv file with the REDCap database import format from the "Format File Path" entry.
   - Enter the target record ID into the "Target Record ID" entry.

5. Click the "Create File" button to update the .csv file with the processed CT plaque data.

6. Use the REDCap import tool to move all data into your REDCap database.

7. Repeat the process for each patient to automate the data entry and enjoy the time saved.

## Note

Make sure to follow the provided video tutorial for a step-by-step guide on using the program to transfer data accurately and efficiently.

## Disclaimer

This program is intended for use with the specific data format and variable naming conventions of the provided sample import database file. Any changes to the data format or variable names may cause unexpected behavior or errors in the data transfer process. Use this program at your own risk and ensure you have a backup of your data before proceeding.

## Contact

For any questions, issues, or suggestions related to the program, please contact asatpathy314@gmail.com or cqa3ym@virginia.edu. I'm usually available 
always willing to help you fix bugs with the program. Happy data entry!
