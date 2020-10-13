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
    # Create database if it does not already exist
    if not database_exists(engine.url):
        create_database(engine.url)

    # Create all the tables
    Base.metadata.create_all(engine)


@event.listens_for(Engine, "before_execute", retval=True)
def _ignore_duplicate(conn, element, multiparams, params):
    if (
        isinstance(element, Insert)
        and "ignore_tables" in conn.info
        and element.table.name in conn.info["ignore_tables"]
    ):
        element = element.prefix_with("IGNORE")
    return element, multiparams, params


@contextmanager
def session_context_manager(ignore_tables=[]):
    session = Session()
    conn = session.connection()
    info = conn.info

    previous = info.get("ignore_tables", ())

    try:
        info["ignore_tables"] = set(ignore_tables)
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
    init()

    from uuid import uuid4

    product = Product(id=str(uuid4()), name="Lemonade", iced=False, price=1.25)
    with session_context_manager() as session:
        insert_many(session, [product])

        # Select query on product table, get the first result
        queried_product = session.query(Product).first()
        print(queried_product.name)
