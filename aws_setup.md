# AWS setup guide (cost-conscious)

## Before creating resources

1. Sign in to the AWS Console and select a region, e.g. `ap-south-1` (Mumbai).
2. Check your account's current Free Tier / credits and current pricing for S3, Glue, Athena, and CloudWatch. Free usage is not guaranteed for every account or service.
3. Set an AWS Budget alert if available. **An alert is not a hard spending cap.**
4. Use synthetic data only. Do not upload credentials or personal data.

## 1. Create an S3 bucket

1. Open Amazon S3 → Create bucket.
2. Choose a globally unique name, e.g. `retail-data-lake-<random-suffix>`.
3. Keep **Block all public access** enabled.
4. Leave ACLs disabled and use bucket-owner-enforced object ownership.
5. Create folders/prefixes:
   - `raw/orders/`
   - `curated/orders/`
   - `quality/orders/`
6. Upload `data/raw/orders.csv` to `raw/orders/orders.csv`.

Do not make the bucket public. The Glue job and Athena access it through IAM permissions.

## 2. Create or select a Glue IAM role

Create an IAM role for AWS Glue (trusted service: `glue.amazonaws.com`) or use a suitable existing Glue service role. Attach the AWS-managed service-role policy needed by Glue, then add a least-privilege inline policy scoped to your bucket and catalog resources. Review policy requirements for your account and region; this sample is a learning guide, not a universal production policy.

At minimum, the job role typically needs:
- `s3:ListBucket` on the bucket, scoped to the required prefixes where possible.
- `s3:GetObject` for `raw/orders/*`.
- `s3:PutObject`, `s3:AbortMultipartUpload`, and appropriate list permissions for `curated/orders/*` and `quality/orders/*`.
- Glue Data Catalog actions for the target database/table.
- CloudWatch Logs permissions for job logs.
- If using SSE-KMS, required KMS permissions.

Never give broad administrator permissions just to make the demo work.

## 3. Create the Glue ETL job

1. Open AWS Glue → ETL jobs → Visual ETL / Script editor (console wording may change).
2. Create a Spark job and choose the Glue version available in your account. Glue 4.0+ is recommended for this script.
3. Set the IAM role from step 2.
4. Upload `glue/retail_orders_etl.py` to an S3 script location, or paste its content in the script editor.
5. Set job parameters (arguments) exactly:
   - `--SOURCE_S3_PATH` = `s3://YOUR_BUCKET/raw/orders/`
   - `--TARGET_S3_PATH` = `s3://YOUR_BUCKET/curated/orders/`
   - `--QUALITY_S3_PATH` = `s3://YOUR_BUCKET/quality/orders/`
   - `--DATABASE_NAME` = `retail_analytics`
   - `--TABLE_NAME` = `curated_orders`
6. Choose the smallest suitable worker configuration for this tiny sample. Review the current Glue billing model before running.
7. Save and run. Inspect the job run and CloudWatch logs if it fails.

The sample job does a full refresh and overwrites curated/quality prefixes. Do not point it at important existing data.

## 4. Catalog and query in Athena

1. Open Athena and set a query result location in S3, e.g. `s3://YOUR_BUCKET/athena-results/`. Create the prefix if needed.
2. If the Glue job successfully created the table, inspect `retail_analytics.curated_orders`.
3. Otherwise, replace `YOUR_BUCKET` in `sql/athena_ddl.sql`, run the DDL, then run `MSCK REPAIR TABLE retail_analytics.curated_orders;`.
4. Run queries from `sql/athena_analytics.sql`.
5. Use the Athena query details to inspect data scanned. Keep queries scoped by `order_year` and `order_month` where possible.

## 5. Verify outputs

Expected S3 outputs:
- `curated/orders/order_year=2025/order_month=.../` containing Parquet files
- `quality/orders/rejected_records/`
- `quality/orders/run_summary/`

Expected sample behavior: input contains deliberately invalid and duplicate records, so curated rows should be fewer than input rows and rejected output should not be empty. Exact counts can vary if you edit the sample.

## 6. Clean up to avoid ongoing charges

After collecting screenshots and results:
1. Stop or delete Glue jobs you no longer need.
2. Delete the Glue database/table if no longer needed.
3. Empty the S3 bucket, including Athena query results, scripts, and outputs; then delete the bucket.
4. Review CloudWatch log groups and delete demo logs if no longer needed.
5. Review AWS Budgets and billing for unexpected resources.

Deleting the local GitHub project does not delete AWS resources. Verify the AWS console separately.

## Troubleshooting

- **AccessDenied:** check the Glue role's S3 and Glue Catalog permissions; also check bucket policy and encryption/KMS.
- **Athena table empty:** confirm the curated prefix has Parquet output and that the table location exactly matches it. Repair partitions or use the DDL.
- **Glue job cannot find input:** verify source prefix ends in `/` and the CSV is under `raw/orders/`.
- **Script/runtime mismatch:** use Glue 4.0+ and review the job's Python/Spark runtime.
- **Athena query fails due to output location:** configure the query result S3 location in Athena workgroup settings.
