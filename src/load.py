import json
from uuid import uuid4 as get_uuid
from itertools import chain
from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import Insert

from src.models import Base, Product, Location, BasketItem, Transaction

# TODO from src.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD

engine: Engine = create_engine("mysql+pymysql://root:password@localhost:33066/dev")
Session = sessionmaker(bind=engine)


def _deduplicate_products(li: list) -> list:
    dumped_set = set([json.dumps(d, sort_keys=True) for d in li])
    return [json.loads(s) for s in dumped_set]


def get_unique_products(transactions: list) -> list:
    return [
        Product(**dict(d, **{"id": str(get_uuid())}))
        for d in _deduplicate_products(
            list(chain.from_iterable([d["basket"] for d in transactions]))
        )
    ]


def get_locations(transactions: list) -> list:
    locations = [
        Location(id=str(get_uuid()), name=location)
        for location in set(d["location"] for d in transactions)
    ]
    return locations


def get_basket_items(session, transactions: list) -> list:
    basket_items = []
    for d in transactions:
        basket_items += (
            x
            for x in set(
                BasketItem(
                    id=str(get_uuid()),
                    transaction_id=d["id"],
                    product_id=session.query(Product.id)
                    .filter_by(
                        name=b["name"],
                        flavour=b["flavour"],
                        size=b["size"],
                        iced=b["iced"],
                    )
                    .as_scalar(),
                    quantity=d["basket"].count(b),
                )
                for b in d["basket"]
            )
        )

    return basket_items


def get_transactions(session, raw_transactions: list) -> list:
    return [
        Transaction(
            id=d["id"],
            datetime=d["datetime"],
            location_id=session.query(Location.id)
            .filter_by(name=d["location"])
            .as_scalar(),
        )
        for d in raw_transactions
    ]


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


def init():
    # Create database if it does not already exist
    if not database_exists(engine.url):
        create_database(engine.url)

    # Create all the tables
    Base.metadata.create_all(engine)


def insert_many(session, data: list):
    session.add_all(data)
