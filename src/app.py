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
    locations = get_locations(transactions)
    products = get_unique_products(transactions)

    basket_items = []
    for d in transactions:
        basket_items += (
            x
            for x in set(
                BasketItem(
                    id=str(get_uuid()),
                    transaction_id=d["id"],
                    product_id=next(
                        x for x in products if b == _dict_without_key(x, "id")
                    )["id"],
                    quantity=d["basket"].count(b),
                )
                for b in d["basket"]
            )
        )

    transactions = [
        Transaction(
            id=d["id"],
            datetime=d["datetime"],
            location_id=next(x for x in locations if d["location"] == x["name"])["id"],
        )
        for d in transactions
    ]

    products = [Product(**d) for d in products]
    locations = [Location(**d) for d in locations]

    init()
    with session_context_manager() as session:
        insert_many(session, products)
        insert_many(session, locations)
        insert_many(session, transactions)
        insert_many(session, basket_items)
