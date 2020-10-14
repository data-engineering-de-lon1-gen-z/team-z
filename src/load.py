from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import Insert

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


# Listens for any before_execute event from SQLAlchemy
@event.listens_for(Engine, "before_execute", retval=True)
def _ignore_duplicate(conn, element, multiparams, params):
    # We only want to find any event which contains `ignore_tables` key in connection.info
    if (
        isinstance(element, Insert)
        and "ignore_tables" in conn.info
        and element.table.name in conn.info["ignore_tables"]
    ):
        # Prefix the query with IGNORE so that we can ignore duplicate inserts rather than
        # raising exception
        element = element.prefix_with("IGNORE")
    return element, multiparams, params


@contextmanager
def session_context_manager(ignore_tables=[]):
    """
    Context manager for SQLAlchemy session object, automatically commit changes
    and perform rollbacks on exception and close the connection

    Parameters
    ----------
    ignore_Tables: list
        A list of table names that use `INSERT IGNORE`

    Yields
    -------
    session
        SQLAlchemy Session object

    Example
    -------
    person = Person(id=uuid4(), first_name="John", last_name="Wrightson")
    with session_context_manager() as session:
        session.add(person)
    """

    session = Session()
    conn = session.connection()
    info = conn.info

    # Get the original ignore_tables dict object to be restored before `session.close()`
    previous = info.get("ignore_tables", ())

    try:
        # Set the ignore_tables from the `ignore_tables` param, for session block
        info["ignore_tables"] = set(ignore_tables)
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
