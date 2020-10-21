import json
from src.app import entrypoint


def handler(event, context):
    print(json.dumps(event))
    # Loop over any records included, incase multiple files have been uploaded
    # for record in event["Records"]:
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    file_key = record["s3"]["object"]["key"]
    print(f"Processing {file_key}")
    entrypoint(bucket, file_key)
