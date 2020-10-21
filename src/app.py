import boto3

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


def entrypoint(bucket, file_path):
    s3 = boto3.client("s3")
    f = s3.get_object(Bucket=bucket, Key=file_path)
    # Read the data as UTF-8 and split at newline char
    raw = f["Body"].read().decode("utf-8").splitlines()
    main(raw)


# Entrypoint to the app from a lambda, takes the bucket and path to csv file
def main(raw):
    # TODO Handle exceptions in file reading
    data = read_csv(raw)

    transactions = get_raw_transactions(data)
    products = get_unique_products(transactions)
    locations = get_locations(transactions)

    init()
    with session_context_manager(ignore_tables=["location", "product"]) as session:
        insert_many(session, products, locations)

        basket_items = get_basket_items(session, transactions)
        transactions = get_transactions(session, transactions)

        insert_many(session, transactions, basket_items)


if __name__ == "__main__":
    raw = None
    with open("/home/matt/Downloads/files/2020-10-20-Westminster.csv", "r") as f:
        raw = f.read().splitlines()

    # Make sure we are closing the file before processing the ETL
    main(raw)
