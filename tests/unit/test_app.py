import json
import os

import boto3
import pytest
from moto import mock_dynamodb2
from mypy_boto3_dynamodb.service_resource import Table


@pytest.fixture()
def table() -> Table:
    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb")
        yield dynamodb.create_table(
            TableName=os.environ["DYNAMODB_TABLE"],
            KeySchema=[{"KeyType": "HASH", "AttributeName": "id"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )


@pytest.mark.parametrize("id", ["aaaaa", "bbbbb"])
def test_lambda_handler(table: Table, id: str):
    from hello_world import app

    resp = app.lambda_handler({"body": json.dumps({"id": id})}, {})
    assert table.get_item(Key={"id": id}) is not None
    assert resp["statusCode"] == 200
    assert json.loads(resp["body"]).items() >= {"message": "hello world"}.items()
