#### CONSTANTS #####
gcpBits = [40,37,34,30,27,24,20]
gcpDigits = [12,11,10,9,8,7,6]
itemRefBits = [4,7,10,14,17,20,24]
itemRefDigits = [1,2,3,4,5,6,7]

##### UTILITY FUNCTIONS #####
### Function hex2binary to convert a hex value to binary string with leading zeroes
def hex2binary(hexvalue):
    base = 16 ## hexadecimal base
    num_of_bits = 4 * len(hexvalue)
    return bin(int(hexvalue, base))[2:].zfill(num_of_bits)

### Function binary2gcp to determine the GCP from a binary EPC
def binary2gcp(binary, partition):
    gcpBitLength = gcpBits[partition]
    gcpBinary = binary[14:(14+gcpBitLength)]
    gcpLength = gcpDigits[partition]
    return str(int(gcpBinary,2)).zfill(gcpLength)

### Function binary2itemref to determine the ItemRef from a binary EPC
def binary2itemref(binary, partition):
    gcpBitLength = gcpBits[partition]
    itemRefBitLength = itemRefBits[partition]
    itemRefBinary = binary[(14+gcpBitLength):(14+gcpBitLength+itemRefBitLength)]
    itemRefLength = itemRefDigits[partition]
    return str(int(itemRefBinary,2)).zfill(itemRefLength)

### Function binary2serial to determine the serial from a binary EPC
def binary2serial(binary, partition):
    gcpBitLength = gcpBits[partition]
    itemRefBitLength = itemRefBits[partition]
    serialBinary = binary[(14+gcpBitLength+itemRefBitLength):]
    return str(int(serialBinary, 2))

### Function binary2epctaguri to determine EPC Tag URI from a binary EPC
def binary2epctaguri(binary):
    epcTagURI = "urn:epc:tag:sgtin-96:"
    
    # Determine Filter Value
    filterValue = int(binary[8:11])

    # Append Filter Value to EPCTagURI
    epcTagURI += str(filterValue)
    epcTagURI += "."

    # Determine Partition
    partition = int(binary[11:14],2)

    # Determine GCP and append to EPCTagURI
    gcp = binary2gcp(binary, partition)
    epcTagURI += gcp
    epcTagURI += "."

    # Determine Item Reference and append to EPCTagURI
    itemRef = binary2itemref(binary, partition)    
    epcTagURI += itemRef
    epcTagURI += "."

    # Determine Serial and append to EPCTagURI
    serial = binary2serial(binary, partition)

    # Append GCP and Item Reference to EPCTagURI
    epcTagURI += serial

    return epcTagURI

### Function epctaguri2epcpureidentityuri to determine the EPC Pure Identity URI from a EPC Tag URI
def epctaguri2epcpureidentityuri(epctaguri):
    epcPureIdentityURI = "urn:epc:id:sgtin:"
    epcTagURIParts = epctaguri.split('.',1)
    epcPureIdentityURI += epcTagURIParts[1]
    return epcPureIdentityURI

### Function calculateCheckDigit to calculate the check digit for a GTIN
def calculateCheckDigit(gtin):
    return (10 - ((3 * (int(gtin[0]) + int(gtin[2])  + int(gtin[4]) + int(gtin[6]) + int(gtin[8]) + int(gtin[10]) + int(gtin[12])) + (int(gtin[1]) + int(gtin[3]) + int(gtin[5]) + int(gtin[7]) + int(gtin[9]) + int(gtin[11])))%10))   

### Function epcpureidentityuri2gs1element to convert EPC Pure Identity URI to GS1 Element String
def epcpureidentityuri2gs1element(epcPureIdentityURI):
    # Strip Prefix
    strippedURI = epcPureIdentityURI.replace("urn:epc:id:sgtin:","")

    # Split URI to GS1 Elements
    splits = strippedURI.split(".")
    gcp = splits[0]
    indicator = splits[1][:1]
    itemRef = splits[1][1:]
    serial = splits[2]

    # Assemble GTIN without Check Digit
    gtinWithoutCheckDigit = indicator + gcp + itemRef

    # Calculate Check Digit
    checkDigit = calculateCheckDigit(gtinWithoutCheckDigit)
    gtin = gtinWithoutCheckDigit + str(checkDigit)

    # Assemble GS1 Element String
    return "(01)" + gtin + "(21)" + serial