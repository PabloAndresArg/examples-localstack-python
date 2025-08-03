"""
This module defines all S3-related API endpoints.
"""
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.services.s3_service import S3Service
from app.services.dynamo_service import DynamoService

router = APIRouter(prefix="/s3", tags=["s3"])

def initialize_router(s3_service: S3Service, dynamo_service: DynamoService):

    @router.post("/export", response_model=dict)
    async def export_to_s3():
        """ Export records from DynamoDB to S3.
            Returns: (dict): Export operation details
        """
        records = dynamo_service.get_all_records()
        if not records:
            return {"message": "No records found to export"}
        records_text = dynamo_service.format_records_as_text(records)
        filename = s3_service.upload_text_file(records_text)
        return {
            "message": "Records exported successfully",
            "file_name": filename,
            "bucket": s3_service.bucket_name,
            "records_count": len(records)
        }

    @router.get("/get-file/{filename}", response_class=PlainTextResponse)
    async def get_file(filename: str):
        """Get file content from S3.
        Args: filename (str): Name of the file to retrieve
        Returns: (str): Content of the file
        """
        return s3_service.get_file_content(filename)
    return router
