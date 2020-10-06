import pandas as pd
from sqlalchemy import Table, Column, String, Integer, DECIMAL, create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database

from extract import csv_import

db = create_engine('mysql+pymysql://root:password@localhost:33066/dev?charset=latin1')
# Create database if it does not already exist
if not database_exists(db.url):
    create_database(db.url)

meta = MetaData()
db.connect()

def remove_duplicates(dict, list):
    if dict not in list:
        list.append(dict)


customers_list = []     # Customers transform
for row in csv_import:
    dict = {}
    name = row['Name'].split(' ')
    dict['First name'] = name[0]
    dict['Last name'] = name[1]
    remove_duplicates(dict, customers_list)


# Products transform 
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

        # Don't append duplicates
        remove_duplicates(dict, product_list)


# Unique product
unique_products = {}
for i in product_list:
    existing = unique_products.get(i['Name'])
    if not existing:
        unique_products[i['Name']] = i['Price']
    else:
        if existing > i['Price']:
            unique_products[i['Name']] = i['Price']

# Create tables
customers_table = Table(
    'customers', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String(255), nullable=False),
    Column('last_name', String(255), nullable=False)
)
products_table = Table(
    'products', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False),
    Column('price', DECIMAL(4, 2))
)

meta.create_all(db)


# Load tables 
for key, value in unique_products.items():
    products_sql = 'INSERT IGNORE INTO products (name, price) VALUES (%s, %s)'
    db.execute(products_sql, (key, value))

customers_sql = "INSERT IGNORE INTO customers (first_name, last_name) VALUES (%s, %s)"
db.execute(customers_sql, (customers_list))
