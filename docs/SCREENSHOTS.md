# 📸 Screenshot Guide for Portfolio

## 🎯 Purpose
Screenshots provide **visual proof** that your project works. They're essential for:
- Portfolio README on GitHub
- LinkedIn posts
- Job applications
- Technical documentation

---

## ✅ ESSENTIAL Screenshots (Must Have)

### **1. MinIO Console - Data Uploaded** ⭐⭐⭐
**When:** After running `python scripts/upload_to_minio.py`

**Where:** http://localhost:9101

**What to show:**
- Bucket `insurance-data`
- Folder `bronze/` with 3 CSV files
- File sizes visible

**Why:** Proves local object storage setup works

**Filename:** `01-minio-bronze-layer.png`

---

### **2. Fabric Workspace Overview** ⭐⭐⭐
**When:** After creating workspace in Fabric

**Where:** https://app.fabric.microsoft.com

**What to show:**
- Workspace name: "Insurance Analytics"
- Lakehouse visible: "insurance_lakehouse"
- Clean workspace view

**Why:** Shows you can navigate Fabric

**Filename:** `02-fabric-workspace.png`

---

### **3. Fabric Lakehouse - Bronze Files** ⭐⭐⭐
**When:** After uploading CSVs to Lakehouse

**Where:** Lakehouse → Files → bronze/

**What to show:**
- 3 CSV files in bronze folder
- File sizes
- Upload timestamp

**Why:** Proves data ingestion to cloud

**Filename:** `03-fabric-bronze-files.png`

---

### **4. PySpark Notebook - Bronze to Silver** ⭐⭐⭐
**When:** After creating Silver layer transformation

**What to show:**
- Code cells with transformations
- Data preview (df.show())
- Success message
- Cell execution numbers

**Why:** Demonstrates PySpark skills

**Filename:** `04-notebook-bronze-to-silver.png`

---

### **5. Fabric Lakehouse - Silver Tables** ⭐⭐⭐
**When:** After running Silver notebook

**Where:** Lakehouse → Tables

**What to show:**
- 3 Delta tables in Silver
- Table schemas
- Row counts

**Why:** Proves transformation worked

**Filename:** `05-fabric-silver-tables.png`

---

### **6. PySpark Notebook - Silver to Gold** ⭐⭐⭐
**When:** After creating Gold aggregations

**What to show:**
- Join operations (claims → policies → customers)
- Aggregations (groupBy, agg)
- Business metrics calculated
- Final data preview

**Why:** Shows analytical thinking

**Filename:** `06-notebook-silver-to-gold.png`

---

### **7. Fabric Lakehouse - Gold Table** ⭐⭐⭐
**When:** After running Gold notebook

**Where:** Lakehouse → Tables

**What to show:**
- Gold aggregation table
- Schema with business metrics
- Sample data preview

**Why:** Proves end-to-end pipeline works

**Filename:** `07-fabric-gold-table.png`

---

### **8. Power BI Dashboard** ⭐⭐⭐⭐⭐
**When:** After creating visualizations

**What to show:**
- 4-6 visuals on dashboard
- KPIs clearly visible
- Clean, professional layout
- Filters/slicers working

**Why:** THIS IS THE MONEY SHOT - what business sees

**Filename:** `08-powerbi-dashboard.png`

---

## 🟡 NICE TO HAVE Screenshots (Optional)

### **9. Terminal - Tests Passing**
```bash
pytest tests/ -v
```
**Shows:** All 5 tests passing

**Filename:** `09-tests-passing.png`

---

### **10. Architecture Diagram**
Create a simple diagram showing:
```
CSV → MinIO → (Manual) → Fabric Bronze → Silver → Gold → Power BI
```

**Filename:** `10-architecture-diagram.png`

---

### **11. Code Quality**
**Show:** Clean Python code in IDE with:
- Proper formatting
- Type hints
- Docstrings

**Filename:** `11-clean-code.png`

---

## 📋 Screenshot Checklist

Before taking each screenshot:

- [ ] **Hide sensitive info** (emails, real names, tokens)
- [ ] **Use light theme** (better for portfolio/LinkedIn)
- [ ] **Full screen or focused crop** (no distractions)
- [ ] **Good resolution** (at least 1920x1080)
- [ ] **Clear text** (zoom in if needed)
- [ ] **Professional browser tabs** (close YouTube, Reddit, etc.)

---

## 🎨 Recommended Tools

**For Screenshots:**
- Windows: Snipping Tool / Snip & Sketch
- Mac: Cmd + Shift + 4
- Linux: Flameshot / GNOME Screenshot

**For Annotations (optional):**
- Excalidraw (arrows, boxes, text)
- PowerPoint (quick annotations)
- GIMP (advanced editing)

**For Architecture Diagrams:**
- Excalidraw (https://excalidraw.com)
- Draw.io (https://draw.io)
- Mermaid (markdown diagrams in README)

---

## 📂 Folder Structure

```
insurance-claims/
└── docs/
    ├── screenshots/
    │   ├── 01-minio-bronze-layer.png
    │   ├── 02-fabric-workspace.png
    │   ├── 03-fabric-bronze-files.png
    │   ├── 04-notebook-bronze-to-silver.png
    │   ├── 05-fabric-silver-tables.png
    │   ├── 06-notebook-silver-to-gold.png
    │   ├── 07-fabric-gold-table.png
    │   └── 08-powerbi-dashboard.png ⭐ MOST IMPORTANT
    └── SCREENSHOTS.md (this file)
```

---

## 🎯 For README.md

Add this section to your main README:

```markdown
## 📊 Project Screenshots

### MinIO Object Storage
![MinIO Bronze Layer](docs/screenshots/01-minio-bronze-layer.png)

### Microsoft Fabric - Medallion Architecture

**Bronze Layer (Raw Data)**
![Fabric Bronze](docs/screenshots/03-fabric-bronze-files.png)

**Silver Layer (Clean & Joined)**
![Fabric Silver](docs/screenshots/05-fabric-silver-tables.png)

**Gold Layer (Business Metrics)**
![Fabric Gold](docs/screenshots/07-fabric-gold-table.png)

### Power BI Dashboard
![Dashboard](docs/screenshots/08-powerbi-dashboard.png)

> See [docs/screenshots/](docs/screenshots/) for more detailed screenshots
```

---

## ⚠️ What NOT to Screenshot

- ❌ Terminal with errors (unless for troubleshooting docs)
- ❌ Personal information (emails, real company data)
- ❌ API keys or credentials
- ❌ Messy desktop backgrounds
- ❌ Random browser tabs open
- ❌ Chat applications in background

---

## 💡 Pro Tips

1. **Take screenshots as you go** - Don't wait until the end
2. **Number them sequentially** - Shows workflow progression
3. **Light theme only** - Dark themes look unprofessional in docs
4. **Annotate key areas** - Add arrows/boxes to highlight important parts
5. **Compress images** - Use tinypng.com before committing to Git
6. **Add alt text** - Helps with accessibility and SEO

---

## ✅ Final Checklist

Before publishing your portfolio:

- [ ] All 8 essential screenshots taken
- [ ] Screenshots are clear and professional
- [ ] No sensitive information visible
- [ ] Files properly named and organized
- [ ] Images compressed (<500KB each)
- [ ] Added to README.md with descriptions
- [ ] Tested image links work in GitHub

---

**Remember:** The Power BI dashboard screenshot (#8) is the **MOST IMPORTANT**.
That's what recruiters and hiring managers care about most - the final business value.
