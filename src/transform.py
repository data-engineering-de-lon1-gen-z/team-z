import json
from itertools import chain
from uuid import uuid4 as get_uuid
from src.extract import csv_import


def _remove_duplicate_products(li: list) -> list:
    dumped_set = set([json.dumps(d, sort_keys=True) for d in li])
    return [json.loads(s) for s in dumped_set]


def _basket(order: list) -> list:
    result = []
    for i in range(0, len(order), 3):
        product = {}

        if "-" in order[i + 1]:
            product_split = order[i + 1].split(" - ")
            product["Name"] = product_split[0]
            product["Flavour"] = product_split[1]
        else:
            product["Name"] = order[i + 1]
            product["Flavour"] = "NULL"

        product["Size"] = None if not order[i] else order[i]
        product["Price"] = float(order[i + 2])

        product["Iced"] = False
        for remove in ["Flavoured ", "Speciality ", "Iced "]:
            if remove in product["Name"]:
                product["Name"] = product["Name"].replace(remove, "").capitalize()
                if remove == "Iced ":
                    product["Iced"] = True

        result.append(product)

    return result


def _get_transactions() -> list:
    transactions = []  # Each transaction contains a basket

    # TODO Each row is a new transaction
    for row in csv_import:
        order = row["Orders"].split(",")
        basket = _basket(order)

        transactions.append(
            {
                "Transaction_ID": get_uuid(),
                "Basket": basket,
                "DateTime": row["Timestamp"],
                "Location": row["Location"],
            }
        )

    return transactions


def _get_unique_products(transactions: list) -> list:
    return [
        dict(d, **{"Product_ID": get_uuid()})
        for d in _remove_duplicate_products(
            list(chain.from_iterable([d["Basket"] for d in transactions]))
        )
    ]


def _get_locations(transactions: list) -> list:
    locations = [
        {"Location_ID": get_uuid(), "Name": location}
        for location in set(d["Location"] for d in transactions)
    ]
    return locations


if __name__ == "__main__":
    transactions = _get_transactions()
    unique_products = _get_unique_products(transactions)
    locations = _get_locations(transactions)

    print(f"Number of transactions: {len(transactions)}")
    print(f"Number of locations: {len(locations)}")
    print(
        f"Number of drinks ordered: {sum([len(transaction['Basket']) for transaction in transactions])}"
    )
    print(f"Number of unique products: {len(unique_products)}")
