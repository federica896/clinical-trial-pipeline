"""
LB (Laboratory Test Results) domain generator.

Generates lab results for enrolled subjects at each visit, with normal
distributions based on test-specific parameters, 8% missing rate,
and reference range flagging (LOW/NORMAL/HIGH).
"""
from datetime import date, datetime, timedelta
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import VISIT_SCHEDULE, LAB_TESTS, MISSING_LAB_RATE
from base import BaseGenerator

class LabGenerator(BaseGenerator):
    def __init__(self, enrolled_subjects, visits):
        super().__init__("LB")
        self.subjects = enrolled_subjects
        self.visits = visits 


    def generate(self):
        """Generate LB records for all enrolled subjects.

        Links to SV via USUBJID to use actual visit dates.
        Each visit x each lab test = one potential record.
        ~8% of labs are missing (skipped).
        """
        all_records = []
        lab_lookup = {v["visitnum"]: v["has_labs"] for v in VISIT_SCHEDULE}
        for subject in self.subjects:
            lb_count = 0
            subject_visits = [v for v in self.visits if v["USUBJID"] == subject["USUBJID"]]
            for visit in subject_visits:
                if not lab_lookup[visit["VISITNUM"]]:
                    continue
                for lab in LAB_TESTS:
                    if self.rng.random() < MISSING_LAB_RATE:
                        # Lab is missing: skip
                        continue

                    lb_count += 1
                    record = {}
                    record = self.add_domain_columns(record)
                    record["USUBJID"] = subject["USUBJID"] 
                    record["LBSEQ"] = lb_count
                    record["VISITNUM"] = visit["VISITNUM"]
                    record["VISIT"] = visit["VISIT"]
                    record["LBTESTCD"] = lab["testcd"]
                    record["LBTEST"] = lab["test"]
                    record["LBORRESU"] = lab["unit"]
                    record["LBORNRLO"] = lab["normal_low"]
                    record["LBORNRHI"] = lab["normal_high"]
                    record["LBSTRESU"] = lab["unit"]  
                    
                    # Generate value from normal distribution
                    lb_value = round(max(0, self.rng.gauss(lab["mean"], lab["sd"])), 1)
                    record["LBORRES"] = str(lb_value)
                    record["LBSTRESN"] = lb_value            
                    record["LBSTRESC"] = str(lb_value)

                    # Flag against ref ranges
                    if lb_value > record["LBORNRHI"]: 
                        record["LBNRIND"] = "HIGH"
                    elif lb_value < record["LBORNRLO"]:
                        record["LBNRIND"] = "LOW"
                    else:
                        record["LBNRIND"] = "NORMAL"

                    # Lab collection time morning-weighted for fasting labs
                    visit_date = datetime.strptime(visit["SVSTDTC"], "%Y-%m-%dT%H:%M:%S").date()
                    lbdtc = self.random_clinic_time(visit_date, lab=True)
                    record["LBDTC"] = self.format_datetime(lbdtc)
                    record["LBDY"] = self.calc_study_day(lbdtc, subject["_rfstdtc_dt"])
                    all_records.append(record)

        return all_records            


