# Architecture and engineering decisions

## Data flow

1. **Landing/raw zone (S3):** original CSV is retained unchanged for replay and audit.
2. **ETL (AWS Glue / PySpark):** schema check; trim keys; parse dates and numeric columns; validate business rules; reject invalid records; deduplicate by `order_id`; calculate gross/net sales.
3. **Curated zone (S3):** Parquet data partitioned by `order_year` and `order_month` to improve Athena query efficiency.
4. **Quality zone (S3):** rejected records and a per-run summary for inspection.
5. **Catalog and query (Glue Data Catalog + Athena):** table metadata allows SQL querying without provisioning a database server.

## Data quality rules

- `order_id` and `customer_id` are required.
- `order_date` must parse as ISO `yyyy-MM-dd`.
- `quantity` must be a positive integer.
- `unit_price` must be non-negative.
- `region` and `order_status` must be from allowed values.
- One row per `order_id`; subsequent duplicates are rejected.

## Business logic

- `gross_sales = quantity × unit_price`.
- `net_sales = gross_sales` for `COMPLETED` orders, otherwise zero.
- This definition is intentionally simple. Real commerce data may require refunds, discounts, tax, shipping, currency, and order-line keys.

## Why these formats/services?

- S3 separates storage from compute and keeps the original source.
- Glue provides managed Spark ETL and Data Catalog integration.
- Parquet is columnar and generally more efficient for analytical queries than CSV.
- Year/month partitions support time-filtered queries, but partitions should be chosen based on data volume and query patterns.

## Known constraints

- The sample job uses `mode("overwrite")`; each run replaces the curated output and quality output at the configured prefixes. This is acceptable for a small full-refresh demo but not a safe incremental production design.
- `order_id` is treated as unique because the sample has one product per order. A production order-line dataset should use `order_line_id` or a composite key.
- The job's catalog table creation uses Spark SQL and assumes a compatible Glue catalog configuration. If catalog creation is blocked by account permissions or runtime configuration, create the external table using `sql/athena_ddl.sql` instead.
