# AWS S3 Setup Guide

This guide walks you through setting up AWS S3 for the insurance claims analytics project and connecting it to Microsoft Fabric.

---

## 📋 Prerequisites

- AWS account (free tier is sufficient)
- AWS CLI installed (optional but recommended)
- Microsoft Fabric workspace created

---

## 🚀 Step 1: Create AWS S3 Bucket

### Option A: AWS Console (Easier)

1. Go to [AWS S3 Console](https://s3.console.aws.amazon.com/)
2. Click **Create bucket**
3. Configure:
   - **Bucket name:** `insurance-data-fabric` (must be globally unique)
   - **Region:** `mx-central-1` (or your preferred region)
   - **Block Public Access:** Keep all checkboxes CHECKED (data should be private)
   - **Bucket Versioning:** Disabled (not needed for MVP)
   - **Encryption:** Default (Server-side encryption)
4. Click **Create bucket**

### Option B: AWS CLI (Faster)

```bash
# Create bucket
aws s3 mb s3://insurance-data-fabric --region mx-central-1

# Verify bucket exists
aws s3 ls
```

---

## 🔑 Step 2: Create IAM User for Fabric Access

### Why?
You need programmatic access credentials (Access Key + Secret Key) for:
- Upload script (`upload_to_s3.py`)
- Microsoft Fabric S3 connector

### Create IAM User:

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Users** → **Add users**
3. Configure:
   - **User name:** `fabric-s3-access`
   - **Access type:** ✅ Programmatic access
   - Click **Next: Permissions**
4. Attach permissions:
   - Click **Attach existing policies directly**
   - Search for and select: **AmazonS3FullAccess** (for simplicity)
   - For production, create a custom policy with least privilege
5. Click **Next** until **Create user**
6. **IMPORTANT:** Download the CSV with credentials or copy:
   - **Access key ID:** `AKIAXXXXXXXXXXXXXXXX`
   - **Secret access key:** `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

⚠️ **Save these credentials securely - you won't see the secret key again**

---

## 🔐 Step 3: Configure Local Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file
nano .env
```

Add your AWS credentials:

```bash
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_REGION=us-east-1
S3_BUCKET=insurance-data-fabric
```

**⚠️ Security Note:**
- Never commit `.env` to Git (already in `.gitignore`)
- Don't share credentials publicly

---

## 📤 Step 4: Upload Data to S3

```bash
# Install boto3 if not already installed
pip install boto3

# Run upload script
python scripts/upload_to_s3.py
```

**Expected output:**
```
============================================================
Uploading data to AWS S3
============================================================
✓ Connected to AWS S3 (region: us-east-1)
✓ Bucket 'insurance-data-fabric' already exists

Uploading files...
✓ Uploaded: s3://insurance-data-fabric/bronze/customers.csv
✓ Uploaded: s3://insurance-data-fabric/bronze/policies.csv
✓ Uploaded: s3://insurance-data-fabric/bronze/claims.csv

============================================================
Process completed: 3/3 files uploaded
============================================================
```

---

## ✅ Step 5: Verify Upload in AWS Console

1. Go to [S3 Console](https://s3.console.aws.amazon.com/)
2. Click on bucket: `insurance-data-fabric`
3. Navigate to `bronze/` folder
4. Verify 3 CSV files are present:
   - `customers.csv` (~2 KB)
   - `policies.csv` (~2 KB)
   - `claims.csv` (~2 KB)

📸 **Screenshot Checkpoint:** Take screenshot for portfolio

---

## 🔗 Step 6: Connect Microsoft Fabric to S3

### 6.1 Create Connection in Fabric

1. Go to [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. Navigate to your workspace: **Insurance Analytics**
3. Click **New** → **Data Pipeline**
4. Name it: `S3_to_Bronze_Ingestion`
5. Add **Copy data** activity
6. Configure **Source**:
   - **Connection:** Click **+ New**
   - **Connector type:** Select **Amazon S3**
   - Fill in details:
     ```
     Connection name: aws-s3-insurance-data
     Endpoint: https://s3.us-east-1.amazonaws.com
     Authentication: Access Key
     Access key ID: <your AWS_ACCESS_KEY_ID>
     Secret access key: <your AWS_SECRET_ACCESS_KEY>
     ```
   - Click **Test connection** → Should show "Connection successful"
   - Click **Create**

### 6.2 Configure Source Dataset

1. In the Source tab:
   - **Bucket:** `insurance-data-fabric`
   - **File path:** `bronze/`
   - **File format:** CSV
   - **Column delimiter:** Comma
   - **First row as header:** Yes

### 6.3 Configure Destination (Lakehouse)

1. Click **Destination** tab
2. Select **Lakehouse**
3. Choose your lakehouse: `insurance_lakehouse`
4. **Table name:** `bronze_customers` (repeat for each file)
5. **Write mode:** Overwrite

### 6.4 Run the Pipeline

1. Click **Save**
2. Click **Run**
3. Monitor execution
4. Verify data in Lakehouse → Tables

📸 **Screenshot Checkpoints:**
- Connection successful test
- Pipeline successful run
- Data in Lakehouse tables

---

## 💰 Cost Considerations

### Free Tier Coverage (12 months):
- ✅ 5 GB storage
- ✅ 20,000 GET requests
- ✅ 2,000 PUT requests

### Your Project (~6 KB total):
- **Storage cost:** $0.00/month
- **Transfer cost:** $0.00/month
- **API calls:** ~10 PUT + 50 GET = $0.00

**Total monthly cost: $0.00** (well within free tier)

### Even After Free Tier:
- Storage: $0.023/GB/month → ~$0.0001/month
- PUT requests: $0.005/1000 → ~$0.00001/month

**Worst case: <$0.01/month**

---

## 🧹 Cleanup (Optional)

If you want to delete resources later:

```bash
# Delete all objects in bucket
aws s3 rm s3://insurance-data-fabric --recursive

# Delete bucket
aws s3 rb s3://insurance-data-fabric

# Delete IAM user (via AWS Console)
# IAM → Users → fabric-s3-access → Delete
```

---

## 🔧 Troubleshooting

### Error: "Bucket already exists"
- Bucket names are globally unique
- Try: `insurance-data-fabric-yourname` or add timestamp

### Error: "Access Denied"
- Check IAM user has S3 permissions
- Verify credentials in `.env` are correct
- Ensure no typos in bucket name

### Fabric connection fails
- Verify endpoint matches your region:
  - `us-east-1`: `https://s3.us-east-1.amazonaws.com`
  - `us-west-2`: `https://s3.us-west-2.amazonaws.com`
- Check credentials are correct
- Ensure bucket exists and has files

### Files not appearing in S3
- Check script output for errors
- Verify AWS credentials are valid
- Check bucket name in `.env` matches created bucket

---

## 📚 Additional Resources

- [AWS S3 Getting Started](https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Microsoft Fabric S3 Connector](https://learn.microsoft.com/en-us/fabric/data-factory/connector-amazon-s3)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

## ✅ Success Checklist

- [ ] AWS account created
- [ ] S3 bucket created: `insurance-data-fabric`
- [ ] IAM user created with S3 permissions
- [ ] Credentials saved in `.env` file
- [ ] Upload script executed successfully
- [ ] 3 CSV files visible in S3 console
- [ ] Fabric connection to S3 tested successfully
- [ ] Data pipeline created and run
- [ ] Data visible in Fabric Lakehouse

**Next:** Proceed to Bronze → Silver transformations in Fabric notebooks
