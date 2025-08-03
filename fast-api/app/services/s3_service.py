
from datetime import datetime
from fastapi import HTTPException
from botocore.exceptions import ClientError

class S3Service:
    """Service class for handling S3 operations."""

    def __init__(self, s3_client, bucket_name):
        """
        Args:
            s3_client: boto3.client: Configured S3 client
            bucket_name (str): Name of the S3 bucket
        """
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def upload_text_file(self, content: str) -> str:
        """Upload text content as a file to S3."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"records_export_{timestamp}.txt"

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=content,
                ContentType='text/plain'
            )
            return filename
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_file_content(self, filename: str) -> str:
        """Get content of a file from S3.
        Returns: (str): Content of the file
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise HTTPException(status_code=404, detail="File not found")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
