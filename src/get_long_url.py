import json
import os

import boto3

URL_TABLE = os.environ["DYNAMODB_TABLE"]
dynamodb_client = boto3.client("dynamodb")


def handler(event, context):
    url_id = event['pathParameters']["url_id"]
    print(url_id)
    result = dynamodb_client.get_item(
        TableName=URL_TABLE,
        Key={"url_id": {"S": url_id}}).get("Item")
    if not result:
        return {"statusCode": 404, "body": json.dump({"error": "URL not found"})}

    long_url = result.get("long_url").get("S")

    # make redirect to long_url
    response = {
        "headers": {"Location": long_url},
        "statusCode": 301,
    }
    return response
