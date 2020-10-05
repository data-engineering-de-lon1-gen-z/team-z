import csv
import pandas as pd
import math
#import numpy

def csv_to_dict(file: str, headers: list):  # Function to convert CSV files to list of dictionaries
    df = pd.read_csv(file, names=headers, engine='python')
    my_dict = df.to_dict(orient='records')
    return my_dict

headers = ['Timestamp', 'Location', 'Name', 'Orders', 'Payment Type', 'Cost', 'Card Details']
a = csv_to_dict('final_project/2020-10-01.csv', headers)

product_list = []
for row in a:
    order = row["Orders"].split(",")

    for i in range(0, len(order), 3):
        dict = {}

        dict['Size'] = 'Regular' if not order[i] else order[i]
        
        if '-' in order[i + 1]:
            product_split = order[i + 1].split(' - ')
            dict['Name'] = product_split[0]
            dict['Flavour'] = product_split[1]
        else:
            dict['Name'] = order[i + 1]
        dict['Price'] = float(order[i + 2])

        # Don't append duplicates
        if dict not in product_list:
            product_list.append(dict)
    

# RUN IT! does that look right?
# NO! WIP
# RUN IT AGAIN! - nvm
# Isnt this a valid product list? But it has duplicates
for i in product_list:
    print(i)
# Now we have a product list right?? - Seems mostly there - still a few errors
# with the wrong flavours for some drinks (ie hot chocolate - carrot kick)
# isn't in csv 
# lol
print(len(product_list))