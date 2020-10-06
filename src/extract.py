import os
import pandas as pd

# TODO Add S3 bucket url to .env
#s3_base_url = os.environ["S3_BASE_URL"]


# Function to convert CSV files to list of dictionaries
def csv_to_dict(file, headers):
    df = pd.read_csv(file, names=headers, engine='python')
    my_dict = df.to_dict(orient='records')
    return my_dict

headers = ['Timestamp', 'Location', 'Name', 'Orders', 'Payment Type', 'Cost', 'Card Details']
csv_import = csv_to_dict('2020-10-01.csv', headers)


# Fetches the csv file from the S3 bucket
#def fetch_csv(path: str, headers: list):
#    return pd.read_csv(path, names=headers, engine='python')


#def extract_data(filename: str, headers: list):
#    data = fetch_csv(f"{s3_base_url}/{filename}", headers)
#    return data.to_dict(orient='records')