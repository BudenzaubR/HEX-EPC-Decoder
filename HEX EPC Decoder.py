#Imports
import csv
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
from tkinter import messagebox
from epcutils import binary2epctaguri, epcpureidentityuri2gs1element, epctaguri2epcpureidentityuri, hex2binary

##### MAIN PROGRAMM #####
### User Input ###
# Input CSV File Path
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title="Select CSV File") # show an "Open" dialog box and return the path to the selected file
#filename = "hex.csv"

hasheaders = messagebox.askyesno("CSV Headers", "Does the CSV-File contain headers?")
#hasheaders = True

# Input CSV Delimiter
delimiter = simpledialog.askstring("CSV Delimiter", "Which delimiter is used?")
#delimiter = ','

# Input HEX EPC Column
column = simpledialog.askinteger("EPC Column", "In which column are the Hex EPCs?")
#column = 1

### Start of conversion ###
# Process CSV to convert HEX EPCs to all other formats
# Output is written to results.csv
try:        
    with open(filename) as csvdatei:
        csvReader = csv.reader(csvdatei, delimiter=delimiter)
        with open("results.csv",'w', newline='') as outputFile:
                csvWriter = csv.writer(outputFile, delimiter=delimiter)
                
                for n, row in enumerate(csvReader):
                    # Check for empty row
                    if not row:
                        continue
                    
                    # If in first object check for header row
                    if n == 0:
                        # Write header line for output file
                        csvWriter.writerow(["HEX EPC","EPC Tag URI","EPC Pure Identity URI","GS1 Element String"])
                        # If source file has headers, skip first row
                        if hasheaders:
                            continue
                    
                    # Convert Hex to Binary
                    hexEPC = row[column-1]
                    binary = hex2binary(hexEPC)
                    
                    # Check for SGTIN-96 Coding Scheme (only supported scheme atm)
                    header = binary[:8]
                    if header == "00110000":
                        epcTagURI = binary2epctaguri(binary)
                        epcPureIdentityURI = epctaguri2epcpureidentityuri(epcTagURI)
                        gs1ElementString = epcpureidentityuri2gs1element(epcPureIdentityURI)
                        # Write Row in Results File
                        csvWriter.writerow([hexEPC,epcTagURI,epcPureIdentityURI,gs1ElementString])
                    else:
                        # Write comment about unsupported coding scheme to output file
                        csvWriter.writerow([hexEPC,"Non-SGTIN-96 EPC found => Currently Not Supported!"])

                # Show info that conversion is complete
                messagebox.showinfo(message="HEX EPC Conversion complete!")
except:
    messagebox.showerror(title = "Excpetion", message="An error occurred, please check your input values and retry!")
        

        
