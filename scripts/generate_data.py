"""
ClinicalTrialPipe: Data Generation Orchestrator.

Runs all domain generators in dependency order and outputs
SDTM-aligned CSVs to data/raw/.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generators'))
from config import COLUMN_ORDER, OUTPUT
from demographics import DemographicsGenerator
from visits import VisitGenerator
from adverse_events import AdverseEventsGenerator
from lab_results import LabGenerator
from trial_summary import TrialSummaryGenerator
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# scripts/generate_data.py → scripts/ → clinical-trial-pipeline/
os.makedirs(os.path.join(PROJECT_ROOT, OUTPUT["raw_dir"]), exist_ok=True)

dm_gen = DemographicsGenerator()
dm_records = dm_gen.generate()

enrolled_subjects = [s for s in dm_records if s["RFSTDTC"] is not None]

sv_gen = VisitGenerator(enrolled_subjects)
sv_records = sv_gen.generate()
ae_gen = AdverseEventsGenerator(enrolled_subjects)
ae_records = ae_gen.generate()
lb_gen = LabGenerator(enrolled_subjects, sv_records)
lb_records = lb_gen.generate()
ts_gen = TrialSummaryGenerator()
ts_records = ts_gen.generate()

domains = {
    "DM": dm_records,
    "AE": ae_records,
    "LB": lb_records,
    "SV": sv_records,
    "TS": ts_records,
}

for domain_name, records in domains.items():
    df = pd.DataFrame(records)
    df = df.drop(columns=[c for c in df.columns if c.startswith("_")], errors="ignore")
    for col in COLUMN_ORDER[domain_name]:
        if col not in df.columns:
            df[col] = None
    df = df[COLUMN_ORDER[domain_name]]
    filepath = os.path.join(PROJECT_ROOT, OUTPUT["raw_dir"], OUTPUT["filenames"][domain_name])
    df.to_csv(filepath, index=False, encoding="utf-8")

print(f"Generated {len(dm_records)} DM records ({len(enrolled_subjects)} enrolled)")
print(f"Generated {len(sv_records)} SV records")
print(f"Generated {len(ae_records)} AE records")
print(f"Generated {len(lb_records)} LB records")
print(f"Generated {len(ts_records)} TS records")
print(f"Files saved to {os.path.join(PROJECT_ROOT, OUTPUT['raw_dir'])}")