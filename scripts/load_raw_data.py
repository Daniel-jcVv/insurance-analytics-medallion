"""
Script to upload CSV data to MinIO
Requirements: pip install minio python-dotenv
"""
from minio import Minio
from minio.error import S3Error
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# MinIO Configuration
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9100')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'adminpassword123')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'insurance-data')
MINIO_SECURE = os.getenv('MINIO_SECURE', 'False').lower() == 'true'

def create_minio_client():
    """Create MinIO client"""
    return Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE
    )

def create_bucket_if_not_exists(client, bucket_name):
    """Create bucket if it doesn't exist"""
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"✓ Bucket '{bucket_name}' created successfully")
        else:
            print(f"✓ Bucket '{bucket_name}' already exists")
    except S3Error as e:
        print(f"✗ Error creating bucket: {e}")
        raise

def upload_file(client, bucket_name, file_path, object_name):
    """Upload file to MinIO"""
    try:
        client.fput_object(
            bucket_name,
            object_name,
            file_path,
        )
        print(f"✓ Uploaded: {file_path} -> {bucket_name}/{object_name}")
    except S3Error as e:
        print(f"✗ Error uploading {file_path}: {e}")
        raise

def main():
    print("=" * 60)
    print("Uploading data to MinIO")
    print("=" * 60)

    # Create client
    client = create_minio_client()
    print(f"✓ Connected to MinIO: {MINIO_ENDPOINT}")

    # Create bucket
    create_bucket_if_not_exists(client, MINIO_BUCKET)

    # Files to upload (use existing CSV files in data/ directory)
    data_dir = Path('data')
    files_to_upload = [
        ('customers.csv', 'bronze/customers.csv'),
        ('policies.csv', 'bronze/policies.csv'),
        ('claims.csv', 'bronze/claims.csv')
    ]

    # Upload files
    print("\nUploading files...")
    for local_file, remote_path in files_to_upload:
        local_path = data_dir / local_file
        if local_path.exists():
            upload_file(client, MINIO_BUCKET, str(local_path), remote_path)
        else:
            print(f"⚠ File not found: {local_path}")

    print("\n" + "=" * 60)
    print("Process completed")
    print(f"MinIO Console: http://{MINIO_ENDPOINT.split(':')[0]}:9101")
    print(f"User: {MINIO_ACCESS_KEY}")
    print("=" * 60)
    

if __name__ == "__main__":
    main()
