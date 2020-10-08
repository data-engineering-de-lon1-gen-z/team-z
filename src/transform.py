import json
from uuid import uuid4 as get_uuid
from src.extract import csv_import



def transaction_table() -> list:
    transactions = []
    for row in csv_import:

        transaction = {}

        transaction["Transaction_UUID"] = get_uuid()
        transaction["Timestamp"] = row["Timestamp"]
        # transaction["Location_ID"]
        # transaction["Order_ID"] 
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


# def _remove_duplicate_products(li: list) -> list:
#     dumped_set = set([json.dumps(d, sort_keys=True) for d in li])
#     return [json.loads(s) for s in dumped_set]


def get_location_table():
    location_dict = {}
    for row in csv_import:
        location_dict["Location_UUID"] = get_uuid()
        location_dict["Location_Name"] = row["Location"]
    return location_dict

    
print(get_location_table())

# def create_product_list() -> list:
#     products = []

#     for row in csv_import:
#         order = row["Orders"].split(",")

#         for i in range(0, len(order), 3):
#             product = {}

#             if "-" in order[i + 1]:
#                 product_split = order[i + 1].split(" - ")
#                 product["Name"] = product_split[0]
#                 product["Flavour"] = product_split[1]
#             else:
#                 product["Name"] = order[i + 1]
#                 product["Flavour"] = "NULL"

#             product["Size"] = None if not order[i] else order[i]
#             product["Price"] = float(order[i + 2])

#             product["Iced"] = False
#             for remove in ["Flavoured ", "Speciality ", "Iced "]:
#                 if remove in product["Name"]:
#                     product["Name"] = product["Name"].replace(remove, "").capitalize()
#                     if remove == "Iced ":
#                         product["Iced"] = True

#             products.append(product)

#     return [
#         dict(d, **{"Product_ID": get_uuid()})
#         for d in _remove_duplicate_products(products)
#     ]


# if __name__ == "__main__":
#     products = create_product_list()
#     for p in products:
#         print(p)

#     print(len(products))

