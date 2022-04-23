import json
import os
import string
import random

import boto3

URL_TABLE = os.environ["DYNAMODB_TABLE"]
DNS_RECORD = os.environ["DNS_RECORD"]
dynamodb_client = boto3.client("dynamodb")


def handler(event, context):
    event_body = event.get("body")

    if not event_body:
        return {"statusCode": 400, "body": json.dump({"error": "empty"})}

    request_body = json.loads(event_body)

    long_url = request_body.get("long_url")

    if not long_url:
        return {"statusCode": 400, "body": json.dump({"error": "long_url is required"})}
    print(long_url, URL_TABLE)
    # generate primary key for DynamoDB table
    url_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

    dynamodb_client.put_item(
        TableName=URL_TABLE,
        Item={
            "url_id": {"S": url_id},
            "long_url": {"S": long_url}
        }
    )

    # create short_url
    short_url = DNS_RECORD + url_id
    print(short_url, url_id)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "url_id": url_id,
            "short_url": short_url,
        })
    }
