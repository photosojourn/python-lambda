"""
Lambda function template for SQS Processing
The sqs_batch_processor decarator handles spliting the batch of records and
then passes the record to the function record_handler for processing
"""
from secrets import compare_digest
import os
from typing import Any, Dict
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import parameters
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerEventV2,
    APIGatewayAuthorizerResponseV2,
)

# Addiotnal useful imports
# import boto3

ssm_provider = parameters.SSMProvider()
service_name = "my-service"  # Set service name used by Logger/Tracer here

logger = Logger(service=service_name)
tracer = Tracer(service=service_name, disabled=bool(os.environ["ENABLE_XRAY"]))
aws_region = os.environ["AWS_REGION"]
priv_token = ssm_provider.get("/api_token", decrypt=True)


def check_token(token: str) -> bool:
    if compare_digest(token, priv_token):
        return True
    return False


@event_source(data_class=APIGatewayAuthorizerEventV2)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(
    event: APIGatewayAuthorizerEventV2, context: LambdaContext
) -> Dict[str, Any]:
    """
    Main Lambda entry point.

    Parameters
    ----------
    event: APIGatewayAuthorizerEventV2
    context: Lambda context object
    """
    logger.info("Checking secret")

    if check_token(event.get_header_value("x-token")):
        return APIGatewayAuthorizerResponseV2(authorize=True).asdict()
    return APIGatewayAuthorizerResponseV2().asdict()
