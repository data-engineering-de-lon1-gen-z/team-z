from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, create_database

from src.models import Base, Product, Location, BasketItem, Transaction

# TODO from src.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD

engine: Engine = create_engine(
    "mysql+pymysql://root:password@localhost:33066/dev?charset=latin1"
)
Session = sessionmaker(bind=engine)


def init():
    """
    Initialize the database by creating the database if it does not already
    exist & create all the defined tables
    """

    # Create database if it does not already exist
    if not database_exists(engine.url):
        create_database(engine.url)

    # Create all the tables
    Base.metadata.create_all(engine)


@contextmanager
def session_context_manager():
    """
    Context manager for SQLAlchemy session object, automatically commit changes
    and perform rollbacks on exception and close the connection

    Example
    -------
    person = Person(id=uuid4(), first_name="John", last_name="Wrightson")
    with session_context_manager() as session:
        session.add(person)
    """

    session = Session()
    try:
        # Yield the session object to be used in the with statement
        yield session
        # When session exits scope without exception, the session is commited
        session.commit()
    except:
        # On exception, rollback any changes before raising the exception
        session.rollback()
        raise
    finally:
        # Always close the connection
        session.close()


def insert_many(session, *argv):
    """
    Insert many rows into the database, each arg given must be an iterable
    containing some valid ORM class

    Parameters
    ----------
    session: Session
        The session object obtained from the `session_context_manager()` function
    """

    for data in argv:
        session.add_all(data)


if __name__ == "__main__":
    init()

    from uuid import uuid4

    product = Product(id=str(uuid4()), name="Lemonade", iced=False, price=1.25)
    with session_context_manager() as session:
        insert_many(session, [product])

        # Select query on product table, get the first result
        queried_product = session.query(Product).first()
        print(queried_product.name)
