"""
Lambda function template for SQS Processing
The sqs_batch_processor decarator handles spliting the batch of records and
then passes the record to the function record_handler for processing
"""
import os
from typing import Any, Dict
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.batch import sqs_batch_processor

# Addiotnal useful imports
# import boto3
# from aws_lambda_powertools.utilities import parameters

service_name = "my-service"  # Set service name used by Logger/Tracer here

logger = Logger(service=service_name)
tracer = Tracer(service=service_name, disabled=bool(os.environ["ENABLE_XRAY"]))
aws_region = os.environ["AWS_REGION"]


def record_handler(record: SQSRecord):
    """
    Processes each record from the SQS queue

    Parameters
    ----------
    record: SQS message object
      The SQS record to be processed
    """


@logger.inject_lambda_context
@sqs_batch_processor(record_handler=record_handler)
@tracer.capture_lambda_handler
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Main Lambda entry point.

    Parameters
    ----------
    event: Lambda event object
    context: Lambda context object
    """
    logger.info("Something did something")
    return {"statusCode": 200}
