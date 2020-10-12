import json
from itertools import chain
from uuid import uuid4 as get_uuid
from src.extract import csv_import


def _deduplicate_products(li: list) -> list:
    """
    Deduplicates the products list so we are left with a list of unique products

    Parameters
    ----------
    li: list
        The unsanitary list of products

    Returns
    -------
    list
        A list of unique products
    """

    # The dictionary is encoded serialized into json formar and placed into a
    # set which cannot contain duplicate entries
    # Each json string is then transformed back into a dictionary and returned
    dumped_set = set([json.dumps(d, sort_keys=True) for d in li])
    return [json.loads(s) for s in dumped_set]


def _basket(order: list) -> list:
    """
    Split the orders section of a transaction into a list of dict containing
    name, flavour, size, price and iced keys and values

    Parameters
    ----------
    order: list
        The order section of the transaction split at the comma delimiter

    Returns
    -------
    list
        A basket which contains all products purchased in this transaction
    """

    result = []
    for i in range(0, len(order), 3):
        product = {}

        # If name section in the order string contains the dash character, then
        # there is usually a flavour included.
        if "-" in order[i + 1]:
            product_split = order[i + 1].split(" - ")
            product["name"] = product_split[0]
            product["flavour"] = product_split[1]
        else:
            product["name"] = order[i + 1]
            product["flavour"] = "NULL"

        # If the size section is empty then we just leave it set to `None`
        product["size"] = None if not order[i] else order[i]
        product["price"] = float(order[i + 2])

        # Default to non-iced
        product["iced"] = False
        # Remove these sections from the name
        for remove in ["Flavoured ", "Speciality ", "Iced "]:
            if remove in product["name"]:
                # The name should be capitalized
                product["name"] = product["name"].replace(remove, "").capitalize()
                # If we are removing Iced then toggle the dictionary entry `iced`
                if remove == "Iced ":
                    product["iced"] = True

        result.append(product)

    return result


def get_transactions() -> list:
    """
    Transform and clean the raw data from the CSV file into a list of transactions
    in which we are able to find unique products and locations. Each transaction
    is assigned a UUID string

    Returns
    -------
    list
        A list of transactions along with the basket of items purchased in the transaction.
    """

    transactions = []  # Each transaction contains a basket

    for row in csv_import:
        # Split the comma delimited order section and pass that into the
        # `_basket()` function
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
    """
    Extract a list of unique products from the transactions list. Each
    product is assigned a UUID string

    Returns
    -------
    list
        A list containing the unique products as dictionaries
    """

    return [
        # Add UUID string to each basket
        dict(d, **{"id": str(get_uuid())})
        # Create one giant list of products and deduplicate the list so we end
        # up only with the unique products
        for d in _deduplicate_products(
            list(chain.from_iterable([d["basket"] for d in transactions]))
        )
    ]


def get_locations(transactions: list) -> list:
    """
    Extract a list of unique locations from the transactions list. Each
    location is assigned a UUID string

    Returns
    -------
    list
        A list containing the unique locations as dictionaries
    """

    return [
        {
            "id": str(get_uuid()),
            "name": location,
        }
        for location in set(d["location"] for d in transactions)
    ]


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
