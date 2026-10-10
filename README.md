# AWS Retail Data Lake — Sales Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/AWS-S3%20%7C%20Glue%20%7C%20Athena-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS Services">
  <img src="https://img.shields.io/badge/Python-Pandas-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python and Pandas">
  <img src="https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
</p>

<p align="center">
  A retail sales data pipeline project using Python, AWS cloud storage, and Power BI to organize sales data and visualize key business metrics.
</p>

---

## Project Overview

The **AWS Retail Data Lake — Sales Dashboard** project demonstrates how retail sales data can be processed, organized, and prepared for analytics using Python and AWS services.

The project includes Python-based data processing with Pandas, Amazon S3 storage for raw and processed data, SQL files for analytics, and a Power BI dashboard for sales visualization.

## Technologies Used

- **Python** — Data processing
- **Pandas** — Data cleaning and transformation
- **Amazon S3** — Cloud storage for raw and processed datasets
- **AWS Glue** — Planned ETL integration
- **Amazon Athena** — Planned SQL-based data analysis
- **Power BI** — Interactive sales dashboard
- **SQL** — Analytical queries

## Project Architecture

<p align="center">
  <b>Retail Sales Dataset</b><br>
  ↓<br>
  <b>Python + Pandas (Data Processing)</b><br>
  ↓<br>
  <b>Processed Dataset</b><br>
  ↓<br>
  <b>Amazon S3 (Raw and Processed Data)</b><br>
  ↓<br>
  <b>AWS Glue and Amazon Athena (Planned Integration)</b><br>
  ↓<br>
  <b>Power BI Sales Dashboard</b>
</p>

## Project Screenshots

### 1. Power BI Sales Dashboard

<p align="center">
  <img src="https://raw.githubusercontent.com/Riya-12-Sharma/aws-retail-data-lake-pipeline/main/docs/screenshots/dashboard_screenshot.png..png" alt="Power BI Retail Sales Dashboard" width="900">
</p>

**Dashboard KPIs:**

| Metric | Value |
|---|---:|
| Total Sales | 9.28K |
| Total Orders | 180 |
| Quantity Sold | 433 |

The dashboard presents key sales metrics and visual breakdowns of retail data.

### 2. Project Folder Structure

<p align="center">
  <img src="https://raw.githubusercontent.com/Riya-12-Sharma/aws-retail-data-lake-pipeline/main/docs/screenshots/project_folder_view_1.png.png" alt="Project Folder Structure" width="850">
</p>

This screenshot shows the project files and folder organization.

### 3. Amazon S3 Bucket Structure

<p align="center">
  <img src="https://raw.githubusercontent.com/Riya-12-Sharma/aws-retail-data-lake-pipeline/main/docs/screenshots/s3_bucket_folders.png.png" alt="Amazon S3 Bucket Folders" width="850">
</p>

The S3 bucket is organized to separate raw and processed data.

### 4. Raw Data Uploaded to Amazon S3

<p align="center">
  <img src="https://raw.githubusercontent.com/Riya-12-Sharma/aws-retail-data-lake-pipeline/main/docs/screenshots/s3_raw_upload.png.png" alt="Raw Data Uploaded to S3" width="850">
</p>

This screenshot shows the raw data stored in the Amazon S3 bucket.

### 5. Processed Data Uploaded to Amazon S3

<p align="center">
  <img src="https://raw.githubusercontent.com/Riya-12-Sharma/aws-retail-data-lake-pipeline/main/docs/screenshots/s3_processed_upload.png.png" alt="Processed Data Uploaded to S3" width="850">
</p>

This screenshot shows the processed data stored separately from the raw dataset.

## Key Features

- Python-based data processing using Pandas
- Separate storage for raw and processed data
- Amazon S3 integration for cloud-based dataset storage
- Power BI dashboard for retail sales analysis
- SQL query files prepared for analytical use
- Project structure designed to support future AWS Glue and Athena integration

## Project Structure

```text
aws-retail-data-lake-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── screenshots/
│       ├── project_folder_view_1.png.png
│       ├── s3_bucket_folders.png.png
│       ├── s3_raw_upload.png.png
│       ├── s3_processed_upload.png.png
│       └── dashboard_screenshot.png..png
│
├── scripts/
│   └── data processing scripts
│
├── sql/
│   └── Athena query files
│
├── README.md
└── requirements.txt
```

*Note: Update the folder and file names above if your actual repository structure differs.*

## How to Run the Python Data Processing

### 1. Clone the repository

```bash
git clone https://github.com/Riya-12-Sharma/aws-retail-data-lake-pipeline.git
```

### 2. Open the project folder

```bash
cd aws-retail-data-lake-pipeline
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the processing script

Run the Python script that is present in your repository. For example:

```bash
python scripts/your_script_name.py
```

Replace `your_script_name.py` with the actual script filename.

## Future Improvements

- Complete and validate AWS Glue ETL job execution
- Configure and test the Amazon Athena tables and SQL queries
- Automate data ingestion and processing
- Connect processed data to Power BI for refreshable reporting
- Add data quality checks and pipeline monitoring

## Author

**Riya Sharma**  
B.Tech — Artificial Intelligence and Data Science

GitHub: [Riya-12-Sharma](https://github.com/Riya-12-Sharma)

---

<p align="center">
  <i>Built as a data engineering and business intelligence portfolio project.</i>
</p>
