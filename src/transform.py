import json
from uuid import uuid4 as get_uuid
from src.extract import csv_import

def get_name() -> list: 
    for row in csv_import:
        for fullname in csv_import:
            fullname = row["Name"].split(" ")
        print(fullname)


get_name()
