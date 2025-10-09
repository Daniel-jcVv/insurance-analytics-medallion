# Insurance Claims Analytics - MinIO + Microsoft Fabric

End-to-end data engineering project implementing **Medallion Architecture** for insurance claims analysis, using local MinIO as an alternative to Azure Data Lake Storage and Microsoft Fabric for processing and visualization.

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
│  ├── Temporal trends                                         │
│  └── Demographic analysis                                    │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.8+
- Microsoft Fabric trial account
- Git

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <your-repo>
cd insurance-claims

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
docker-compose up -d

# Verify it's running
docker ps
```

**MinIO Console:** http://localhost:9101
- **User:** admin
- **Password:** adminpassword123

### 3. Upload Sample Data

```bash
# Upload data to MinIO (50 records per file - already in data/raw/)
python scripts/upload_to_minio.py
```

This will upload:
- `data/raw/customers.csv` (50 customers)
- `data/raw/policies.csv` (50 policies)
- `data/raw/claims.csv` (50 claims)

> **Note:** We use small datasets (50 records) for MVP - sufficient to validate logic and demonstrate understanding.

### 4. Connect Fabric to MinIO

#### Option A: Publicly Accessible MinIO (Ngrok/Tunneling)

If you need Fabric to access your local MinIO:

```bash
# Install ngrok
# https://ngrok.com/download

# Expose MinIO port 9100
ngrok http 9100
```

Use the public URL provided by ngrok (e.g., `https://xxxx.ngrok.io`)

#### Option B: Manual Upload

```bash
# Export data for manual upload to Fabric
# Files are in data/raw/
```

### 5. Configure Microsoft Fabric

#### 5.1 Create Workspace and Lakehouse

1. Go to [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. Create a new **Workspace** named `Insurance Analytics`
3. Inside the workspace, create a **Lakehouse** named `insurance_lakehouse`

#### 5.2 Create Data Pipeline

1. In your workspace, create a new **Data Pipeline**
2. Configure S3 connection (MinIO is S3-compatible):
   - **Endpoint:** `http://your-ip:9100` or ngrok URL
   - **Access Key:** `admin`
   - **Secret Key:** `adminpassword123`
   - **Bucket:** `insurance-data`

3. Create **Copy Data** activities for each file:
   - `bronze/customers.csv` → `bronze/customers` Delta table
   - `bronze/policies.csv` → `bronze/policies` Delta table
   - `bronze/claims.csv` → `bronze/claims` Delta table

#### 5.3 Create PySpark Notebooks

See reference implementation in [Notebook+1.ipynb](Notebook+1.ipynb)

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

## 📁 Project Structure

```
insurance-claims/
├── docker-compose.yml          # MinIO configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Files to ignore
├── README.md                  # This file
├── CLAUDE.md                  # Developer guide for AI assistants
│
├── data/
│   └── raw/                   # CSV files (50 records each)
│       ├── customers.csv
│       ├── policies.csv
│       └── claims.csv
│
├── scripts/
│   └── upload_to_minio.py     # Upload data to MinIO
│
├── docs/                      # Documentation (empty - to be populated)
│
├── notebooks/                 # Local notebooks (empty)
│
├── Notebook+1.ipynb           # Fabric notebook export (Bronze→Silver→Gold)
│
├── minio/
│   └── data/                  # MinIO persistent storage (gitignored)
│
└── notes/
    └── CLAUDE.md              # Detailed architecture guide (Spanish)
```

## 🎯 Implementation Stages (MVP)

### Stage 1: FOUNDATION - "It Works"
- ✅ MinIO running in Docker
- ✅ 50 records in each CSV file
- 🔲 Fabric workspace created
- 🔲 Data ingested to Bronze layer

### Stage 2: TRANSFORMATION - "It's Clean"
- 🔲 Silver layer notebook created
- 🔲 Data cleaning implemented
- 🔲 3 Silver Delta tables written

### Stage 3: ANALYTICS - "It Answers Questions"
- 🔲 Tables joined (claims → policies → customers)
- 🔲 Gold aggregation table created
- 🔲 Business metrics calculated

### Stage 4: VISUALIZATION - "It's Presentable"
- 🔲 Power BI connected to Gold layer
- 🔲 Dashboard created
- 🔲 Portfolio screenshots captured

### Stage 5 (Optional): SCALE - "It Handles More"
- 🔲 Script to generate 200-500 records
- 🔲 Pipeline re-run with larger dataset
- 🔲 Performance documented

### Stage 6 (Optional): PRODUCTION-READY - "It's Robust"
- 🔲 Data quality checks added
- 🔲 Error handling implemented
- 🔲 Automated orchestration configured

## 🔧 Useful Commands

```bash
# View MinIO logs
docker-compose logs -f minio

# Stop MinIO
docker-compose down

# Clean MinIO data (destructive)
docker-compose down -v

# Upload data to MinIO
python scripts/upload_to_minio.py

# Verify data in MinIO
# Access http://localhost:9101 and explore the bucket
```

## 📝 Portfolio Highlights

This project demonstrates:

- ✅ **Medallion Architecture** (Bronze/Silver/Gold)
- ✅ **End-to-End Data Engineering**
- ✅ **Microsoft Fabric** (Lakehouse, Data Pipelines, PySpark)
- ✅ **PySpark Processing** for cleaning and transformations
- ✅ **S3/MinIO Integration**
- ✅ **Power BI Visualization**
- ✅ **Docker** for local infrastructure
- ✅ **Python** for automation
- ✅ **Delta Lake** format (ACID, time travel)
- ✅ **MVP Approach** (incremental value delivery)

## 🤝 Design Decisions

| Component | Azure Original | Alternative Chosen | Reason |
|-----------|---------------|-------------------|--------|
| Storage | Azure Data Lake Storage | MinIO (local) | No Azure account needed, S3-compatible |
| Processing | Azure Synapse | Microsoft Fabric | Trial account available |
| Orchestration | Azure Data Factory | Fabric Data Pipelines | Included in Fabric |
| Visualization | Power BI Service | Power BI (Fabric) | Included in Fabric |

## 📚 Resources

- [Microsoft Fabric Docs](https://learn.microsoft.com/en-us/fabric/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Delta Lake](https://delta.io/)

## 📄 License

MIT License - Free to use in your portfolio

---

**Built to demonstrate modern data engineering skills for professional portfolios**
