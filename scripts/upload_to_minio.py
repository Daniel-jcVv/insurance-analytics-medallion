"""
Upload CSV data to MinIO storage - Simple version for MVP
"""
from minio import Minio
from minio.error import S3Error
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MinIO Configuration
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9100')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'adminpassword123')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'insurance-data')
MINIO_SECURE = os.getenv('MINIO_SECURE', 'False').lower() == 'true'


def main():
    """Upload insurance data files to MinIO"""
    print("=" * 70)
    print("Uploading data to MinIO")
    print("=" * 70)

    # Create MinIO client
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE
    )
    print(f"Connected to MinIO: {MINIO_ENDPOINT}")

    # Create bucket if not exists
    try:
        if not client.bucket_exists(MINIO_BUCKET):
            client.make_bucket(MINIO_BUCKET)
            print(f"Created bucket: '{MINIO_BUCKET}'")
        else:
            print(f"Bucket '{MINIO_BUCKET}' already exists")
    except S3Error as e:
        print(f"Error creating bucket: {e}")
        return

    # Define data directory
    data_dir = Path('data/raw')

    # Files to upload (local_filename, remote_path)
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

    for local_file, remote_path in files_to_upload:
        local_path = data_dir / local_file
        try:
            client.fput_object(
                MINIO_BUCKET,
                remote_path,
                str(local_path),
                content_type='text/csv'
            )
            print(f"Uploaded: {remote_path}")
            uploaded_count += 1
        except S3Error as e:
            print(f"Failed to upload {local_file}: {e}")

    # Summary
    print("\n" + "=" * 70)
    print(f"Process completed: {uploaded_count}/{len(files_to_upload)} files uploaded")
    print(f"\nMinIO Console: http://{MINIO_ENDPOINT.split(':')[0]}:9101")
    print(f"Username: {MINIO_ACCESS_KEY}")
    print(f"Bucket: {MINIO_BUCKET}")
    print("=" * 70)


if __name__ == "__main__":
    main()
