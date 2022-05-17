"""AWS Lambda sample module"""

import json
import logging
import os

import boto3
from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV2
from aws_lambda_typing.responses import APIGatewayProxyResponseV2

# import requests

logger = logging.getLogger(__name__)
logger.setLevel(os.environ["LOG_LEVEL"])

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def lambda_handler(event: APIGatewayProxyEventV2, context: Context) -> APIGatewayProxyResponseV2:
    """Sample pure Lambda function

    Args:
        event (APIGatewayProxyEventV2):
          API Gateway Lambda Proxy Input Format
          Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format # noqa: E501

        context (Context):
          Lambda Context runtime methods and attributes
          Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns:
        APIGatewayProxyResponseV2:
          responce
          https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    table.put_item(Item={"id": "aaaaa", "item": event["body"]})
    logger.info("successfully put item")

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
