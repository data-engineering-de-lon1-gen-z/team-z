import json
from uuid import uuid4 as get_uuid
from src.extract import csv_import

def get_name() -> list: 
    # name = []
    for row in csv_import:
        for fullname in csv_import:
            fullname = row["Name"].split(" ")
        # names = {}
        # forename = name[0]
        # surname = name[1]
        # name.append(names)
        print(fullname)


get_name()


# def _remove_duplicate_products(li: list) -> list:
#     dumped_set = set([json.dumps(d, sort_keys=True) for d in li])
#     return [json.loads(s) for s in dumped_set]


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