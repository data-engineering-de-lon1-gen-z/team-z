from src.extract import csv_import

import pandas as pd
import uuid

def remove_duplicates(dict, list):  # Remove duplicated function
    if dict not in list:
        list.append(dict)

def get_uuid():
    return uuid.uuid4()

# Customers table transform
customers_list = []     # List of dictionaries to be created
for row in csv_import:
    dict = {}
    name = row['Name'].split(' ')
    dict['Customer_UUID'] = get_uuid()
    dict['First name'] = name[0]
    dict['Last name'] = name[1]
    remove_duplicates(dict, customers_list)


# Products table transform 
remove_list = ['Flavoured ', 'Speciality ', 'Iced ']  
product_list = []
for row in csv_import:   
    order = row["Orders"].split(",")

    for i in range(0, len(order), 3):
        dict = {}

        dict['Size'] = None if not order[i] else order[i]

        if '-' in order[i + 1]:
            product_split = order[i + 1].split(' - ')
            dict['Name'] = product_split[0]
            dict['Flavour'] = product_split[1]
        else:
            dict['Name'] = order[i + 1]

        for remove in remove_list:
            if remove in dict['Name']:
                dict['Name'] = dict['Name'].replace(remove, '').capitalize()
                if remove == 'Iced':
                    dict['is_iced'] = True


        dict['Price'] = float(order[i + 2])

        remove_duplicates(dict, product_list)

# Create flavours table
flavours = []
# for product in product_list:
#     dict = {}
#     if product['Flavour'] not in flavours:
#         dict['Flavour'] = product['Flavour']
#         flavours.append(product['Flavour'])


unique_products = {} # Unique product dictionary created
for i in product_list:
    existing = unique_products.get(i['Name'])
    if not existing:
        unique_products[i['Name']] = i['Price']
    else:
        if existing > i['Price']:
            unique_products[i['Name']] = i['Price']


