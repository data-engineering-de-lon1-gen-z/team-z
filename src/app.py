from src.transform import get_raw_transactions
from src.load import (
    get_unique_products,
    get_locations,
    get_basket_items,
    get_transactions,
    init,
    session_context_manager,
    insert_many,
)

if __name__ == "__main__":
    transactions = get_raw_transactions()
    products = get_unique_products(transactions)
    locations = get_locations(transactions)

    init()
    with session_context_manager(ignore_tables=["location", "product"]) as session:
        insert_many(session, products)
        insert_many(session, locations)

        basket_items = get_basket_items(session, transactions)
        transactions = get_transactions(session, transactions)

        insert_many(session, transactions)
        insert_many(session, basket_items)
