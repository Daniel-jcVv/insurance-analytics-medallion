"""
Upload CSV data to AWS S3 for Fabric integration

This script uploads data to AWS S3, which can then be accessed by
Microsoft Fabric Data Pipelines using the Amazon S3 connector.
"""
import os
import boto3
from pathlib import Path
from dotenv import load_dotenv
from botocore.exceptions import ClientError, NoCredentialsError

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'mex-central-1')
S3_BUCKET = os.getenv('S3_BUCKET', 'insurance-data-fabric')


def create_s3_client():
    """Create S3 client with credentials"""
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise EnvironmentError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and "
            "AWS_SECRET_ACCESS_KEY in your .env file"
        )

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        return s3_client
    except NoCredentialsError:
        raise EnvironmentError("Invalid AWS credentials")


def create_bucket_if_not_exists(s3_client, bucket_name, region):
    """Create S3 bucket if it doesn't exist"""
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists")
    except ClientError as e:
        error_code = e.response['Error']['Code']

        if error_code == '404':
            # Bucket doesn't exist, create it
            try:
                if region == 'us-east-1':
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                print(f"✓ Created bucket: '{bucket_name}'")
            except ClientError as create_error:
                print(f"Error creating bucket: {create_error}")
                raise
        else:
            print(f"Error checking bucket: {e}")
            raise


def upload_file_to_s3(s3_client, file_path, bucket_name, s3_key):
    """Upload a single file to S3"""
    try:
        s3_client.upload_file(
            str(file_path),
            bucket_name,
            s3_key,
            ExtraArgs={'ContentType': 'text/csv'}
        )
        return True
    except ClientError as e:
        print(f"Error uploading {file_path.name}: {e}")
        return False


def main():
    """Upload insurance data files to AWS S3"""
    print("=" * 70)
    print("Uploading data to AWS S3")
    print("=" * 70)

    # Create S3 client
    try:
        s3_client = create_s3_client()
        print(f"Connected to AWS S3 (region: {AWS_REGION})")
    except EnvironmentError as e:
        print(f"{e}")
        return

    # Create bucket if needed
    try:
        create_bucket_if_not_exists(s3_client, S3_BUCKET, AWS_REGION)
    except ClientError:
        return

    # Define data directory
    data_dir = Path('data/bronze')

    # Files to upload (local_filename, s3_key)
    files_to_upload = [
        ('customers.csv', 'bronze/customers.csv'),
        ('policies.csv', 'bronze/policies.csv'),
        ('claims.csv', 'bronze/claims.csv')
    ]

    # Validate all files exist
    missing_files = []
    for local_file, _ in files_to_upload:
        local_path = data_dir / local_file
        if not local_path.exists():
            missing_files.append(str(local_path))

    if missing_files:
        print(f"\nError: Missing required files:")
        for missing in missing_files:
            print(f"  - {missing}")
        return

    # Upload files
    print("\nUploading files...")
    uploaded_count = 0

    for local_file, s3_key in files_to_upload:
        local_path = data_dir / local_file

        if upload_file_to_s3(s3_client, local_path, S3_BUCKET, s3_key):
            print(f"✓ Uploaded: s3://{S3_BUCKET}/{s3_key}")
            uploaded_count += 1

    # Summary
    print("\n" + "=" * 70)
    print(f"Process completed: {uploaded_count}/{len(files_to_upload)} files uploaded")
    print(f"\nS3 Bucket: {S3_BUCKET}")
    print(f"Region: {AWS_REGION}")
    print(f"AWS Console: https://s3.console.aws.amazon.com/s3/buckets/{S3_BUCKET}")
    print("\nNext steps:")
    print("1. Go to Microsoft Fabric")
    print("2. Create Data Pipeline with Amazon S3 connector")
    print(f"3. Use bucket: {S3_BUCKET}")
    print("=" * 60)


if __name__ == "__main__":
    main()
