# 🚀 Quick Start Guide

## Prerequisites
- Docker and Docker Compose installed
- Python 3.8+ installed
- Git installed

## Step-by-Step Setup (5 minutes)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd insurance-claims
```

### 2. Start MinIO (Storage Layer)
```bash
# Start MinIO in Docker
docker-compose up -d

# Verify it's running
docker ps | grep minio
```

**Expected output:**
```
insurance-minio   Up X seconds   0.0.0.0:9100->9000/tcp, 0.0.0.0:9101->9001/tcp
```

### 3. Setup Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (defaults work for local setup)
# nano .env
```

### 5. Upload Data to MinIO
```bash
# Upload CSV files to MinIO bronze layer
python scripts/upload_to_minio.py
```

**Expected output:**
```
============================================================
Uploading data to MinIO
============================================================
✓ Connected to MinIO: localhost:9100
✓ Bucket 'insurance-data' already exists

Uploading files...
✓ Uploaded: bronze/customers.csv
✓ Uploaded: bronze/policies.csv
✓ Uploaded: bronze/claims.csv

============================================================
Process completed: 3/3 files uploaded
============================================================
```

### 6. Verify Upload (MinIO Console)
```bash
# Open in browser:
http://localhost:9101

# Login credentials:
Username: admin
Password: adminpassword123

# Navigate to: Buckets → insurance-data → bronze/
# You should see 3 CSV files
```

### 7. Run Tests (Optional but Recommended)
```bash
# Run integration tests
pytest tests/ -v
```

**Expected output:**
```
tests/test_upload.py::test_minio_connection PASSED
tests/test_upload.py::test_bucket_creation PASSED
tests/test_upload.py::test_upload_single_file PASSED
tests/test_upload.py::test_upload_all_files PASSED
tests/test_upload.py::test_file_exists_check PASSED

====== 5 passed in 0.17s ======
```

---

## Stage 1 Complete!

You have successfully:
- ✅ Started MinIO locally
- ✅ Uploaded 3 CSV files (150 total records)
- ✅ Verified data in MinIO Console
- ✅ Ran automated tests

**Next Steps:**
- Stage 2: Create Microsoft Fabric workspace
- Stage 3: Ingest data from MinIO to Fabric Bronze layer
- Stage 4: Transform data (Bronze → Silver → Gold)

---

## Useful Commands

```bash
# View MinIO logs
docker-compose logs -f minio

# Stop MinIO
docker-compose down

# Restart MinIO (keeps data)
docker-compose restart

# Delete everything and start fresh
docker-compose down -v
docker-compose up -d
python scripts/upload_to_minio.py

# Re-upload data (if you make changes)
python scripts/upload_to_minio.py

# Run tests
pytest tests/ -v

# Deactivate virtual environment
deactivate
```

---

## 🆘 Troubleshooting

### MinIO not starting?
```bash
# Check if port 9100 is already in use
sudo lsof -i :9100

# Kill process using the port
kill -9 <PID>

# Restart
docker-compose up -d
```

### Upload script fails?
```bash
# Make sure MinIO is running
docker ps | grep minio

# Check environment variables
cat .env

# Verify data files exist
ls -lh data/raw/
```

### Tests fail?
```bash
# Make sure MinIO is running
docker-compose up -d

# Reinstall dependencies
pip install -r requirements.txt

# Run tests again
pytest tests/ -v
```

---

## What's in the Data?

- **customers.csv**: 50 insurance customers (ID, name, DOB, gender, contact)
- **policies.csv**: 50 insurance policies (ID, customer_id, type, status, coverage)
- **claims.csv**: 50 insurance claims (ID, policy_id, date, amount, status)

Total dataset: **150 records** - perfect for MVP demonstration

---

**Ready for Stage 2?** See [README.md](README.md#4-connect-fabric-to-minio) for Microsoft Fabric setup
