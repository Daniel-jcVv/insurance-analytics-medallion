"""
Simple integration test for MinIO upload
Tests that the upload script can connect and upload files successfully
"""
import pytest
import os
from pathlib import Path
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv

load_dotenv()

# Configuration
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9100')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'adminpassword123')
MINIO_BUCKET = 'test-insurance-data'
TEST_DATA_DIR = Path('data/raw')


@pytest.fixture(scope='module')
def minio_client():
    """Create MinIO client for testing"""
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    return client


@pytest.fixture(scope='module')
def test_bucket(minio_client):
    """Create test bucket and clean up after tests"""
    # Setup: create bucket
    try:
        if not minio_client.bucket_exists(MINIO_BUCKET):
            minio_client.make_bucket(MINIO_BUCKET)
    except S3Error:
        pass  # Bucket might already exist

    yield MINIO_BUCKET

    # Teardown: remove test bucket and objects
    try:
        objects = minio_client.list_objects(MINIO_BUCKET, recursive=True)
        for obj in objects:
            minio_client.remove_object(MINIO_BUCKET, obj.object_name)
        minio_client.remove_bucket(MINIO_BUCKET)
    except S3Error:
        pass  # Ignore cleanup errors


def test_minio_connection(minio_client):
    """Test that we can connect to MinIO"""
    buckets = minio_client.list_buckets()
    assert isinstance(buckets, list)


def test_bucket_creation(minio_client, test_bucket):
    """Test that bucket exists"""
    assert minio_client.bucket_exists(test_bucket)


def test_upload_single_file(minio_client, test_bucket):
    """Test uploading a single CSV file"""
    test_file = TEST_DATA_DIR / 'customers.csv'

    # Skip if file doesn't exist
    if not test_file.exists():
        pytest.skip(f"Test file not found: {test_file}")

    # Upload file
    object_name = 'test/customers.csv'
    minio_client.fput_object(
        test_bucket,
        object_name,
        str(test_file),
        content_type='text/csv'
    )

    # Verify upload
    stat = minio_client.stat_object(test_bucket, object_name)
    assert stat.size > 0
    assert stat.size == test_file.stat().st_size


def test_upload_all_files(minio_client, test_bucket):
    """Test uploading all CSV files"""
    files = [
        ('customers.csv', 'test/customers.csv'),
        ('policies.csv', 'test/policies.csv'),
        ('claims.csv', 'test/claims.csv')
    ]

    uploaded_count = 0

    for local_file, remote_path in files:
        local_path = TEST_DATA_DIR / local_file

        if not local_path.exists():
            continue

        # Upload
        minio_client.fput_object(
            test_bucket,
            remote_path,
            str(local_path),
            content_type='text/csv'
        )

        # Verify
        stat = minio_client.stat_object(test_bucket, remote_path)
        assert stat.size == local_path.stat().st_size

        uploaded_count += 1

    assert uploaded_count == 3, f"Expected 3 files, uploaded {uploaded_count}"


def test_file_exists_check(minio_client, test_bucket):
    """Test checking if file exists in bucket"""
    test_file = TEST_DATA_DIR / 'customers.csv'

    if not test_file.exists():
        pytest.skip(f"Test file not found: {test_file}")

    object_name = 'test/exists_check.csv'

    # File should not exist initially
    try:
        minio_client.stat_object(test_bucket, object_name)
        file_exists = True
    except S3Error as e:
        if e.code == 'NoSuchKey':
            file_exists = False
        else:
            raise

    assert not file_exists

    # Upload file
    minio_client.fput_object(
        test_bucket,
        object_name,
        str(test_file),
        content_type='text/csv'
    )

    # Now file should exist
    stat = minio_client.stat_object(test_bucket, object_name)
    assert stat is not None
