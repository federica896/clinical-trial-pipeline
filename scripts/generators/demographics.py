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
        record = {}
        selected = self.rng.choices(TREATMENT_ARMS, weights=RANDOMIZATION_RATIO, k=1)[0]
        record["ARMCD"] = selected["armcd"]
        record["ARM"] = selected["arm"]
        return record 


    def generate(self):
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

                rfstdtc = STUDY["start_date"] + timedelta(days=self.rng.randint(0, 180))
                if self.rng.random() < self.screen_failure_rate:
                    # screen failure assignment 
                    record["DSDECOD"] = self.weighted_choice(SCREEN_FAILURE_REASONS)
                    record["ARMCD"] = None
                    record["ARM"] = None
                    record["RFSTDTC"] = None
                    record["RFENDTC"] = None
                else:
                    # enrolled assignements
                    if self.rng.random() < self.discontinuation_rate:
                        # discontinued assignment 
                        record.update(self._assign_arms())
                        record["DSDECOD"] = self.weighted_choice(DISCONTINUATION_REASONS)
                        record["RFSTDTC"] = rfstdtc
                        record["RFENDTC"] = rfstdtc + timedelta(days=self.rng.randint(1,168))
                    else:
                        # completed
                        record.update(self._assign_arms())
                        record["DSDECOD"] = "COMPLETED"
                        record["RFSTDTC"] = rfstdtc
                        record["RFENDTC"] = rfstdtc + timedelta(days=168)
                
                all_records.append(record)

        return all_records 
        