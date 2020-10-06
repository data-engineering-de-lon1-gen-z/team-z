from sqlalchemy import Table, Column, String, Integer, DECIMAL, create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database, CHAR
from src.transform import unique_products, customer_list, flavours_list, get_uuid


db = create_engine('mysql+pymysql://root:password@localhost:33066/dev?charset=latin1')
# Create database if it does not already exist
if not database_exists(db.url):
    create_database(db.url)

meta = MetaData()
db.connect()

customers_table = Table(
    'customers', meta,
    Column('UUID', CHAR(36), primary_key=True, unique=True),
    Column('first_name', String(255), nullable=False),
    Column('last_name', String(255), nullable=False)
)
products_table = Table(
    'products', meta,
    Column('UUID', CHAR(36), primary_key=True, unique=True),
    Column('name', String(60), unique=True, nullable=False),
    Column('price', DECIMAL(4, 2))
)
flavours_table = Table(
    'flavours', meta,
    Column('UUID', CHAR(36)), primary_key=True, unique=True),
    Column('name', String(60), unique=True)
)

meta.create_all(db)   # Creates all tables above in db 


# Load tables 
for key, value in unique_products.items():
    products_sql = 'INSERT IGNORE INTO products (name, price) VALUES (%s, %s)'
    db.execute(products_sql, (key, value))

customers_sql = "INSERT IGNORE INTO customers (UUID, first_name, last_name) VALUES (%s, %s, %s)"
db.execute(customers_sql, (customers_list))

flavours_sql = "INSERT IGNORE INTO flavours (UUID, name) VALUES (%s, %s, %s)"
db.execute(flavours_sql, (flavours_list))