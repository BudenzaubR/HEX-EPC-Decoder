#Imports
import csv
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
from tkinter import messagebox
from epcutils import binary2epctaguri, epcpureidentityuri2gs1element, epctaguri2epcpureidentityuri, hex2binary

########## MAIN PROGRAMM ##########
### Start of conversion ###
# Process CSV to convert HEX EPCs to all other formats
# Output is written to results.csv
def convert():        
    try:        
        with open(filename.get()) as csvdatei:
            csvReader = csv.reader(csvdatei, delimiter=delimiter.get())
            with open("results.csv",'w', newline='') as outputFile:
                    csvWriter = csv.writer(outputFile, delimiter=delimiter.get())
                    
                    for n, row in enumerate(csvReader):
                        # Check for empty row
                        if not row:
                            continue
                        
                        # If in first object check for header row
                        if n == 0:
                            # Write header line for output file
                            csvWriter.writerow(["HEX EPC","EPC Tag URI","EPC Pure Identity URI","GS1 Element String"])
                            # If source file has headers, skip first row
                            if hasheaders.get():
                                continue
                        
                        # Convert Hex to Binary
                        hexEPC = row[int(column.get())-1]
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
        messagebox.showerror(title = "Exception", message="An error occurred, please check your input values and retry!")

# Function to open the CSV file
def open_file():
    filename.set(askopenfilename(title="Select CSV File"))

### User Input ###
# Open main window
root = Tk()
#root.geometry("600x400")
root.resizable(False,False)
root.title("EPC HEX Decoder")

# Main Frame
mainframe = ttk.Frame(root, padding=10)
mainframe.grid()

# Input CSV File
fileframe = ttk.LabelFrame(mainframe, text="CSV File:", padding=10)
fileframe.grid(row=0, column=0, columnspan=2)

filename = StringVar()
csventry = ttk.Entry(fileframe, textvariable=filename, width=60, state=DISABLED)
csventry.grid(row=0, column=0, sticky=EW, padx=10, pady=5)

csvopendialogbutton = ttk.Button(fileframe, text="Select file", command=open_file)
csvopendialogbutton.grid(row=0, column=1, sticky=E)

# Input if CSV has Headers
headerframe = ttk.LabelFrame(mainframe, text="Has the CSV headers?:", padding=10)
headerframe.grid(row=1, column=0, sticky=W, rowspan=2)

hasheaders = BooleanVar()
hasheaders.set(False)
headercheckbox = ttk.Checkbutton(headerframe, text="Headers?", variable=hasheaders)
headercheckbox.grid(row=0, column=0, sticky=W, padx=10, pady=5)

# Input Delimiter
delimiterframe = ttk.LabelFrame(mainframe, text="Select the delimiter:", padding=10)
delimiterframe.grid(row=3, column=0, sticky=W, rowspan=2)

delimiter = StringVar()
delimiter.set(",")
rb1 = ttk.Radiobutton(delimiterframe, text=",",value=",",variable=delimiter)
rb1.grid(row=0, column=0, sticky=W, padx=10)

rb1 = ttk.Radiobutton(delimiterframe, text=";",value=";",variable=delimiter)
rb1.grid(row=1, column=0, sticky=W, padx=10)

# Input Column No.
columnframe = ttk.LabelFrame(mainframe, text="In which column are the HEX EPCs?:", padding=10)
columnframe.grid(row=6, column=0, sticky=W)
column = StringVar()
column.set(1)
columnentry = ttk.Entry(columnframe, textvariable=column, width=1)
columnentry.grid(row=0, column=0, sticky=W, padx=10)

# Convert Button
csvconvertbutton = ttk.Button(mainframe, text="Convert", command=convert)
csvconvertbutton.grid(row=8, column=0, sticky=W)

# Exit Button
exitbutton = ttk.Button(mainframe, text="Exit", command=root.destroy)
exitbutton.grid(row=8, column=1, sticky=W)

root.mainloop()

# Input CSV File Path
#filename = askopenfilename(title="Select CSV File") # show an "Open" dialog box and return the path to the selected file
#filename = "hex.csv"

#hasheaders = messagebox.askyesno("CSV Headers", "Does the CSV-File contain headers?")
#hasheaders = True

# Input CSV Delimiter
#delimiter = simpledialog.askstring("CSV Delimiter", "Which delimiter is used?")
#delimiter = ','

# Input HEX EPC Column
#column = simpledialog.askinteger("EPC Column", "In which column are the Hex EPCs?")
column = 1