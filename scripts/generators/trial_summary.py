"""
TS (Trial Summary) domain generator.

Generates one record per trial summary parameter from config.
No subject-level data just trial-level metadata.
"""

import os 
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import TRIAL_SUMMARY_PARAMS
from base import BaseGenerator

class TrialSummaryGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("TS")
    
    def generate(self):
        all_records = []
        for ts_count, rec in enumerate(TRIAL_SUMMARY_PARAMS, start=1):
            record = {}
            record = self.add_domain_columns(record)
            record["TSSEQ"] = ts_count
            record["TSPARMCD"] = rec["tsparmcd"]
            record["TSPARM"] = rec['tsparm']
            record["TSVAL"] = rec["tsval"]
            all_records.append(record)
        return all_records

