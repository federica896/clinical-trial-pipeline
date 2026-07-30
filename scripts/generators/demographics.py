"""
DM (Demographics) domain generator.

Generates one record per screened subject (1200 total) with site assignment,
randomisation, screen failure/discontinuation simulation, and demographic
attributes. All other generators depend on the output of this domain.
"""

from datetime import datetime, timedelta, date 
from dateutil.relativedelta import relativedelta
import random 
import os
import sys 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import STUDY, ENROLLMENT, SITES, SITE_ENROLLMENT_WEIGHTS, TREATMENT_ARMS, \
    RANDOMIZATION_RATIO, DEMOGRAPHICS, SCREEN_FAILURE_REASONS, DISCONTINUATION, \
    DISCONTINUATION_REASONS, COLUMN_ORDER
from base import BaseGenerator

class DemographicsGenerator(BaseGenerator):
    def __init__(self):
        super().__init__("DM")
        self.num_screened = ENROLLMENT["num_screened"]
        self.screen_failure_rate = ENROLLMENT["screen_failure_rate"]
        self.discontinuation_rate = DISCONTINUATION["rate"]
        self.sites = [site["site_id"] for site in SITES]
    
    def _assign_sites(self):
        """ Distributes subjects across sites """
        total = sum(SITE_ENROLLMENT_WEIGHTS.values())
        normalised = {k: v / total for k, v in SITE_ENROLLMENT_WEIGHTS.items()}
        counts = {site_id: int(proportion * self.num_screened) for site_id, proportion in normalised.items()}
        remainder = self.num_screened - sum(counts.values())

        for _ in range(remainder):
            random_site = self.rng.choice(self.sites)
            counts[random_site] +=1

        return counts 

    def _generate_subjids(self, count):
        """ SUBJID generator method 4-digit per site """
        subjids = [str(n).zfill(4) for n in self.rng.sample(range(0, 10000), k=count)]
        return subjids


    def _generate_demographics(self):
        """ Generate personal attributes: SEX, RACE, ETHNIC, BRTHDTC, AGE, AGEU """
        record = {}
        record["SEX"] = self.weighted_choice(DEMOGRAPHICS["sex_distribution"])
        record["RACE"] = self.weighted_choice(DEMOGRAPHICS["race_distribution"])
        record["ETHNIC"] = self.weighted_choice(DEMOGRAPHICS["ethnicity_distribution"])
        record["AGE"] = int(max(DEMOGRAPHICS["age_range"][0], 
          min(self.rng.gauss(DEMOGRAPHICS["age_mean"], DEMOGRAPHICS["age_sd"]), 
              DEMOGRAPHICS["age_range"][1])))
        record["AGEU"] = 'YEARS'
        birth = STUDY["start_date"] - relativedelta(years=record["AGE"])
        record["BRTHDTC"] = self.format_date(birth)
        return record 
        

    def _assign_arms(self):
        """Randomize subject to treatment arm (2:2:1 ratio)"""
        record = {}
        selected = self.rng.choices(TREATMENT_ARMS, weights=RANDOMIZATION_RATIO, k=1)[0]
        record["ARMCD"] = selected["armcd"]
        record["ARM"] = selected["arm"]
        return record 


    def generate(self):
        """Generate DM records for all screened subjects.

        Per subject:
          1. Assign demographics (age, sex, race, ethnicity)
          2. Screen failure? (25%) → no arm, no treatment dates
          3. Enrolled → randomise to arm
          4. Discontinued? (15%) → early RFENDTC
          5. Completed → RFENDTC at Week 24
        """
        all_records = []
        counts = self._assign_sites()
        country_lookup = {site["site_id"]: site["country"] for site in SITES}

        for site_id, num_subjects in counts.items():
            subjids = self._generate_subjids(num_subjects)
            country = country_lookup[site_id]
            
            for subjid in subjids:
                record = {}
                record.update(self._generate_demographics())
                record = self.add_domain_columns(record)
                record["SUBJID"] = subjid
                record["USUBJID"] = self.make_usubjid(site_id, subjid)
                record["SITEID"] = site_id
                record["COUNTRY"] = country

                rfstdtc_date = STUDY["start_date"] + timedelta(days=self.rng.randint(0, 180))
                rfstdtc = self.random_clinic_time(rfstdtc_date, lab=False)
                if self.rng.random() < self.screen_failure_rate:
                    # screen failure assignment 
                    record["DSDECOD"] = self.weighted_choice(SCREEN_FAILURE_REASONS)
                    record["ARMCD"] = None
                    record["ARM"] = None
                    record["RFSTDTC"] = None
                    record["RFENDTC"] = None
                    record["DMDTC"] = self.format_datetime(self.random_clinic_time(
                    STUDY["start_date"] + timedelta(days=self.rng.randint(0, 180)), lab=False))
                    record["DMDY"] = None
                    record["DSSTDTC"] = self.format_date(STUDY["start_date"] + timedelta(days=self.rng.randint(0, 180)))
                else:
                    # enrolled assignements
                    record.update(self._assign_arms())
                    if self.rng.random() < self.discontinuation_rate:
                        # discontinued assignment 
                        record["DSDECOD"] = self.weighted_choice(DISCONTINUATION_REASONS)
                        record["RFSTDTC"] = self.format_datetime(rfstdtc)
                        record["_rfstdtc_dt"] = rfstdtc
                        rfendtc = self.random_clinic_time(rfstdtc_date + timedelta(days=self.rng.randint(1, 168)), lab=False)
                        record["RFENDTC"] = self.format_datetime(rfendtc)
                        record["_rfendtc_dt"] = rfendtc
                    else:
                        # completed
                        record["DSDECOD"] = "COMPLETED"
                        record["RFSTDTC"] = self.format_datetime(rfstdtc)
                        record["_rfstdtc_dt"] = rfstdtc
                        rfendtc = self.random_clinic_time(rfstdtc_date + timedelta(days=168), lab=False)
                        record["RFENDTC"] = self.format_datetime(rfendtc)
                        record["_rfendtc_dt"] = rfendtc
                    record["DMDTC"] = self.format_datetime(self.random_clinic_time(rfstdtc.date() if isinstance(rfstdtc, datetime) else rfstdtc, lab=False))
                    record["DMDY"] = 1  # collected on Day 1
                    record["DSSTDTC"] = self.format_date(rfendtc)
                
                all_records.append(record)

        return all_records 
        