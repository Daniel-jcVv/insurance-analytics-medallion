"""
Upload CSV data to MinIO - Production version
Features:
- Retry logic for network failures
- Parallel uploads for better performance
- Comprehensive logging to file
- Progress tracking with visual feedback

Use this version for:
- Larger datasets (10K+ records)
- Production environments with network variability
- When you need detailed logs and monitoring
"""
from minio import Minio
from minio.error import S3Error
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# MinIO Configuration
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9100')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'adminpassword123')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'insurance-data')
MINIO_SECURE = os.getenv('MINIO_SECURE', 'False').lower() == 'true'


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def create_client():
    """Create MinIO client with retry logic"""
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE
    )
    # Test connection
    client.list_buckets()
    return client


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def upload_file_with_retry(client, bucket, local_path, remote_path):
    """Upload single file with retry and progress tracking"""
    file_size = local_path.stat().st_size

    with tqdm(
        total=file_size,
        unit='B',
        unit_scale=True,
        desc=f"↑ {local_path.name}",
        leave=False
    ) as pbar:
        client.fput_object(
            bucket,
            remote_path,
            str(local_path),
            content_type='text/csv'
        )
        pbar.update(file_size)

    logger.info(f"✓ Uploaded: {remote_path}")
    return True


def upload_files_parallel(client, bucket, files_to_upload, data_dir, max_workers=4):
    """Upload multiple files in parallel"""
    results = {'success': 0, 'failed': 0}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}

        for local_file, remote_path in files_to_upload:
            local_path = data_dir / local_file
            if not local_path.exists():
                logger.error(f"✗ File not found: {local_path}")
                results['failed'] += 1
                continue

            future = executor.submit(
                upload_file_with_retry,
                client,
                bucket,
                local_path,
                remote_path
            )
            futures[future] = local_file

        for future in as_completed(futures):
            try:
                future.result()
                results['success'] += 1
            except Exception as e:
                logger.error(f"✗ Failed to upload {futures[future]}: {e}")
                results['failed'] += 1

    return results


def main():
    """Upload insurance data files to MinIO"""
    logger.info("=" * 60)
    logger.info("Starting MinIO upload process")
    logger.info("=" * 60)

    # Create logs directory
    Path('logs').mkdir(exist_ok=True)

    # Create client
    try:
        client = create_client()
        logger.info(f"✓ Connected to MinIO: {MINIO_ENDPOINT}")
    except Exception as e:
        logger.error(f"✗ Failed to connect to MinIO: {e}")
        return

    # Create bucket if not exists
    try:
        if not client.bucket_exists(MINIO_BUCKET):
            client.make_bucket(MINIO_BUCKET)
            logger.info(f"✓ Created bucket: '{MINIO_BUCKET}'")
        else:
            logger.info(f"✓ Bucket '{MINIO_BUCKET}' already exists")
    except S3Error as e:
        logger.error(f"✗ Error creating bucket: {e}")
        return

    # Define files
    data_dir = Path('data/raw')
    files_to_upload = [
        ('customers.csv', 'bronze/customers.csv'),
        ('policies.csv', 'bronze/policies.csv'),
        ('claims.csv', 'bronze/claims.csv')
    ]

    # Upload files (parallel for speed)
    logger.info(f"\nUploading {len(files_to_upload)} files...")
    results = upload_files_parallel(client, MINIO_BUCKET, files_to_upload, data_dir)

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info(f"Process completed: {results['success']} successful, {results['failed']} failed")
    logger.info(f"MinIO Console: http://{MINIO_ENDPOINT.split(':')[0]}:9101")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
