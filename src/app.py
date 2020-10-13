from uuid import uuid4 as get_uuid
from itertools import chain
from src.transform import (
    get_transactions,
    get_locations,
    get_unique_products,
)
from src.load import init, session_context_manager, insert_many

from src.models import Product, Location, BasketItem, Transaction


def _dict_without_key(d, key):
    result = d.copy()
    result.pop("id")
    return result


if __name__ == "__main__":

    transactions = get_transactions()
    products = [Product(**d) for d in get_unique_products(transactions)]
    locations = [Location(**d) for d in get_locations(transactions)]

    init()
    with session_context_manager(ignore_tables=["location", "product"]) as session:
        insert_many(session, products)
        insert_many(session, locations)

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

        transactions = [
            Transaction(
                id=d["id"],
                datetime=d["datetime"],
                location_id=session.query(Location.id)
                .filter_by(name=d["location"])
                .as_scalar(),
            )
            for d in transactions
        ]

        insert_many(session, transactions)
        insert_many(session, basket_items)
