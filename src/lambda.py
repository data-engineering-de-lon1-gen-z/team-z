import json
import boto3
from src.app import entrypoint


def handler(event, context):
    print(json.dumps(event))

    s3 = event["Records"][0]["s3"]
    obj = s3["object"]

    bucket = s3["bucket"]["name"]
    file_key = obj["key"]
    # e_tag = obj["eTag"]

    print(f"Processing s3://{bucket}/{file_key}")

    s3 = boto3.client("s3")
    print("Established client")
    response = s3.get_object(Bucket=bucket, Key=file_key)  # , IfMatch=e_tag)
    print(response)

    # Read the data as UTF-8 and split at newline char
    lines = response["Body"].read().decode("utf-8").splitlines()
    entrypoint(lines)

    return {
        "statusCode": 200,
    }
