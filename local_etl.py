"""Local, testable version of the retail orders ETL pipeline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "order_id", "order_date", "customer_id", "product_id", "product_name",
    "category", "quantity", "unit_price", "region", "sales_channel", "order_status",
]
VALID_STATUSES = {"COMPLETED", "CANCELLED", "RETURNED"}
VALID_REGIONS = {"North", "South", "East", "West"}

def transform_orders(input_path: str | Path):
    """Return (curated_df, rejected_df, quality_report)."""
    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)
    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Input is missing required columns: {missing_columns}")
    df = df[REQUIRED_COLUMNS].copy()
    df["_source_row"] = range(2, len(df) + 2)

    for col in ["quantity", "unit_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce").dt.date

    reason = pd.Series("", index=df.index, dtype="object")
    checks = [
        (df["order_id"].astype(str).str.strip().eq(""), "missing_order_id"),
        (df["order_date"].isna(), "invalid_order_date"),
        (df["customer_id"].astype(str).str.strip().eq(""), "missing_customer_id"),
        (df["quantity"].isna() | (df["quantity"] <= 0), "invalid_quantity"),
        (df["unit_price"].isna() | (df["unit_price"] < 0), "invalid_unit_price"),
        (~df["region"].isin(VALID_REGIONS), "invalid_region"),
        (~df["order_status"].isin(VALID_STATUSES), "invalid_order_status"),
    ]
    invalid = pd.Series(False, index=df.index)
    for mask, label in checks:
        reason.loc[mask & reason.eq("")] = label
        invalid |= mask

    # A repeated order_id is rejected after the first occurrence.
    duplicate = df["order_id"].astype(str).str.strip().ne("") & df["order_id"].duplicated(keep="first")
    reason.loc[duplicate & reason.eq("")] = "duplicate_order_id"
    invalid |= duplicate

    rejected = df.loc[invalid].copy()
    rejected["rejection_reason"] = reason.loc[invalid]
    valid = df.loc[~invalid].copy()

    valid["quantity"] = valid["quantity"].astype(int)
    valid["unit_price"] = valid["unit_price"].astype(float).round(2)
    valid["gross_sales"] = (valid["quantity"] * valid["unit_price"]).round(2)
    valid["net_sales"] = valid["gross_sales"].where(valid["order_status"].eq("COMPLETED"), 0.0).round(2)
    valid["order_year"] = pd.to_datetime(valid["order_date"]).dt.year.astype(int)
    valid["order_month"] = pd.to_datetime(valid["order_date"]).dt.month.astype(int)
    valid["order_date"] = valid["order_date"].astype(str)
    valid = valid.drop(columns=["_source_row"])
    rejected["order_date"] = rejected["order_date"].astype(str)
    rejected = rejected.drop(columns=["_source_row"])

    report = {
        "input_rows": int(len(df)),
        "curated_rows": int(len(valid)),
        "rejected_rows": int(len(rejected)),
        "duplicate_order_ids_rejected": int(duplicate.sum()),
        "net_sales_completed_orders": round(float(valid["net_sales"].sum()), 2),
        "status": "PASS" if len(valid) > 0 else "FAIL",
    }
    return valid, rejected, report

def run(input_path: str | Path, output_dir: str | Path):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    curated, rejected, report = transform_orders(input_path)
    curated.to_csv(output / "curated_orders.csv", index=False)
    rejected.to_csv(output / "rejected_orders.csv", index=False)
    (output / "quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="data/raw/orders.csv")
    parser.add_argument("--output-dir", default="data/processed")
    args = parser.parse_args()
    run(args.input, args.output_dir)

if __name__ == "__main__":
    main()
