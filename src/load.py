from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, create_database

from src.models import Base, Product, Location, Basket, Transaction

# TODO from src.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD

engine: Engine = create_engine(
    "mysql+pymysql://root:password@localhost:33066/dev?charset=latin1"
)
Session = sessionmaker(bind=engine)


@contextmanager
def session_context_manager():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def insert_many(session, data: list):
    session.add_all(data)


if __name__ == "__main__":
    # Create database if it does not already exist
    if not database_exists(engine.url):
        create_database(engine.url)

    # Create all the tables
    Base.metadata.create_all(engine)

    from uuid import uuid4

    product = Product(id=str(uuid4()), name="Lemonade", iced=False, price=1.25)
    with session_context_manager() as session:
        insert_many(session, [product])

        # Select query on product table, get the first result
        queried_product = session.query(Product).first()
        print(queried_product.name)
