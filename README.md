# AWS Retail Data Lake — Sales Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS">
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=databricks&logoColor=white" alt="SQL">
</p>

<p align="center">
  A retail data engineering project that cleans order data, prepares curated datasets, and presents sales insights through a Power BI dashboard.
</p>

<p align="center">
  <b>Python • Pandas • Amazon S3 • AWS Glue • Amazon Athena • Power BI</b>
</p>

---

## 📌 Project Overview

The **AWS Retail Data Lake — Sales Dashboard** project demonstrates a retail data processing workflow using Python, Pandas, AWS-related components, SQL, and Power BI.

The pipeline processes retail order data, separates valid and rejected records, generates a data quality report, and prepares curated data for sales analysis.

The project also includes AWS Glue ETL code and Amazon Athena SQL queries to support future cloud-based processing and analysis.

## 🎯 Project Objectives

- Clean and validate retail order data.
- Identify invalid and duplicate records.
- Separate curated and rejected records.
- Generate a data quality report.
- Organize data for downstream analysis.
- Visualize sales performance using Power BI.
- Prepare AWS Glue and Athena components for cloud integration.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and ETL logic |
| Pandas | Data cleaning and transformation |
| SQL | Querying and sales analysis |
| Amazon S3 | Cloud object storage |
| AWS Glue / PySpark | Cloud ETL processing |
| Amazon Athena | SQL analysis of data in S3 |
| Power BI | Interactive data visualization |
| Git & GitHub | Version control and project hosting |

## 🔄 Project Architecture

<p align="center">
  <img src="https://img.shields.io/badge/Step_1-Raw_Data-4479A1?style=flat-square" alt="Raw Data">
  &nbsp;→&nbsp;
  <img src="https://img.shields.io/badge/Step_2-Python_&_Pandas-3776AB?style=flat-square" alt="Python and Pandas">
  &nbsp;→&nbsp;
  <img src="https://img.shields.io/badge/Step_3-Curated_Data-228B22?style=flat-square" alt="Curated Data">
</p>

```text
                  RETAIL ORDER CSV
                         |
                         v
                Python + Pandas ETL
                         |
                Data Cleaning & Validation
                         |
               +---------+---------+
               |                   |
               v                   v
         Curated Data        Rejected Data
               |
               v
       Data Quality Report
               |
               v
         Power BI Dashboard
               |
               v
       Sales Insights & Analysis
```

**AWS integration components:**

```text
Amazon S3 → AWS Glue → Amazon Athena → Sales Analysis
```

The AWS flow represents the intended cloud integration. Glue job execution and Athena query results should be marked as completed only after they have been tested successfully.

## ✨ Key Features

- Retail order data cleaning and validation.
- Duplicate and invalid record identification.
- Curated and rejected CSV outputs.
- Data quality reporting.
- Sales analysis by category and region.
- Order-status analysis.
- Power BI dashboard with key sales metrics.
- AWS Glue ETL script and Athena SQL query files.

## 📊 Power BI Dashboard

The current sample dashboard reports the following metrics:

<p align="center">
  <img src="https://img.shields.io/badge/Total_Sales-9.28K-0078D4?style=for-the-badge" alt="Total Sales 9.28K">
  <img src="https://img.shields.io/badge/Total_Orders-180-6C63FF?style=for-the-badge" alt="Total Orders 180">
  <img src="https://img.shields.io/badge/Quantity_Sold-433-159957?style=for-the-badge" alt="Quantity Sold 433">
</p>

### Dashboard Analysis

- **Sales by Category:** Compare sales across product categories.
- **Sales by Region:** Examine sales distribution across regions.
- **Orders by Status:** Review order-status distribution.
- **Key Performance Indicators:** Monitor sales, orders, and quantity sold.

> **Note:** These metrics are based on the current sample dataset. Confirm the values and calculation definitions against the actual dataset before presenting them as final results.

## 🖼️ Project Screenshots

### 1. Power BI Sales Dashboard

![Power BI Sales Dashboard](docs/screenshots/power_bi_dashboard.png)

### 2. Project Folder Structure

![Project Folder View](docs/screenshots/project_folder_view_1.png)

### 3. Amazon S3 Bucket and Folders

![Amazon S3 Bucket Folders](docs/screenshots/s3_bucket_folders.png)

### 4. Amazon S3 — Raw Data Upload

![Amazon S3 Raw Data Upload](docs/screenshots/s3_raw_upload.png)

### 5. Amazon S3 — Processed Data Upload

![Amazon S3 Processed Data Upload](docs/screenshots/s3_processed_upload.png)

> Make sure the screenshot filenames above match the actual filenames in your repository. Replace or remove any screenshot that you have not uploaded.

## 📁 Repository Structure

```text
aws-retail-data-lake/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   └── etl.py
│
├── glue/
│   └── glue_etl.py
│
├── sql/
│   └── sales_analysis.sql
│
├── dashboard/
│   └── README.md
│
├── docs/
│   ├── project_architecture.md
│   └── screenshots/
│       ├── power_bi_dashboard.png
│       ├── project_folder_view_1.png
│       ├── s3_bucket_folders.png
│       ├── s3_raw_upload.png
│       └── s3_processed_upload.png
│
├── requirements.txt
├── .gitignore
└── README.md
```

*This structure describes the intended repository layout. Keep only files and folders that actually exist in your project.*

## 🚀 Getting Started

### Prerequisites

- Python installed on your computer.
- Git installed (optional for command-line uploads).
- The retail sales CSV dataset.
- Power BI Desktop for dashboard development.
- An AWS account if you want to run the cloud components.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/aws-retail-data-lake.git
cd aws-retail-data-lake
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Python ETL Script

```bash
python scripts/etl.py
```

Ensure the input dataset is placed at the path expected by the script. The exact input filename and required columns depend on your implementation.

### 4. AWS Integration

For cloud integration:

1. Upload the appropriate raw data to an Amazon S3 bucket.
2. Configure and test the AWS Glue ETL job.
3. Configure the Glue Data Catalog if required.
4. Run and validate the Athena SQL queries.
5. Connect the prepared data to Power BI if that integration is part of your implementation.

AWS configuration, permissions, and resource names must be supplied for your own account.

## 🔮 Future Improvements

- Execute and validate the AWS Glue ETL job.
- Configure the Glue Data Catalog.
- Run and validate Amazon Athena queries.
- Add time-based sales trend analysis.
- Add interactive dashboard filters.
- Automate pipeline execution and monitoring.
- Improve data quality checks and error reporting.

## 👩‍💻 Author

**Riya Sharma**

B.Tech — Artificial Intelligence & Data Science

**Areas of interest:** Data Engineering | Python | SQL | AWS | Power BI

---

<p align="center">
  <i>Built to explore retail data processing, cloud data architecture, and business intelligence.</i>
</p>
