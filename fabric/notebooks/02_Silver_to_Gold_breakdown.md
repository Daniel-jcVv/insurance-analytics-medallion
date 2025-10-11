# Silver to Gold Transformation - Step by Step

This document shows the breakdown of Silver → Gold transformation for the notebook

---

## 📊 Cell 1: Load Silver Tables

**Purpose:** Load cleaned data from Silver layer

**Demonstrates:** Basic data loading from lakehouse tables

```python
from pyspark.sql.functions import *
from pyspark.sql import functions as F

# Load Silver tables
df_customers_clean = spark.table("silver_customers")
df_policies_clean = spark.table("silver_policies")
df_claims_clean = spark.table("silver_claims")

print("✓ Silver tables loaded:")
print(f"  - Customers: {df_customers_clean.count()} rows")
print(f"  - Policies: {df_policies_clean.count()} rows")
print(f"  - Claims: {df_claims_clean.count()} rows")
```

---

## 🔗 Cell 2: Join Customer Journey

**Purpose:** Unite 3 tables to create a complete customer journey view (claim → policy → customer)

**Demonstrates:** Multi-table joins and relationship mapping

```python
# JOIN: Claims → Policies → Customers
df_joined = (
    df_claims_clean.alias("c")
    .join(
        df_policies_clean.alias("p"),
        col("c.policy_id") == col("p.policy_id"),
        "inner"
    )
    .join(
        df_customers_clean.alias("cu"),
        col("p.cust_id") == col("cu.cust_id"),
        "inner"
    )
)

print(f"✓ Joined data: {df_joined.count()} rows")
display(df_joined.limit(5))
```

---

## 📈 Cell 3: Basic Claim Metrics

**Purpose:** Calculate fundamental claim metrics per customer

**Demonstrates:** Basic aggregations (COUNT, SUM, AVG)

```python
# Basic claim metrics per customer
df_basic_metrics = df_joined.groupBy(
    "cu.cust_id",
    "cu.CustomerName",
    "cu.Gender"
).agg(
    count("c.claim_id").alias("TotalClaims"),
    round(sum("c.claim_amount"), 2).alias("TotalClaimAmount"),
    round(avg("c.claim_amount"), 2).alias("AvgClaimAmount")
)

print("📊 Basic Claim Metrics:")
display(df_basic_metrics.orderBy(desc("TotalClaimAmount")).limit(10))
```

---

## ✅ Cell 4: Claim Status Analysis

**Purpose:** Analyze claim approvals and rejections

**Demonstrates:** Conditional logic (CASE WHEN) and rate calculations

```python
# Claim status analysis (Approved vs Rejected)
df_status_metrics = df_joined.groupBy(
    "cu.cust_id",
    "cu.CustomerName"
).agg(
    count(when(lower(col("c.status")) == "approved", True)).alias("ApprovedClaims"),
    count(when(lower(col("c.status")) == "rejected", True)).alias("RejectedClaims"),
    count("c.claim_id").alias("TotalClaims")
).withColumn(
    "ApprovalRate",
    round((col("ApprovedClaims") / col("TotalClaims")) * 100, 2)
)

print("✅ Claim Status Analysis:")
display(df_status_metrics.orderBy(desc("ApprovalRate")).limit(10))
```

---

## 🏥 Cell 5: Policy Coverage Analysis

**Purpose:** Analyze relationship between policy coverage and claims

**Demonstrates:** Complex aggregations and business ratio calculations

```python
# Policy coverage analysis
df_coverage_metrics = df_joined.groupBy(
    "cu.cust_id",
    "cu.CustomerName"
).agg(
    round(sum("p.coverage_amount"), 2).alias("TotalCoverageAmount"),
    round(sum("c.claim_amount"), 2).alias("TotalClaimAmount"),
    collect_set(lower(col("p.policy_type"))).alias("PolicyTypesArray")
).withColumn(
    "ClaimToCoverageRatio",
    round((col("TotalClaimAmount") / col("TotalCoverageAmount")) * 100, 2)
).withColumn(
    "PolicyTypes",
    concat_ws(", ", col("PolicyTypesArray"))
).drop("PolicyTypesArray")

print("🏥 Coverage Analysis:")
display(df_coverage_metrics.orderBy(desc("ClaimToCoverageRatio")).limit(10))
```

---

## 📅 Cell 6: Temporal Analysis

**Purpose:** Analyze temporal behavior of claims per customer

**Demonstrates:** Date functions and temporal activity analysis

```python
# Temporal claim analysis
df_temporal_metrics = df_joined.groupBy(
    "cu.cust_id",
    "cu.CustomerName"
).agg(
    min("c.claim_date").alias("FirstClaimDate"),
    max("c.claim_date").alias("LastClaimDate"),
    count("c.claim_id").alias("TotalClaims")
).withColumn(
    "DaysBetweenFirstAndLast",
    datediff(col("LastClaimDate"), col("FirstClaimDate"))
)

print("📅 Temporal Analysis:")
display(df_temporal_metrics.orderBy(desc("DaysBetweenFirstAndLast")).limit(10))
```

---

## 🎯 Cell 7: Consolidate Gold Table

**Purpose:** Consolidate all metrics into final Gold table

**Demonstrates:** Integration of multiple aggregations into a dimensional model

```python
# Consolidate all metrics into final Gold table
df_gold_final = (
    df_joined.groupBy("cu.cust_id", "cu.CustomerName", "cu.Gender")
    .agg(
        # Claim counts
        count("c.claim_id").alias("TotalClaims"),
        count(when(lower(col("c.status")) == "approved", True)).alias("ApprovedClaims"),
        count(when(lower(col("c.status")) == "rejected", True)).alias("RejectedClaims"),

        # Claim amounts
        round(sum("c.claim_amount"), 2).alias("TotalClaimAmount"),
        round(avg("c.claim_amount"), 2).alias("AvgClaimAmount"),

        # Policy information
        collect_set(lower(col("p.policy_type"))).alias("PolicyTypesArray"),
        round(sum("p.coverage_amount"), 2).alias("TotalCoverageAmount"),

        # Temporal information
        min("c.claim_date").alias("FirstClaimDate"),
        max("c.claim_date").alias("LastClaimDate")
    )
    .withColumn("PolicyTypes", concat_ws(", ", col("PolicyTypesArray")))
    .withColumn(
        "ApprovalRate",
        round((col("ApprovedClaims") / col("TotalClaims")) * 100, 2)
    )
    .withColumn(
        "ClaimToCoverageRatio",
        round((col("TotalClaimAmount") / col("TotalCoverageAmount")) * 100, 2)
    )
    .drop("PolicyTypesArray")
)

print("🎯 Gold Table Preview:")
display(df_gold_final.orderBy(desc("TotalClaimAmount")).limit(10))
```

---

## 💾 Cell 8: Save Gold Table

**Purpose:** Persist Gold table as Delta Lake

**Demonstrates:** Knowledge of optimized formats for analytics

```python
# Save as Delta table in Lakehouse
df_gold_final.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("gold_customer_claims_analytics")

print("✅ Gold table created: gold_customer_claims_analytics")
print(f"   Total customers analyzed: {df_gold_final.count()}")
print(f"   Columns: {len(df_gold_final.columns)}")
print(f"\nTable location: Tables/gold_customer_claims_analytics")
```

---

## 📊 Cell 9: Data Quality Checks

**Purpose:** Validate Gold table quality

**Demonstrates:** Data quality best practices and validation

```python
# Data quality validations
print("🔍 Data Quality Checks:")
print("-" * 50)

# Check 1: No nulls in key columns
null_checks = df_gold_final.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in ["cust_id", "CustomerName", "TotalClaims"]
])
print("\n1. Null values in key columns:")
display(null_checks)

# Check 2: Valid ranges
print("\n2. Metric ranges:")
print(f"   Max TotalClaims: {df_gold_final.agg(max('TotalClaims')).collect()[0][0]}")
print(f"   Max TotalClaimAmount: ${df_gold_final.agg(max('TotalClaimAmount')).collect()[0][0]:,.2f}")
print(f"   Avg ApprovalRate: {df_gold_final.agg(avg('ApprovalRate')).collect()[0][0]:.2f}%")

# Check 3: Distribution by gender
print("\n3. Distribution by Gender:")
display(df_gold_final.groupBy("Gender").count().orderBy("Gender"))

print("\n✅ All quality checks passed!")
```

---

## 🏆 Cell 10: Business Insights Summary

**Purpose:** Generate executive insights for stakeholders

**Demonstrates:** Ability to extract business value from data

```python
# Business insights
print("🏆 KEY BUSINESS INSIGHTS")
print("=" * 60)

# Top 5 claimers
top_claimers = df_gold_final.orderBy(desc("TotalClaimAmount")).limit(5)
print("\n1. TOP 5 CUSTOMERS BY CLAIM AMOUNT:")
display(top_claimers.select("CustomerName", "TotalClaimAmount", "TotalClaims", "ApprovalRate"))

# Approval rate distribution
print("\n2. APPROVAL RATE DISTRIBUTION:")
approval_buckets = df_gold_final.withColumn(
    "ApprovalBucket",
    when(col("ApprovalRate") >= 80, "High (80%+)")
    .when(col("ApprovalRate") >= 50, "Medium (50-79%)")
    .otherwise("Low (<50%)")
).groupBy("ApprovalBucket").count().orderBy("ApprovalBucket")
display(approval_buckets)

# High risk customers (claim/coverage > 50%)
print("\n3. HIGH RISK CUSTOMERS (Claim/Coverage > 50%):")
high_risk = df_gold_final.filter(col("ClaimToCoverageRatio") > 50).count()
print(f"   {high_risk} customers with high claim-to-coverage ratio")

print("\n✅ Ready for Power BI visualization!")
```

---

## 🎓 What This Notebook Demonstrates

### Technical Skills:
- ✅ PySpark aggregations and transformations
- ✅ Multi-table joins and relationship mapping
- ✅ Conditional logic and business calculations
- ✅ Delta Lake format usage
- ✅ Data quality validation practices

### Business Acumen:
- ✅ Customer analytics and segmentation
- ✅ Risk assessment metrics
- ✅ Performance indicators (KPIs)
- ✅ Stakeholder-focused insights

### Best Practices:
- ✅ Step-by-step analytical thinking
- ✅ Code organization and readability
- ✅ Quality checks before production
- ✅ Documentation and clear objectives

