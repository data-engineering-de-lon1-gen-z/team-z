from src.extract import read_csv
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

import json


# Entrypoint to the app from a lambda, takes the bucket and path to csv file
def entrypoint(lines):
    # TODO Handle exceptions in file reading
    print("Reading csv")
    data = read_csv(lines)

    print("Cleaning transactions")
    transactions = get_raw_transactions(data)
    print("Unique products")
    products = get_unique_products(transactions)
    print("Unique locations")
    locations = get_locations(transactions)

    print("Initialize db")
    init()
    with session_context_manager(ignore_tables=["location", "product"]) as session:
        insert_many(session, products, locations)

        basket_items = get_basket_items(session, transactions)
        transactions = get_transactions(session, transactions)

        insert_many(session, transactions, basket_items)


if __name__ == "__main__":
    raw = None
    with open("/home/matt/Downloads/files/2020-10-20-Westminster.csv", "r") as f:
        lines = f.read().splitlines()

    # Make sure we are closing the file before processing the ETL
    entrypoint(lines)
