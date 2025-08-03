"""AWS configuration module.

This module handles the AWS service configurations for the application.
"""
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

class AWSConfig:
    """AWS configuration class for managing AWS services."""

    def __init__(self):
        """Initialize AWS configuration."""
        self.endpoint_url = os.getenv("AWS_ENDPOINT_URL")
        self.table_name = "MyTableDynamo"
        self.bucket_name = "my-bucket"

    def get_dynamodb_resource(self):
        """Get DynamoDB resource.

        Returns:
            boto3.resource: Configured DynamoDB resource
        """
        return boto3.resource('dynamodb', endpoint_url=self.endpoint_url)

    def get_s3_client(self):
        """Get S3 client.

        Returns:
            boto3.client: Configured S3 client
        """
        return boto3.client('s3', endpoint_url=self.endpoint_url)
