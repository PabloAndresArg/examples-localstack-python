# Import necessary libraries
from fastapi import FastAPI, HTTPException  # FastAPI framework and HTTP error handling
from fastapi.responses import PlainTextResponse  # For returning text files
from pydantic import BaseModel, Field      # For data validation and schema definition
import boto3                               # AWS SDK for Python
from typing import Optional                # For optional type hints
import json                                # For JSON serialization
from datetime import datetime              # For timestamping files
from botocore.exceptions import ClientError # For handling S3 specific errors

# Initialize FastAPI application
app = FastAPI()

# Configure DynamoDB client with LocalStack settings
dynamodb = boto3.resource('dynamodb',
    endpoint_url='http://localhost:4566',      # LocalStack endpoint
    aws_access_key_id='test',                 # Mock AWS credentials for local testing
    aws_secret_access_key='test',             # Mock AWS credentials for local testing
    region_name='us-east-1'                   # AWS region setting
)
# Connect to the 'Users' table
table = dynamodb.Table('Users')

# Configure S3 client with LocalStack settings
s3 = boto3.client('s3',
    endpoint_url='http://localhost:4566',      # LocalStack endpoint
    aws_access_key_id='test',                 # Mock AWS credentials for local testing
    aws_secret_access_key='test',             # Mock AWS credentials for local testing
    region_name='us-east-1'                   # AWS region setting
)

# S3 bucket name
BUCKET_NAME = "user-files"

# Define the data model for User using Pydantic
class User(BaseModel):
    # Define required fields with validation
    id: str = Field(..., min_length=1, description="User ID")
    nombre: str = Field(..., min_length=1, description="User name")

    # Provide example data for API documentation
    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "nombre": "Juan"
            }
        }

# POST endpoint to create a new user
@app.post("/users/", response_model=dict)
async def create_user(user: User):
    try:
        # Insert the user data into DynamoDB
        table.put_item(
            Item={
                'id': user.id,
                'nombre': user.nombre
            }
        )
        # Return success message with user data
        return {"message": "User created successfully", "user": user.dict()}
    except Exception as e:
        # Handle any errors during the process
        raise HTTPException(status_code=500, detail=str(e))

# GET endpoint to retrieve a user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        # Query DynamoDB for the user with the specified ID
        response = table.get_item(
            Key={
                'id': user_id
            }
        )
        
        # Check if user exists
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Return the user data    
        return response['Item']
    except Exception as e:
        # Handle any errors during the process
        raise HTTPException(status_code=500, detail=str(e))



# POST endpoint to export all users to S3 as a text file
@app.post("/s3/export", response_model=dict)
async def export_users_to_s3():
    try:
        print("Exporting users to S3...")
        # Scan the DynamoDB table to get all users
        response = table.scan()
        users = response.get('Items', [])
        
        # Continue scanning if we haven't got all users
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            users.extend(response.get('Items', []))
        
        if not users:
            return {"message": "No users found to export"}
        
        # Format the users data as text
        users_text = ""
        for user in users:
            users_text += f"ID: {user.get('id', 'N/A')}, Nombre: {user.get('nombre', 'N/A')}\n"
        
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"users_export_{timestamp}.txt"
        
        # Upload the text file to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=users_text,
            ContentType='text/plain'
        )
        
        return {
            "message": "Users exported successfully",
            "file_name": filename,
            "bucket": BUCKET_NAME,
            "user_count": len(users)
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