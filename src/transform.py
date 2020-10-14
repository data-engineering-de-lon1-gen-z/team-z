from uuid import uuid4 as get_uuid
from src.extract import csv_import


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

        product["name"] = product["name"].title()
        if product["flavour"]:
            product["flavour"] = product["flavour"].title()

        product["iced"] = False
        for remove in ["Flavoured ", "Speciality ", "Iced "]:
            if remove in product["name"]:
                product["name"] = product["name"].replace(remove, "")
                if remove == "Iced ":
                    product["iced"] = True

        result.append(product)

    return result


def get_raw_transactions() -> list:
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


if __name__ == "__main__":
    transactions = get_raw_transactions()
    print(f"Number of transactions: {len(transactions)}")
