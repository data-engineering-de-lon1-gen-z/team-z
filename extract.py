import pandas as pd
from sqlalchemy import Table, Column, String, Integer, DECIMAL, create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database

db = create_engine('mysql+pymysql://root:password@localhost:33066/dev?charset=latin1')
# Create database if it does not already exist
if not database_exists(db.url):
    create_database(db.url)

meta = MetaData()
db.connect()

def csv_to_dict(file: str, headers: list):  # Function to convert CSV files to list of dictionaries
    df = pd.read_csv(file, names=headers, engine='python')
    my_dict = df.to_dict(orient='records')
    return my_dict

headers = ['Timestamp', 'Location', 'Name', 'Orders', 'Payment Type', 'Cost', 'Card Details']
csv_import = csv_to_dict('2020-10-01.csv', headers)