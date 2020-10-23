from csv import DictReader

COLUMN_HEADERS = [
    "Timestamp",
    "Location",
    "Name",
    "Orders",
    "Payment Type",
    "Cost",
    "Card Details",
]

def read_csv(f):
    reader = DictReader(f, fieldnames=COLUMN_HEADERS)
    return list(reader)

if __name__ == "__main__":
    with open("2020-10-01.csv", "r") as f:
        print(len(read_csv(f)))
