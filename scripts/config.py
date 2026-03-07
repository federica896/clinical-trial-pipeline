"""
ClinicalTrialPipe — Trial Configuration

Every parameter in this file traces to the protocol synopsis (docs/protocol_synopsis.md)
and evidence base (docs/data_assumptions.md). Cross-references are noted inline.

To adapt this pipeline for a different trial, modify this file only.
The generator classes read from these dictionaries and require no code changes.
"""

from datetime import date

# =============================================================================
# 1. STUDY METADATA
# Protocol Synopsis §1 (General Information)
# =============================================================================

STUDY = {
    "study_id": "ONCO-2024-001",
    "short_title": "MERIDIAN-3",
    "phase": "PHASE III TRIAL",
    "indication": "Locally advanced or metastatic solid tumors",
    "sponsor": "Meridian Therapeutics, Inc.",
    "start_date": date(2024, 1, 15),
    "sdtm_version": "1.7",
    "sdtmig_version": "3.3",
    "meddra_version": "27.0",
    "ct_version": "2024-03-29",  # CDISC CT package date
}

# Reproducibility — single global seed controls all randomness
RANDOM_SEED = 42

# =============================================================================
# 2. SITES AND COUNTRIES
# Protocol Synopsis §5.2 (Study Sites)
# =============================================================================

SITES = [
    # site_id,  name,                              country (ISO 3166 alpha-3)
    {"site_id": "SITE-001", "name": "Memorial Cancer Institute",      "country": "USA"},
    {"site_id": "SITE-002", "name": "Pacific Oncology Center",        "country": "USA"},
    {"site_id": "SITE-003", "name": "Midwest Cancer Research Group",  "country": "USA"},
    {"site_id": "SITE-004", "name": "Southeast Oncology Associates",  "country": "USA"},
    {"site_id": "SITE-005", "name": "Northeast Medical Center",       "country": "USA"},
    {"site_id": "SITE-006", "name": "Royal Marsden Cancer Centre",    "country": "GBR"},
    {"site_id": "SITE-007", "name": "Manchester Oncology Unit",       "country": "GBR"},
    {"site_id": "SITE-008", "name": "Charité Comprehensive Cancer",   "country": "DEU"},
    {"site_id": "SITE-009", "name": "Munich Oncology Clinic",         "country": "DEU"},
    {"site_id": "SITE-010", "name": "National Cancer Center Tokyo",   "country": "JPN"},
    {"site_id": "SITE-011", "name": "Osaka University Hospital",      "country": "JPN"},
    {"site_id": "SITE-012", "name": "Toronto Cancer Research Centre", "country": "CAN"},
]

# Site-level enrollment weights — larger sites enroll more subjects
# Reflects real pattern where a few sites contribute disproportionately
# data_assumptions.md §9
SITE_ENROLLMENT_WEIGHTS = {
    "SITE-001": 1.4,   # High-enrolling US site
    "SITE-002": 1.2,
    "SITE-003": 1.0,
    "SITE-004": 0.8,
    "SITE-005": 0.9,
    "SITE-006": 1.1,
    "SITE-007": 0.8,
    "SITE-008": 1.0,
    "SITE-009": 0.9,
    "SITE-010": 1.1,
    "SITE-011": 0.9,
    "SITE-012": 0.7,   # Smallest site
}

# =============================================================================
# 3. SUBJECT ENROLLMENT
# Protocol Synopsis §5.1; data_assumptions.md §1, §2
# =============================================================================

ENROLLMENT = {
    "num_screened": 1200,
    "screen_failure_rate": 0.25,  # 25% — evidence: 25-36% in oncology Phase III
}

# Screen failure reasons — data_assumptions.md §2
# Based on: French multi-center study (2020-2022), Indian Phase III analysis
SCREEN_FAILURE_REASONS = {
    "ELIGIBILITY CRITERIA NOT MET": 0.60,   # 60% — eligibility dominant cause
    "CONSENT WITHDRAWN":            0.20,   # 20% — patient refusal
    "LAB VALUES OUT OF RANGE":      0.15,   # 15% — screening labs fail
    "OTHER":                        0.05,   # 5%  — administrative/logistic
}

# =============================================================================
# 4. TREATMENT ARMS AND RANDOMIZATION
# Protocol Synopsis §4.3, §4.4
# =============================================================================

TREATMENT_ARMS = [
    {
        "armcd": "CMPX",
        "arm": "Compound X 200mg BID",
        "description": "Oral kinase inhibitor, 200 mg twice daily",
        "ae_multiplier": 1.0,     # Reference rate for active arm AE probabilities
    },
    {
        "armcd": "CMPY",
        "arm": "Compound Y 150mg QD",
        "description": "Oral immune checkpoint modulator, 150 mg once daily",
        "ae_multiplier": 0.90,    # Slightly lower AE rate than Compound X
    },
    {
        "armcd": "PBO",
        "arm": "Placebo",
        "description": "Matching placebo capsules, twice daily",
        "ae_multiplier": 0.50,    # ~50% of active arm AE rate
    },
]

# Randomization ratio: 2:2:1 (Compound X : Compound Y : Placebo)
RANDOMIZATION_RATIO = [2, 2, 1]

# =============================================================================
# 5. DISCONTINUATION
# Protocol Synopsis §6; data_assumptions.md §3, §4
# =============================================================================

DISCONTINUATION = {
    "rate": 0.15,  # 15% of enrolled — evidence: industry avg ~19%, excl. progression
}

# Discontinuation reasons — data_assumptions.md §4
# Based on: Korean CRC survey (PMC 2022), JNCCN censoring analysis (2021)
DISCONTINUATION_REASONS = {
    "ADVERSE EVENT":        0.40,   # 40% — dominant non-progression cause
    "WITHDRAWAL BY SUBJECT": 0.20,  # 20% — consent withdrawal
    "PHYSICIAN DECISION":   0.15,   # 15% — investigator decision
    "LOST TO FOLLOW-UP":    0.10,   # 10%
    "PROTOCOL VIOLATION":   0.10,   # 10%
    "OTHER":                0.05,   # 5%
}

# =============================================================================
# 6. DEMOGRAPHICS
# Protocol Synopsis §5.3 (Inclusion Criteria); data_assumptions.md §10
# =============================================================================

DEMOGRAPHICS = {
    "age_min": 18,       # Inclusion criterion #1
    "age_range": (45, 80),  # Realistic enrolled range (median ~62)
    "age_mean": 62,
    "age_sd": 9,
    "sex_distribution": {
        "M": 0.55,
        "F": 0.45,
    },
    "race_distribution": {
        "WHITE":                              0.65,
        "ASIAN":                              0.15,
        "BLACK OR AFRICAN AMERICAN":          0.10,
        "AMERICAN INDIAN OR ALASKA NATIVE":   0.02,
        "OTHER":                              0.08,
    },
    "ethnicity_distribution": {
        "NOT HISPANIC OR LATINO": 0.88,
        "HISPANIC OR LATINO":     0.12,
    },
}

# =============================================================================
# 7. VISIT SCHEDULE
# Protocol Synopsis §10.1 (Schedule of Assessments)
# =============================================================================

VISIT_SCHEDULE = [
    # visit_num, visit_name,     target_day, window_days, has_labs, is_treatment
    {"visitnum": 0,  "visit": "Screening",         "target_day": -14, "window": 14, "has_labs": True,  "is_treatment": False},
    {"visitnum": 1,  "visit": "Baseline",           "target_day": 1,   "window": 0,  "has_labs": True,  "is_treatment": True},
    {"visitnum": 2,  "visit": "Week 4",             "target_day": 29,  "window": 3,  "has_labs": True,  "is_treatment": True},
    {"visitnum": 3,  "visit": "Week 8",             "target_day": 57,  "window": 3,  "has_labs": True,  "is_treatment": True},
    {"visitnum": 4,  "visit": "Week 12",            "target_day": 85,  "window": 5,  "has_labs": True,  "is_treatment": True},
    {"visitnum": 5,  "visit": "Week 16",            "target_day": 113, "window": 5,  "has_labs": True,  "is_treatment": True},
    {"visitnum": 6,  "visit": "Week 20",            "target_day": 141, "window": 5,  "has_labs": True,  "is_treatment": True},
    {"visitnum": 7,  "visit": "Week 24 / EOT",      "target_day": 169, "window": 5,  "has_labs": True,  "is_treatment": True},
    {"visitnum": 8,  "visit": "Follow-up (Week 28)", "target_day": 199, "window": 7,  "has_labs": True,  "is_treatment": False},
]

# Protocol deviation rate for visit windows — data_assumptions.md §8
VISIT_DEVIATION_RATE = 0.05  # 5% of visits fall outside window

# =============================================================================
# 8. LABORATORY TESTS
# Protocol Synopsis §9.3; data_assumptions.md §7
# Normal ranges from standard clinical laboratory references
# =============================================================================

LAB_TESTS = [
    {
        "testcd": "HGB",
        "test": "Hemoglobin",
        "unit": "g/dL",
        "normal_low": 12.0,
        "normal_high": 17.5,
        "mean": 13.5,      # Slightly below midpoint — oncology population, mild anemia
        "sd": 1.8,
    },
    {
        "testcd": "WBC",
        "test": "White Blood Cell Count",
        "unit": "10^9/L",
        "normal_low": 4.0,
        "normal_high": 11.0,
        "mean": 7.0,
        "sd": 2.5,
    },
    {
        "testcd": "PLAT",
        "test": "Platelet Count",
        "unit": "10^9/L",
        "normal_low": 150.0,
        "normal_high": 400.0,
        "mean": 250.0,
        "sd": 60.0,
    },
    {
        "testcd": "CREAT",
        "test": "Creatinine",
        "unit": "mg/dL",
        "normal_low": 0.6,
        "normal_high": 1.2,
        "mean": 0.9,
        "sd": 0.2,
    },
    {
        "testcd": "ALT",
        "test": "Alanine Aminotransferase",
        "unit": "U/L",
        "normal_low": 7.0,
        "normal_high": 56.0,
        "mean": 25.0,
        "sd": 12.0,
    },
    {
        "testcd": "AST",
        "test": "Aspartate Aminotransferase",
        "unit": "U/L",
        "normal_low": 10.0,
        "normal_high": 40.0,
        "mean": 22.0,
        "sd": 10.0,
    },
]

# Missing lab rate — data_assumptions.md §7
MISSING_LAB_RATE = 0.08  # 8% — operational norm (5-10% typical)

# =============================================================================
# 9. ADVERSE EVENTS
# Protocol Synopsis §9.4; data_assumptions.md §5, §6
# Rates are per-subject probabilities for active arms (Compound X baseline)
# Compound Y and Placebo rates derived via ae_multiplier in TREATMENT_ARMS
# =============================================================================

AE_TERMS = [
    # term (AETERM/AEDECOD),   base_prob (active arm),  severity weights (MILD/MOD/SEVERE)
    # Severity categories from CDISC CT C66769. Weights are modeled estimates:
    #   - Hematologic AEs (neutropenia, thrombocytopenia, anemia): skew moderate/severe
    #     (detected via lab thresholds, rarely classified mild)
    #   - Subjective symptoms (headache, pyrexia, arthralgia): skew mild
    #     (patient-reported at lower thresholds)
    #   - GI events (nausea, diarrhea): distributed across all grades
    {"term": "Fatigue",                  "base_prob": 0.25, "severity": [0.50, 0.35, 0.15]},
    {"term": "Nausea",                   "base_prob": 0.20, "severity": [0.55, 0.35, 0.10]},
    {"term": "Headache",                 "base_prob": 0.15, "severity": [0.65, 0.30, 0.05]},
    {"term": "Diarrhea",                 "base_prob": 0.12, "severity": [0.45, 0.40, 0.15]},
    {"term": "Neutropenia",              "base_prob": 0.10, "severity": [0.20, 0.40, 0.40]},
    {"term": "Pyrexia",                  "base_prob": 0.10, "severity": [0.60, 0.30, 0.10]},
    {"term": "Decreased appetite",       "base_prob": 0.08, "severity": [0.60, 0.35, 0.05]},
    {"term": "Anemia",                   "base_prob": 0.08, "severity": [0.30, 0.40, 0.30]},
    {"term": "Arthralgia",               "base_prob": 0.06, "severity": [0.60, 0.30, 0.10]},
    {"term": "Alanine aminotransferase increased", "base_prob": 0.07, "severity": [0.40, 0.40, 0.20]},
    {"term": "Rash",                     "base_prob": 0.05, "severity": [0.60, 0.30, 0.10]},
    {"term": "Thrombocytopenia",         "base_prob": 0.05, "severity": [0.25, 0.35, 0.40]},
    {"term": "Peripheral neuropathy",    "base_prob": 0.04, "severity": [0.50, 0.35, 0.15]},
]

# AE severity → seriousness/outcome/action correlation model
# data_assumptions.md §6 — based on CTCAE/ICH E2A clinical logic
AE_CORRELATION = {
    "MILD": {
        "serious_prob": 0.02,
        "fatal_prob": 0.0,
        "action_weights": {
            "DOSE NOT CHANGED": 0.95,
            "DOSE REDUCED":     0.04,
            "DRUG WITHDRAWN":   0.01,
        },
        "outcome_weights": {
            "RECOVERED/RESOLVED":          0.85,
            "RECOVERING/RESOLVING":        0.10,
            "NOT RECOVERED/NOT RESOLVED":  0.05,
            "FATAL":                       0.00,
        },
    },
    "MODERATE": {
        "serious_prob": 0.15,
        "fatal_prob": 0.0,
        "action_weights": {
            "DOSE NOT CHANGED": 0.60,
            "DOSE REDUCED":     0.25,
            "DRUG WITHDRAWN":   0.15,
        },
        "outcome_weights": {
            "RECOVERED/RESOLVED":          0.65,
            "RECOVERING/RESOLVING":        0.25,
            "NOT RECOVERED/NOT RESOLVED":  0.10,
            "FATAL":                       0.00,
        },
    },
    "SEVERE": {
        "serious_prob": 0.60,
        "fatal_prob": 0.05,
        "action_weights": {
            "DOSE NOT CHANGED": 0.10,
            "DOSE REDUCED":     0.30,
            "DRUG WITHDRAWN":   0.60,
        },
        "outcome_weights": {
            "RECOVERED/RESOLVED":          0.40,
            "RECOVERING/RESOLVING":        0.25,
            "NOT RECOVERED/NOT RESOLVED":  0.30,
            "FATAL":                       0.05,
        },
    },
}

# Causality weights — higher for active arms, lower for placebo
AE_CAUSALITY = {
    "active": {
        "RELATED":           0.30,
        "POSSIBLY RELATED":  0.35,
        "NOT RELATED":       0.35,
    },
    "placebo": {
        "RELATED":           0.05,
        "POSSIBLY RELATED":  0.15,
        "NOT RELATED":       0.80,
    },
}

# Maximum AEs per subject (realistic cap)
MAX_AES_PER_SUBJECT = 5

# =============================================================================
# 10. TRIAL SUMMARY (TS DOMAIN)
# Protocol Synopsis §1, §4, §11
# =============================================================================

TRIAL_SUMMARY_PARAMS = [
    {"tsparmcd": "SSTDTC",  "tsparm": "Study Start Date",               "tsval": "2024-01-15"},
    {"tsparmcd": "SENDTC",  "tsparm": "Study End Date",                  "tsval": "2025-01-15"},
    {"tsparmcd": "TITLE",   "tsparm": "Study Title",                     "tsval": "MERIDIAN-3: A Phase III Study of Compound X and Compound Y vs Placebo in Advanced Solid Tumors"},
    {"tsparmcd": "PHASE",   "tsparm": "Trial Phase Classification",      "tsval": "PHASE III TRIAL"},
    {"tsparmcd": "INDIC",   "tsparm": "Trial Disease/Condition Indication", "tsval": "Locally advanced or metastatic solid tumors"},
    {"tsparmcd": "TRT",     "tsparm": "Investigational Therapy or Treatment", "tsval": "Compound X 200mg BID; Compound Y 150mg QD"},
    {"tsparmcd": "CTRL",    "tsparm": "Control Type",                    "tsval": "PLACEBO"},
    {"tsparmcd": "RANDOM",  "tsparm": "Trial Is Randomized",             "tsval": "Y"},
    {"tsparmcd": "STYPE",   "tsparm": "Study Type",                      "tsval": "INTERVENTIONAL"},
    {"tsparmcd": "BLIND",   "tsparm": "Trial Blinding Schema",           "tsval": "DOUBLE BLIND"},
    {"tsparmcd": "PLTEFPS", "tsparm": "Planned Number of Subjects",      "tsval": "900"},
    {"tsparmcd": "PCNTRY",  "tsparm": "Planned Country of Investigational Sites", "tsval": "USA; GBR; DEU; JPN; CAN"},
    {"tsparmcd": "REGID",   "tsparm": "Registry Identifier",             "tsval": "NCT06000001"},
    {"tsparmcd": "OBJPRIM", "tsparm": "Trial Primary Objective",         "tsval": "Compare overall survival of Compound X and Compound Y vs Placebo"},
    {"tsparmcd": "ADDON",   "tsparm": "Added on to Existing Treatments", "tsval": "N"},
    {"tsparmcd": "STOPRULE","tsparm": "Study Stop Rules",                "tsval": "Futility at 50% OS events (Lan-DeMets O'Brien-Fleming)"},
    {"tsparmcd": "ACESSION","tsparm": "Accession Number",                "tsval": "IND 123456"},
    {"tsparmcd": "SPONSOR", "tsparm": "Clinical Study Sponsor",          "tsval": "Meridian Therapeutics, Inc."},
]

# =============================================================================
# 11. CLINIC HOURS — for realistic datetime generation
# =============================================================================

CLINIC_HOURS = {
    "open": 8,    # 08:00
    "close": 17,  # 17:00
    "lab_peak": 9,  # Lab draws peak at 09:00 (fasting)
}

# =============================================================================
# 12. SDTM DOMAIN COLUMN ORDER
# Ensures CSV output matches SDTM variable ordering from data_model_design.md
# Identifiers → Topic → Qualifiers → Timing
# =============================================================================

COLUMN_ORDER = {
    "DM": [
        "STUDYID", "DOMAIN", "USUBJID", "SUBJID",
        "RFSTDTC", "RFENDTC", "SITEID", "BRTHDTC",
        "AGE", "AGEU", "SEX", "RACE", "ETHNIC",
        "ARMCD", "ARM", "COUNTRY",
        "DMDTC", "DMDY",
        # Non-standard (would be SUPPDM)
        "DSDECOD", "DSSTDTC",
    ],
    "AE": [
        "STUDYID", "DOMAIN", "USUBJID", "AESEQ",
        "AETERM", "AEDECOD",
        "AESEV", "AESER", "AEREL", "AEACN", "AEOUT",
        "AESTDTC", "AEENDTC", "AESTDY", "AEENDY",
    ],
    "LB": [
        "STUDYID", "DOMAIN", "USUBJID", "LBSEQ",
        "LBTESTCD", "LBTEST",
        "LBORRES", "LBORRESU", "LBORNRLO", "LBORNRHI",
        "LBSTRESC", "LBSTRESN", "LBSTRESU",
        "LBNRIND",
        "VISITNUM", "VISIT", "LBDTC", "LBDY",
    ],
    "SV": [
        "STUDYID", "DOMAIN", "USUBJID",
        "VISITNUM", "VISIT", "SVSTDTC", "SVENDTC",
        "SVUPDES",
    ],
    "TS": [
        "STUDYID", "DOMAIN", "TSSEQ",
        "TSPARMCD", "TSPARM", "TSVAL",
    ],
}

# =============================================================================
# 13. OUTPUT CONFIGURATION
# =============================================================================

OUTPUT = {
    "raw_dir": "data/raw",
    "filenames": {
        "DM": "dm.csv",
        "AE": "ae.csv",
        "LB": "lb.csv",
        "SV": "sv.csv",
        "TS": "ts.csv",
    },
}