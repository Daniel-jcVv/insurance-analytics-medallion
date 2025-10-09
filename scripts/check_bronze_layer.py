"""
Stage 1: FOUNDATION - Validation Script

Validates that:
1. MinIO container is running
2. MinIO bucket exists
3. Data files are uploaded to MinIO
4. Data files have expected row counts

Run this after completing Stage 1 to verify everything is working.
"""
import os
import sys
from pathlib import Path
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9100')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'adminpassword123')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'insurance-data')
MINIO_SECURE = os.getenv('MINIO_SECURE', 'False').lower() == 'true'

# Expected files in MinIO
EXPECTED_FILES = {
    'bronze/customers.csv': 50,  # Expected minimum row count
    'bronze/policies.csv': 50,
    'bronze/claims.csv': 50
}

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BLUE}{'=' * 60}")
    print(f"{text}")
    print(f"{'=' * 60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def validate_minio_connection():
    """Validate MinIO connection"""
    print_header("Stage 1.1: Validating MinIO Connection")

    try:
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )

        # Test connection by listing buckets
        buckets = list(client.list_buckets())
        print_success(f"Connected to MinIO at {MINIO_ENDPOINT}")
        print_success(f"Found {len(buckets)} bucket(s)")

        return client, True
    except Exception as e:
        print_error(f"Failed to connect to MinIO: {e}")
        print_warning("Make sure MinIO is running: docker-compose up -d")
        return None, False

def validate_bucket_exists(client):
    """Validate that the required bucket exists"""
    print_header("Stage 1.2: Validating Bucket Exists")

    try:
        if client.bucket_exists(MINIO_BUCKET):
            print_success(f"Bucket '{MINIO_BUCKET}' exists")
            return True
        else:
            print_error(f"Bucket '{MINIO_BUCKET}' does not exist")
            print_warning(f"Run: python scripts/upload_to_minio.py to create it")
            return False
    except S3Error as e:
        print_error(f"Error checking bucket: {e}")
        return False

def validate_files_uploaded(client):
    """Validate that required files are uploaded"""
    print_header("Stage 1.3: Validating Files Uploaded")

    all_valid = True

    for file_path, min_rows in EXPECTED_FILES.items():
        try:
            # Check if file exists
            stat = client.stat_object(MINIO_BUCKET, file_path)
            print_success(f"Found: {file_path} ({stat.size} bytes)")

            # Download and count rows
            response = client.get_object(MINIO_BUCKET, file_path)
            content = response.read().decode('utf-8')
            row_count = len(content.strip().split('\n')) - 1  # -1 for header

            if row_count >= min_rows:
                print_success(f"  → Row count: {row_count} (expected ≥ {min_rows})")
            else:
                print_error(f"  → Row count: {row_count} (expected ≥ {min_rows})")
                all_valid = False

        except S3Error as e:
            if e.code == 'NoSuchKey':
                print_error(f"Missing: {file_path}")
                print_warning(f"Run: python scripts/upload_to_minio.py")
                all_valid = False
            else:
                print_error(f"Error checking {file_path}: {e}")
                all_valid = False

    return all_valid

def validate_local_data_files():
    """Validate that local CSV files exist"""
    print_header("Stage 1.0: Validating Local Data Files")

    data_dir = Path('data/raw')
    required_files = ['customers.csv', 'policies.csv', 'claims.csv']

    all_exist = True
    for filename in required_files:
        file_path = data_dir / filename
        if file_path.exists():
            size = file_path.stat().st_size
            print_success(f"Found: {file_path} ({size} bytes)")
        else:
            print_error(f"Missing: {file_path}")
            all_exist = False

    return all_exist

def main():
    """Main validation function"""
    print_header("Stage 1 FOUNDATION - Validation")
    print("This script validates that Stage 1 is complete\n")

    validation_results = {}

    # 1. Validate local files
    validation_results['local_files'] = validate_local_data_files()

    # 2. Validate MinIO connection
    client, connection_ok = validate_minio_connection()
    validation_results['minio_connection'] = connection_ok

    if not connection_ok:
        print_header("VALIDATION FAILED")
        print_error("Cannot proceed without MinIO connection")
        sys.exit(1)

    # 3. Validate bucket exists
    validation_results['bucket_exists'] = validate_bucket_exists(client)

    # 4. Validate files uploaded
    validation_results['files_uploaded'] = validate_files_uploaded(client)

    # Final summary
    print_header("VALIDATION SUMMARY")

    all_passed = all(validation_results.values())

    for check, result in validation_results.items():
        status = "PASS" if result else "FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.END} - {check.replace('_', ' ').title()}")

    print()

    if all_passed:
        print_success("Stage 1 FOUNDATION is complete! ✓")
        print_success("You can proceed to Stage 2 (TRANSFORMATION)")
        print(f"\n{Colors.BLUE}Next steps:{Colors.END}")
        print("  1. Create Microsoft Fabric workspace")
        print("  2. Create Lakehouse in Fabric")
        print("  3. Configure Data Pipeline: MinIO → Bronze layer")
        print("  4. Run: python scripts/validate_stage2_transformation.py (when ready)")
        sys.exit(0)
    else:
        print_error("Stage 1 validation FAILED")
        print_warning("Fix the issues above before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main()
