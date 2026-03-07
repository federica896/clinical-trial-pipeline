"""
Base generator class — shared utilities for all SDTM domain generators.

Provides:
- STUDYID/DOMAIN injection
- USUBJID construction
- ISO 8601 datetime formatting
- Study day calculation (date - RFSTDTC)
- Random time generation within clinic hours
- Weighted random choice helper
"""

from datetime import datetime, timedelta, date 
import random 
import os
import sys 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import STUDY, RANDOM_SEED, CLINIC_HOURS

class BaseGenerator:
    def __init__(self, domain: str):
        self.domain = domain
        self.study_id = STUDY["study_id"]
        self.rng = random.Random(RANDOM_SEED)

    def make_usubjid(self, site_id: str, subjid: str):
        """ Return usubjid with format STUDYID-SITEID-SUBJID """
        return f"{self.study_id}-{site_id}-{subjid}"
    
    def format_datetime(self, dt: datetime):
        """" Return a full precision date """
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    def format_date(self, dt: date):
        """ Return date-only """
        return dt.strftime("%Y-%m-%d")
    
    def calc_study_day(self, event_date, ref_start_date):
        """ Study day calculation """
        delta = (event_date.date() if isinstance(event_date, datetime) else event_date) - (ref_start_date.date() if isinstance(ref_start_date, datetime) else ref_start_date)
        days = delta.days
        if days >= 0:
            return days + 1  # No Day 0: Day 1 = RFSTDTC
        return days          # Negative days stay as-is
    
    def weighted_choice(self, options: dict):
        """ Pick a random key from a dict of {value: probability}.
            options: dict mapping choice strings to their probabilities (must sum to ~1.0) """
        items = list(options.keys())
        weights = list(options.values())
        return self.rng.choices(items, weights=weights, k=1)[0]
    
    def add_domain_columns(self, record: dict):
        """ Inject studyid and domain into a record """
        record["STUDYID"] = self.study_id
        record["DOMAIN"] = self.domain
        return record 
    
    def random_clinic_time(self, base_date: date, lab: bool):
        """ Generate a random datetime for labs """
        if lab:
            if self.rng.random() < 0.70:
                hour = self.rng.randint(CLINIC_HOURS["open"], CLINIC_HOURS["lab_peak"])
            else: 
                hour = self.rng.randint(10,12)
        else:
            hour = self.rng.randint(CLINIC_HOURS["open"], CLINIC_HOURS["close"]-1)

        minute = self.rng.randint(0, 59) 
        second = self.rng.randint(0, 59)    
        return datetime(base_date.year, base_date.month, base_date.day, hour, minute, second)    