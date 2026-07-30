"""
SV (Subject Visits) domain generator.

Generates one record per visit per enrolled subject, with protocol
deviation simulation and realistic clinic-hours timestamps.
"""

from datetime import datetime, timedelta, date 
import random 
import os
import sys 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import STUDY, VISIT_SCHEDULE, VISIT_DEVIATION_RATE, COLUMN_ORDER
from base import BaseGenerator

class VisitGenerator(BaseGenerator):
    def __init__(self, enrolled_subjects):
        super().__init__("SV")
        self.subjects = enrolled_subjects


    def generate(self):
        """Generate SV records for all enrolled subjects.

        For each subject, iterates through the protocol visit schedule
        until RFENDTC (discontinued subjects get fewer visits).
        ~5% of visits are shifted outside the protocol window.
        """
        all_records = []
        for subject in self.subjects:
            for visit in VISIT_SCHEDULE:
                is_deviation = False
                visdat = subject["_rfstdtc_dt"] + timedelta(days=visit["target_day"])
                if visdat > subject["_rfendtc_dt"]:
                    break
                if self.rng.random() < VISIT_DEVIATION_RATE:
                    # Deviation: outside window
                    is_deviation = True
                    deviation = self.rng.choice([-1, 1]) * (visit["window"] + self.rng.randint(1,5))
                    visit_date = visdat + timedelta(days=deviation) 
                else:
                    # Normal: within window
                    visit_date = visdat + timedelta(days=self.rng.randint(-visit["window"], visit["window"]))
                svstdtc = self.random_clinic_time(visit_date, lab=False)
                svendtc = svstdtc + timedelta(hours=self.rng.randint(1,3))

                record = {}
                record = self.add_domain_columns(record)
                record["USUBJID"] = subject["USUBJID"]  
                record["VISITNUM"] = visit["visitnum"]
                record["VISIT"] = visit["visit"]
                record["SVSTDTC"] = self.format_datetime(svstdtc)
                record["SVENDTC"] = self.format_datetime(svendtc)
                record["SVUPDES"] = "VISIT OUTSIDE WINDOW" if is_deviation else ""
                all_records.append(record)
        return all_records  

