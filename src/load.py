from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, create_database

from src.models import Base, Product, Location, Basket, Transaction

# TODO from src.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD

if __name__ == "__main__":
    engine: Engine = create_engine(
        "mysql+pymysql://root:password@localhost:33066/dev?charset=latin1"
    )
    # Create database if it does not already exist
    if not database_exists(engine.url):
        create_database(engine.url)

    engine.connect()

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    from uuid import uuid4

    product = Product(id=str(uuid4()), name="Lemonade", iced=False, price=1.25)
    session.add(product)

    # TODO Don't forget to commit

    queried_product = session.query(Product).first()
    print(queried_product.name)
