# Insurance Claims Analytics - MinIO + Microsoft Fabric

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-3.x-orange?logo=apache-spark&logoColor=white)
![Microsoft Fabric](https://img.shields.io/badge/Microsoft%20Fabric-Lakehouse-blue?logo=microsoft&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-ACID-00ADD8?logo=delta&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-S3%20Compatible-C72E49?logo=minio&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS%20S3-Cloud%20Storage-FF9900?logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Stage%204%20Complete-brightgreen)

End-to-end data engineering project implementing **Medallion Architecture** for insurance claims analysis, using local MinIO and Microsoft Fabric for processing and visualization.

> **Approach:** MVP (Minimum Viable Product) built incrementally in functional stages with small, manageable datasets (~50 records) to demonstrate data engineering skills.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     STORAGE LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  MinIO (Local - Docker)                                      │
│  ├── insurance-data/bronze/                                  │
│  │   ├── customers.csv                                       │
│  │   ├── policies.csv                                        │
│  │   └── claims.csv                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              MICROSOFT FABRIC (Lakehouse)                    │
├─────────────────────────────────────────────────────────────┤
│  📦 BRONZE Layer (Raw Data)                                  │
│  ├── Data Pipeline: MinIO → Lakehouse                        │
│  ├── Format: Delta Tables                                    │
│  └── Data as-is from source                                  │
│                                                               │
│  🔄 SILVER Layer (Clean & Merged)                            │
│  ├── PySpark Notebooks                                       │
│  ├── Data cleaning and validation                            │
│  ├── Table joins                                             │
│  └── Format: Delta Tables                                    │
│                                                               │
│  ✨ GOLD Layer (Business Ready)                              │
│  ├── KPI aggregations                                        │
│  ├── Analytics-optimized data                                │
│  └── Format: Delta Tables                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              VISUALIZATION LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  Power BI (Fabric)                                           │
│  ├── KPI Dashboard                                           │
│  ├── Top claimers analysis                                   │
│  ├── Approval rate by gender/policy                          │
│  ├── Temporal trends                                         │                                    │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.8+
- Microsoft Fabric trial account
- Git


### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/Daniel-jcVv/insurance-analytics-medallion.git
cd insurance-analytics-medallion

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

### 2. Start MinIO

```bash
# Start MinIO with Docker Compose
docker compose up -d

# Verify it's running
docker ps
```

**MinIO Console:** http://localhost:9101
- **User:** admin
- **Password:** adminpassword123

### 3. Upload Sample Data

#### Option A: Local Development (MinIO)
```bash
# Install dependencies
pip install -r requirements.txt

# Upload data to MinIO
python scripts/upload_to_minio.py

# Run tests
pytest tests/ -v
```

#### Option B: Cloud Storage (AWS S3) - **Recommended for Fabric**
```bash
# Configure AWS credentials in .env file
cp .env.example .env
# Edit .env and add your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

# Upload data to S3
python scripts/upload_to_s3.py
```

**Uploaded files:**
- `data/raw/customers.csv` → `bronze/customers.csv`
- `data/raw/policies.csv` → `bronze/policies.csv`
- `data/raw/claims.csv` → `bronze/claims.csv`

> **Note:** We use small datasets (50 records) for MVP - sufficient to validate logic and demonstrate understanding.

> **Cloud Integration:** Using AWS S3 allows Microsoft Fabric to connect directly via Amazon S3 connector, enabling automated data pipelines instead of manual uploads.

### 4. Setup Microsoft Fabric (Cloud)

#### 4.1 Create Workspace and Lakehouse

1. Go to [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. Create a new **Workspace** named `Insurance Analytics`
3. Inside the workspace, create a **Lakehouse** named `insurance_lakehouse`

#### 4.2 Connect Fabric to AWS S3

1. In your workspace, create a new **Data Pipeline**
2. Add **Copy Data** activity
3. Configure **Source** with Amazon S3 connector:
   - **Endpoint:** `https://s3.amazonaws.com` (or region-specific endpoint)
   - **Access Key ID:** Your AWS_ACCESS_KEY_ID
   - **Secret Access Key:** Your AWS_SECRET_ACCESS_KEY
   - **Bucket:** `insurance-data-fabric` (or your S3_BUCKET name)
   - **Region:** `us-east-1` (or your AWS_REGION)
4. Select files from `bronze/` folder
5. Configure **Destination** as your Lakehouse
6. Run the pipeline to ingest data



#### 4.3 Create PySpark Notebooks

**Bronze → Silver:**
- Clean null values
- Standardize formats
- Join tables

**Silver → Gold:**
- KPI aggregations
- Business metrics calculation
- Report optimization

## 📊 Business Questions Answered

This project provides insights into:

1. **Top Claimers:** Which customers generate the most claims?
2. **Approval Rates:** Claim approval by gender and policy type
3. **Temporal Trends:** Claims patterns over time
4. **Policy Performance:** Claim activity by policy type
5. **Demographics:** Claims by customer segments
6. **Risk Analysis:** High-risk customers with claim-to-coverage ratio > 50%

### Power BI Dashboard Features

**Dashboard:** "Customer Claims Performance Report"

**KPI Cards:**
- Total Customers: 24
- Total Claim Amount: $1.354M
- Average Approval Rate: 22.65%
- High Risk Customers: 7

**Visualizations:**
1. **Customer Distribution by Gender** - Donut chart showing gender breakdown
2. **Policy Types Distribution** - Bar chart analyzing Life, Auto, and Health policies
3. **Claims vs Coverage Analysis** - Scatter plot showing relationship by gender
4. **Top 10 Customers by Total Claims** - Horizontal bar chart of highest claimers
5. **Claims Volume Over Time** - Line chart showing temporal trends (2019-2023)

📸 **Screenshot:** [power-bi/Customer-Claims-Performance-Report.png](power-bi/Customer-Claims-Performance-Report.png)

## 📁 Project Structure

```
insurance-claims/
├── docker-compose.yml               # MinIO configuration
├── requirements.txt                 # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Files to ignore
├── README.md                       # This file
│
├── data/
│   └── raw/                        # CSV files (50 records each)
│       ├── customers.csv
│       ├── policies.csv
│       └── claims.csv
│
├── scripts/
│   ├── upload_to_minio.py          # Upload to MinIO (local dev)
│   ├── upload_to_minio_production.py  # Production MinIO (retry + logging)
│   ├── upload_to_s3.py             # Upload to AWS S3 (cloud/Fabric)
│ 
│
├── tests/
│   ├── test_upload.py              # Integration tests
│   └── README.md                   # Test documentation
│
├── fabric/
│   └── notebooks/
│       ├── 01_Bronze_to_Silver.ipynb   # Data cleaning & validation
│       └── 02_Silver_to_Gold.ipynb     # Business metrics & analytics
│
├── power-bi/
│   └── Customer-Claims-Performance-Report.png  # Dashboard screenshot
│
├── docs/
│   └── screenshots/
│       └── fabric/                 # Fabric workspace screenshots
│           ├── 03-fabric-bronze-files.png
│           ├── 05-fabric-silver-tables.png
│           └── 06-fabric-gold-tables.png
│
│
├── minio/
│   └── data/                       # MinIO persistent storage (gitignored)
│___

```

## 🎯 Implementation Stages (MVP)

### Stage 1: FOUNDATION - "It Works"
- ✅ MinIO running in Docker
- ✅ 50 records in each CSV file
- ✅ AWS S3 bucket created and data uploaded
- ✅ Fabric workspace created


### Stage 2: TRANSFORMATION - "It's Clean"
- ✅ Silver layer notebook created (`01_Bronze_to_Silver.ipynb`)
- ✅ Data cleaning implemented (dates, nulls, formatting)
- ✅ 3 Silver Delta tables written

### Stage 3: ANALYTICS - "It Answers Questions"
- ✅ Tables joined (claims → policies → customers)
- ✅ Gold aggregation table created (`gold_customer_claims_analytics`)
- ✅ Business metrics calculated (approval rates, coverage ratios, temporal analysis)
- ✅ Data quality checks implemented
- ✅ Business insights generated

### Stage 4: VISUALIZATION - "It's Presentable"
- ✅ Power BI report created (`Customer Claims Performance Report`)
- ✅ Dashboard with KPIs and visualizations
- ✅ Portfolio screenshots captured

### Stage 5 (Optional): SCALE - "It Handles More"
- 🔲 Script to generate 200-500 records
- 🔲 Pipeline re-run with larger dataset
- 🔲 Performance documented



## 📈 Scalability & Production Readiness

This project demonstrates pragmatic through **two upload scripts**:

### Simple Version (`upload_to_minio.py`)
**Use for:** MVP, demos, small datasets
- Basic error handling
- File validation


### Production Version (`upload_to_minio_production.py`)
**Use for:** Larger datasets, production environments
- Retry logic with exponential backoff
- Parallel uploads (4 workers)
- Logging to file
- Progress bars

**Philosophy:** Start simple, add complexity when justified. The value is in the **Medallion Architecture + Fabric transformations**.

## 🔧 Useful Commands

```bash
# View MinIO logs
docker compose logs -f minio

# Stop MinIO
docker compose down

# Clean MinIO data (destructive)
docker compose down -v

# Upload data to MinIO (simple)
python scripts/upload_to_minio.py

# Upload data to MinIO (production)
python scripts/upload_to_minio_production.py

# Verify data in MinIO
# Access http://localhost:9101 and explore the bucket
```

## 📝 Portfolio Highlights

This project demonstrates:

- ✅ **Medallion Architecture** (Bronze/Silver/Gold) - Complete implementation
- ✅ **End-to-End Data Engineering** - From raw data to business insights
- ✅ **Microsoft Fabric** (Lakehouse, PySpark Notebooks, Power BI)
- ✅ **PySpark Processing** - Data cleaning, transformations, and aggregations
- ✅ **Object Storage Patterns** (S3-compatible MinIO + AWS S3)
- ✅ **Power BI Dashboards** - Interactive analytics with 5 visualizations + 4 KPIs
- ✅ **Docker** for local infrastructure
- ✅ **Python Automation** (upload scripts + integration tests)
- ✅ **Delta Lake** format (ACID transactions, time travel)
- ✅ **Data Quality Checks** - Validation and business logic
- ✅ **Cloud Integration** - AWS S3 → Fabric pipeline
- ✅ **Pragmatic Engineering** (simple first, complexity when justified)

## 🎯 Architecture Strategy

### Why MinIO + Fabric (instead of just Fabric)?

**MinIO (Local Development):**
- Practice S3 API integration patterns
- Test data pipelines without cloud costs
- Demonstrate infrastructure-as-code skills
- Learn object storage concepts

**Fabric (Cloud Demo):**
- Showcase Medallion Architecture transformations
- Demonstrate PySpark and Delta Lake expertise
- Build Power BI dashboards
- Prove cloud data engineering skills

**Key Insight:** MinIO localhost cannot be accessed by cloud Fabric. For MVP, data is manually uploaded to Fabric Lakehouse. In production, this would be automated via Azure Data Lake Storage → Fabric Data Pipeline.


## 📚 Resources

- [Microsoft Fabric Docs](https://learn.microsoft.com/en-us/fabric/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Delta Lake](https://delta.io/)



---

