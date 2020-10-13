import json
from itertools import chain
from uuid import uuid4 as get_uuid
from src.extract import csv_import


def _deduplicate_products(li: list) -> list:
    dumped_set = set([json.dumps(d, sort_keys=True) for d in li])
    return [json.loads(s) for s in dumped_set]


def _basket(order: list) -> list:
    result = []
    for i in range(0, len(order), 3):
        product = {}

        if "-" in order[i + 1]:
            product_split = order[i + 1].split(" - ")
            product["name"] = product_split[0]
            product["flavour"] = product_split[1]
        else:
            product["name"] = order[i + 1]
            product["flavour"] = ""

        product["size"] = "" if not order[i] else order[i]
        product["price"] = float(order[i + 2])

        product["iced"] = False
        for remove in ["Flavoured ", "Speciality ", "Iced "]:
            if remove in product["name"]:
                product["name"] = product["name"].replace(remove, "").capitalize()
                if remove == "Iced ":
                    product["iced"] = True

        result.append(product)

    return result


def get_transactions() -> list:
    transactions = []  # Each transaction contains a basket

    # TODO Each row is a new transaction
    for row in csv_import:
        order = row["Orders"].split(",")
        basket = _basket(order)

        transactions.append(
            {
                "id": str(get_uuid()),
                "basket": basket,
                "datetime": row["Timestamp"],
                "location": row["Location"],
            }
        )

    return transactions


def get_unique_products(transactions: list) -> list:
    return [
        dict(d, **{"id": str(get_uuid())})
        for d in _deduplicate_products(
            list(chain.from_iterable([d["basket"] for d in transactions]))
        )
    ]


def get_locations(transactions: list) -> list:
    locations = [
        {"id": str(get_uuid()), "name": location}
        for location in set(d["location"] for d in transactions)
    ]
    return locations


if __name__ == "__main__":
    transactions = get_transactions()
    unique_products = get_unique_products(transactions)
    locations = get_locations(transactions)

    print(f"Number of transactions: {len(transactions)}")
    print(f"Number of locations: {len(locations)}")
    print(
        f"Number of drinks ordered: {sum([len(transaction['basket']) for transaction in transactions])}"
    )
    print(f"Number of unique products: {len(unique_products)}")
