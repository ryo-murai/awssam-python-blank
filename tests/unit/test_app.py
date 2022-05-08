import json

import boto3
import pytest
from moto import mock_dynamodb2


@pytest.fixture()
def table():
    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb")
        yield dynamodb.create_table(
            TableName="hoge",
            KeySchema=[{"KeyType": "HASH", "AttributeName": "id"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )


def test_lambda_handler(table):
    from hello_world import app

    app.lambda_handler({"body": json.dumps({"id": "aaaaa"})}, {})
    assert table.get_item(Key={"id": "aaaaa"}) is not None
