import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from local_etl import transform_orders

class TestLocalETL(unittest.TestCase):
    def test_quality_rules_and_revenue(self):
        curated, rejected, report = transform_orders(ROOT / "data" / "raw" / "orders.csv")
        self.assertGreater(len(curated), 0)
        self.assertGreater(len(rejected), 0)
        self.assertEqual(curated["order_id"].nunique(), len(curated))
        self.assertTrue((curated["quantity"] > 0).all())
        self.assertTrue((curated["unit_price"] >= 0).all())
        self.assertTrue((curated.loc[curated["order_status"] != "COMPLETED", "net_sales"] == 0).all())
        self.assertEqual(report["input_rows"], report["curated_rows"] + report["rejected_rows"])

    def test_missing_column_fails(self):
        import pandas as pd
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            pd.DataFrame([{"order_id": "x"}]).to_csv(path, index=False)
            with self.assertRaises(ValueError):
                transform_orders(path)

if __name__ == "__main__":
    unittest.main()
