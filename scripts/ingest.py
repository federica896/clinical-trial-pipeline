import os
import sys 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generators'))
from config import OUTPUT
from schemas import DmSchema, AeSchema, LbSchema, SvSchema, TsSchema
import pandas as pd
import pandera as pa
import duckdb

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

domains = {
    "DM": DmSchema,
    "AE": AeSchema,
    "LB": LbSchema,
    "SV": SvSchema,
    "TS": TsSchema,
}

con = duckdb.connect(os.path.join(PROJECT_ROOT, "data", "clinical_trial.duckdb"))
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

for domain_name, DomainSchema in domains.items():
    path = os.path.join(PROJECT_ROOT, OUTPUT["raw_dir"], OUTPUT["filenames"][domain_name])
    df = pd.read_csv(path)
    try:
        validated = DomainSchema.validate(df, lazy=True)
        con.execute(f"CREATE OR REPLACE TABLE raw.{domain_name.lower()} AS SELECT * FROM validated")
        print(f"{domain_name}: validated and loaded ({len(validated)} rows)")
    except pa.errors.SchemaErrors as err:
        report_path = os.path.join(PROJECT_ROOT, "data", "quality_reports", f"{domain_name.lower()}_errors.csv")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        err.failure_cases.to_csv(report_path, index=False)
        print(f"{domain_name}: Validation Failed: see {report_path}")

con.close()

