
import csv
import sys

filename = 'device_attr.csv'    

def addressRead(IP):
    with open(filename,'r',newline='') as csvFile:
        params = csv.reader(csvFile,delimiter=';')
        for row in params:
            # print(f"{row[0]} : {IP}")
            if row[0] == IP:
                return row[6]
    return("Not in database")

def main(argv):
    if len(argv) == 1:
        sys.exit(f"Usage: python {argv[0]} IP_address.")
    elif len(argv) > 2:
        sys.exit(f"Usage: python {argv[0]} IP_address.") 
    print(addressRead(argv[1]))         

if __name__ == "__main__":
    main(sys.argv)