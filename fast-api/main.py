# Import necessary libraries
from fastapi import FastAPI, HTTPException  # FastAPI framework and HTTP error handling
from fastapi.responses import PlainTextResponse  # For returning text files
import boto3                               # AWS SDK for Python
from datetime import datetime              # For timestamping files
from botocore.exceptions import ClientError # For handling S3 specific errors

# Initialize FastAPI application
app = FastAPI()

# Configure DynamoDB client with LocalStack settings
dynamodb = boto3.resource('dynamodb',
    endpoint_url='http://localhost:4566',      # LocalStack endpoint

)
# Configure S3 client with LocalStack settings
s3 = boto3.client('s3',
    endpoint_url='http://localhost:4566',      # LocalStack endpoint
)


TABLE_DYNAMO = dynamodb.Table('MyTableDynamo')
BUCKET_NAME = "my-bucket"



@app.post("/s3/export", response_model=dict)
async def export_to_s3():
    try:
        response = TABLE_DYNAMO.scan()
        records = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            response = TABLE_DYNAMO.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            records.extend(response.get('Items', []))
        if not records:
            return {"message": "No records found to export"}
        # Format the records data as text
        records_text = ""
        for r in records:
            records_text += f"ID: {r.get('id', 'N/A')}, Body: {r.get('body', 'N/A')}\n"
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"records_export_{timestamp}.txt"

        # Upload the text file to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=records_text,
            ContentType='text/plain'
        )
        return {
            "message": "Records exported successfully",
            "file_name": filename,
            "bucket": BUCKET_NAME,
            "records_count": len(records)
        }
    except Exception as e:
        # Handle any errors during the process
        raise HTTPException(status_code=500, detail=str(e))

# GET endpoint to retrieve a text file from S3
@app.get("/s3/get-file/{filename}", response_class=PlainTextResponse)
async def get_file(filename: str):
    try:
        print(f"Retrieving file: {filename} from S3...")
        # Get the object from S3
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=filename
        )
        # Read the file content
        file_content = response['Body'].read().decode('utf-8')

        return file_content
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise HTTPException(status_code=404, detail="File not found")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    # Start the server with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Listen on all available network interfaces