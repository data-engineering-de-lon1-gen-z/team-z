import os
import csv


# TODO Add S3 bucket url to .env
#s3_base_url = os.environ["S3_BASE_URL"]

# Function to convert CSV files to list of dictionaries
def read_csv(file_name):
    with open(file_name) as csvfile: #opens csv file and says that every new line is just "" aka a space (stops new lines in between rows)
        reader = list(csv.DictReader(csvfile, fieldnames = ('Timestamp', 'Location', 'Name', 'Orders','Payment Type','Cost','Card Details')))
    return reader

if __name__ == "__main__":  
    print(read_csv('2020-10-01.csv'))


# Fetches the csv file from the S3 bucket
#def fetch_csv(path: str, headers: list):
#    return pd.read_csv(path, names=headers, engine='python')


#def extract_data(filename: str, headers: list):
#    data = fetch_csv(f"{s3_base_url}/{filename}", headers)
#    return data.to_dict(orient='records')