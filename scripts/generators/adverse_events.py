from datetime import datetime, date, timedelta
import os
import sys 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import AE_TERMS, AE_CORRELATION, AE_CAUSALITY, MAX_AES_PER_SUBJECT, \
TREATMENT_ARMS
from base import BaseGenerator

class AdverseEventsGenerator(BaseGenerator):
    def __init__(self, enrolled_subjects):
        super().__init__("AE")
        self.subjects = enrolled_subjects
    
    def generate(self):
        """Generate AE records for all enrolled subjects.

        Each AE term is evaluated independently per subject, probability
        is base_prob x arm ae_multiplier. Severity drives downstream
        attributes (seriousness, action, outcome) via AE_CORRELATION.
        """
        all_records = []
        for subject in self.subjects:
            ae_count = 0
            ae_multiplier = [arm["ae_multiplier"] for arm in TREATMENT_ARMS if arm["armcd"] == subject["ARMCD"]][0]
            
            for ae in AE_TERMS:
                if ae_count >= MAX_AES_PER_SUBJECT:
                    break

                prob = ae["base_prob"] * ae_multiplier
                if self.rng.random() < prob:
                    # subject gets the AE
                    ae_count += 1
                    record = {}
                    record = self.add_domain_columns(record)
                    record["USUBJID"] = subject["USUBJID"]  
                    record["AESEQ"] = ae_count 
                    record["AETERM"] = ae["term"]
                    record["AEDECOD"] = ae["term"] # simulating verbatim-to-coded mapping out of scope for now
                    
                    # severity -> seriousness - action - outcome 
                    severity_labels = ["MILD", "MODERATE", "SEVERE"]
                    severity = self.rng.choices(severity_labels, weights=ae["severity"], k=1)[0]
                    record["AESEV"] = severity
                    corr = AE_CORRELATION[severity]
                    record["AESER"] = "Y" if self.rng.random() < corr["serious_prob"] else "N"
                    record["AEACN"] = self.weighted_choice(corr["action_weights"])
                    record["AEOUT"] = self.weighted_choice(corr["outcome_weights"])

                    # Causality: higher attribution in active arms
                    active_yn = "active" if subject["ARMCD"] in ("CMPX", "CMPY") else "placebo"
                    record["AEREL"] = self.weighted_choice(AE_CAUSALITY[active_yn])

                    # AE onset: random day during treatment period
                    treatment_days = (subject["_rfendtc_dt"] - subject["_rfstdtc_dt"]).days
                    ae_date = (subject["_rfstdtc_dt"] + timedelta(days=self.rng.randint(0, treatment_days))).date()
                    aestdtc = self.random_clinic_time(ae_date, lab=False)
                    record["AESTDTC"] = self.format_datetime(aestdtc)
                    record["AESTDY"] = self.calc_study_day(aestdtc, subject["_rfstdtc_dt"])

                    # AE resolves within 1-30 days after onset, capped at RFENDTC + 30. No end date for not resolved AEs
                    if record["AEOUT"] == "NOT RECOVERED/NOT RESOLVED":
                        record["AEENDTC"] = None
                        record["AEENDY"] = None
                    else:
                        aeend_date = min(ae_date + timedelta(days=self.rng.randint(1, 30)), (subject["_rfendtc_dt"] + timedelta(days=30)).date())
                        aeendtc = self.random_clinic_time(aeend_date, lab=False)
                        record["AEENDTC"] = self.format_datetime(aeendtc)
                        record["AEENDY"] = self.calc_study_day(aeendtc, subject["_rfstdtc_dt"])

                    all_records.append(record)       

        return all_records

                    

