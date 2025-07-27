import boto3

def create_s3_bucket():
    # Create the S3 client with LocalStack endpoint
    s3 = boto3.client('s3',
        endpoint_url='http://localhost:4566',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )

    # Create the bucket
    try:
        s3.create_bucket(Bucket='my-bucket')
        print("S3 bucket 'my-bucket' created successfully!")
    except Exception as e:
        print(f"Error creating bucket: {str(e)}")

if __name__ == "__main__":
    create_s3_bucket()