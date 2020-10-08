import json
from uuid import uuid4 as get_uuid
from src.extract import csv_import



def transaction_table() -> list:
    transactions = []
    for row in csv_import:

        transaction = {}

        transaction["Transaction_UUID"] = get_uuid()
        transaction["Timestamp"] = row["Timestamp"]
        transaction["Total_Price"] = row["Cost"]
        transaction["Payment_method"] = row["Payment Type"]
        
        no_digits = []
        for i in row["Card Details"]:
            if not i.isdigit():
                no_digits.append(i)
        
        result = ''.join(no_digits).replace(",","")
        transaction["Card_type"] = result
        
        transactions.append(transaction)
        print(transaction)

print(transaction_table())


def get_location_table():
    location_dict = {}
    for row in csv_import:
        location_dict["Location_UUID"] = get_uuid()
        location_dict["Location_Name"] = row["Location"]
    return location_dict

    
print(get_location_table())
