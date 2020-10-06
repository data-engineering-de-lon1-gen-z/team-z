import pandas as pd
from sqlalchemy import Table, Column, String, Integer, DECIMAL, create_engine, MetaData

db = create_engine('mysql+pymysql://admin:Qe93QXUK2g2Y3n@mysql-team-z-dev.cf7fmv3wj2yd.eu-west-1.rds.amazonaws.com/dev')
meta = MetaData()
db.connect()


def csv_to_dict(file: str, headers: list):  # Function to convert CSV files to list of dictionaries
    df = pd.read_csv(file, names=headers, engine='python')
    my_dict = df.to_dict(orient='records')
    return my_dict


headers = ['Timestamp', 'Location', 'Name', 'Orders', 'Payment Type', 'Cost', 'Card Details']
a = csv_to_dict('2020-10-01.csv', headers)

remove_list = ['Flavoured ', 'Speciality ', 'Iced ']
product_list = []
for row in a:
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
        if dict not in product_list:
            product_list.append(dict)


unique_products = {}
for i in product_list:
    existing = unique_products.get(i['Name'])
    if not existing:
        unique_products[i['Name']] = i['Price']
    else:
        if existing > i['Price']:
            unique_products[i['Name']] = i['Price']

products_table = Table(
    'products', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(25), unique=True, nullable=False),
    Column('price', DECIMAL(4, 2))
)


meta.create_all(db)

for key, value in unique_products.items():
    sql = 'INSERT IGNORE INTO products (name, price) VALUES (%s, %s)'
    db.execute(sql, (key, value))
