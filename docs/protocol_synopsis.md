# Protocol Synopsis

**Protocol Number:** ONCO-2024-001
**Version:** 1.0
**Date:** 15 January 2024

*This is a fictional protocol created for the ClinicalTrialPipe portfolio project. It follows the structure outlined in ICH E6(R3) Appendix B and is designed to provide clinically plausible parameters that drive the synthetic data generation pipeline. No real investigational product, sponsor, or patients are referenced.*

---

## 1. General Information

| Field | Detail |
|-------|--------|
| Protocol Number | ONCO-2024-001 |
| Protocol Title | A Randomized, Double-Blind, Placebo-Controlled Phase III Study to Evaluate the Safety and Efficacy of Compound X (200 mg BID) and Compound Y (150 mg QD) Versus Placebo in Subjects with Locally Advanced or Metastatic Solid Tumors Who Have Progressed After Prior Systemic Therapy |
| Short Title | MERIDIAN-3 |
| Sponsor | [Fictional Sponsor] |
| Regulatory Status | IND 123456 (FDA), CTA 2024-000001-01 (EMA) |
| IND/CTA Holder | [Fictional Sponsor] |
| Phase | III |
| Indication | Locally advanced or metastatic solid tumors |
| ClinicalTrials.gov ID | NCT06000001 (fictional) |
| EudraCT Number | 2024-000001-01 (fictional) |

---

## 2. Background Information

Advanced solid tumors that have progressed after prior systemic therapy represent a significant unmet medical need. Compound X is an oral kinase inhibitor that demonstrated promising antitumor activity and a manageable safety profile in Phase I/II studies (ONCO-2022-001, ONCO-2023-002). Compound Y is an oral immune checkpoint modulator with a complementary mechanism of action. This Phase III study evaluates both compounds individually versus placebo, with a primary focus on overall survival and a comprehensive safety assessment.

The known safety profile from earlier studies includes the following commonly reported adverse events: fatigue (25%), nausea (20%), headache (15%), neutropenia (10%), diarrhea (12%), rash (5%), elevated ALT (7%), and thrombocytopenia (5%). The safety monitoring plan is designed around these known risks.

---

## 3. Trial Objectives and Purpose

### 3.1 Primary Objective

To compare the overall survival (OS) of subjects receiving Compound X or Compound Y versus placebo in subjects with locally advanced or metastatic solid tumors who have progressed after prior systemic therapy.

### 3.2 Secondary Objectives

- To evaluate the safety and tolerability of Compound X and Compound Y versus placebo
- To compare progression-free survival (PFS) across treatment arms
- To assess overall response rate (ORR) per RECIST v1.1

### 3.3 Exploratory Objectives

- To evaluate pharmacokinetic parameters of Compound X and Compound Y
- To identify potential predictive biomarkers of response

---

## 4. Trial Design

### 4.1 Overall Design

This is a multicenter, randomized, double-blind, placebo-controlled, three-arm, parallel-group Phase III study.

### 4.2 Study Schema

```
                        Screening       Randomization
                        (Day -28        (Day 1)
                         to -1)            │
                           │               │
                           ▼               ▼
                      ┌─────────┐    ┌───────────┐
                      │Informed │    │ 2:2:1     │
                      │ Consent │───→│Randomize  │
                      │Screening│    │Stratified │
                      │ Assess  │    │by ECOG,   │
                      └─────────┘    │prior lines│
                                     └─────┬─────┘
                                           │
                          ┌────────────────┼────────────────┐
                          ▼                ▼                ▼
                    ┌──────────┐    ┌──────────┐    ┌──────────┐
                    │ Arm A    │    │ Arm B    │    │ Arm C    │
                    │Compound X│    │Compound Y│    │ Placebo  │
                    │ 200mg BID│    │ 150mg QD │    │          │
                    └────┬─────┘    └────┬─────┘    └────┬─────┘
                         │               │               │
                         ▼               ▼               ▼
                    Treatment Period: 24 weeks (6 cycles of 28 days)
                    Visits: Baseline, Wk 4, Wk 8, Wk 12, Wk 16, Wk 20, Wk 24
                         │               │               │
                         ▼               ▼               ▼
                    End of Treatment / Safety Follow-up (30 days)
```

### 4.3 Randomization

- Ratio: 2:2:1 (Compound X : Compound Y : Placebo)
- Method: Interactive Response Technology (IRT), centralized
- Stratification factors: ECOG performance status (0 vs 1) and number of prior lines of therapy (1 vs ≥2)
- Blinding: Double-blind. Matching placebo capsules provided.

### 4.4 Treatment Arms

| Arm | Treatment | Dose | Route | Frequency | Duration |
|-----|-----------|------|-------|-----------|----------|
| A | Compound X | 200 mg | Oral | Twice daily (BID) | 24 weeks (6 × 28-day cycles) |
| B | Compound Y | 150 mg | Oral | Once daily (QD) | 24 weeks (6 × 28-day cycles) |
| C | Placebo | — | Oral | Twice daily (BID) | 24 weeks (6 × 28-day cycles) |

### 4.5 Dose Modifications

- For Grade 3 hematologic toxicity: hold treatment until recovery to Grade ≤1, resume at reduced dose (Compound X: 150 mg BID, Compound Y: 100 mg QD)
- For Grade 4 hematologic toxicity or any Grade 3 non-hematologic toxicity: hold treatment, resume at reduced dose upon recovery, or permanently discontinue at investigator discretion
- Maximum 2 dose reductions permitted. A third occurrence requires permanent discontinuation.

---

## 5. Selection of Participants

### 5.1 Planned Number of Subjects

- Screened: approximately 1,200
- Randomized: approximately 900 (accounting for ~25% screen failure rate)
- Distribution: ~360 Arm A, ~360 Arm B, ~180 Arm C

### 5.2 Study Sites

Approximately 12 sites across 5 countries:
- United States: 5 sites
- United Kingdom: 2 sites
- Germany: 2 sites
- Japan: 2 sites
- Canada: 1 site

### 5.3 Inclusion Criteria

1. Age ≥18 years at time of informed consent
2. Histologically or cytologically confirmed locally advanced or metastatic solid tumor
3. Documented progression after at least one prior line of systemic therapy
4. ECOG performance status 0 or 1
5. Measurable disease per RECIST v1.1
6. Adequate organ function as defined by:
   - Hemoglobin ≥10.0 g/dL
   - Absolute neutrophil count ≥1.5 × 10⁹/L
   - Platelet count ≥100 × 10⁹/L
   - Serum creatinine ≤1.5 × ULN or calculated CrCl ≥50 mL/min
   - ALT and AST ≤2.5 × ULN (≤5 × ULN for subjects with liver metastases)
   - Total bilirubin ≤1.5 × ULN
7. Life expectancy ≥12 weeks
8. Written informed consent obtained

### 5.4 Exclusion Criteria

1. Prior treatment with Compound X, Compound Y, or any investigational agent with same mechanism of action
2. Known active CNS metastases (stable, treated CNS metastases permitted)
3. Active autoimmune disease requiring systemic immunosuppression
4. Clinically significant cardiovascular disease within 6 months
5. Known hepatitis B, hepatitis C, or HIV infection with detectable viral load
6. Pregnant or breastfeeding
7. Major surgery within 4 weeks of first dose
8. Any condition that, in the opinion of the investigator, would compromise the subject's safety or data quality

---

## 6. Discontinuation of Trial Intervention and Participant Withdrawal

### 6.1 Discontinuation of Trial Intervention

Subjects may discontinue study treatment for the following reasons:
- Disease progression (per RECIST v1.1)
- Unacceptable toxicity despite dose modifications
- Subject withdrawal of consent
- Investigator decision (safety or compliance concerns)
- Pregnancy
- Protocol deviation that compromises data quality or subject safety
- Lost to follow-up

### 6.2 Expected Discontinuation Rate

Based on Phase II data and published discontinuation rates in oncology Phase III trials, approximately 15% of randomized subjects are expected to discontinue treatment prior to Week 24 for reasons other than disease progression. The primary drivers are anticipated to be adverse events (~40% of discontinuations), followed by withdrawal of consent (~20%), physician decision (~15%), lost to follow-up (~10%), protocol deviation (~10%), and other reasons (~5%).

---

## 7. Treatment and Interventions

### 7.1 Study Drug Supply and Administration

Study drug will be supplied as capsules in blister packs. Subjects will be instructed to take study drug at approximately the same time(s) each day, with or without food.

### 7.2 Concomitant Medications

- Permitted: Standard supportive care (antiemetics, analgesics, growth factors per institutional guidelines)
- Prohibited: Other investigational agents, strong CYP3A4 inhibitors/inducers, concurrent anticancer therapy

---

## 8. Assessment of Efficacy

### 8.1 Primary Endpoint

Overall Survival (OS), defined as time from randomization to death from any cause.

### 8.2 Secondary Endpoints

- Progression-Free Survival (PFS) per RECIST v1.1
- Overall Response Rate (ORR) per RECIST v1.1
- Duration of Response (DOR) in responders

*Note: Efficacy endpoints are defined for protocol completeness but are not modeled in the ClinicalTrialPipe analytics pipeline, which focuses on safety data.*

---

## 9. Assessment of Safety

### 9.1 Safety Parameters

Safety will be assessed by monitoring the following:
- Adverse events (AEs), graded per NCI CTCAE v5.0
- Serious adverse events (SAEs)
- Laboratory assessments (hematology and clinical chemistry)
- Vital signs
- ECOG performance status

### 9.2 Adverse Event Recording

- All AEs will be recorded from the time of first dose through 30 days after last dose
- AEs will be coded using MedDRA (version 27.0 or later)
- Severity will be graded as MILD, MODERATE, or SEVERE per NCI CTCAE v5.0
- Relationship to study drug will be assessed by the investigator as RELATED, POSSIBLY RELATED, or NOT RELATED
- Action taken with study treatment: DOSE NOT CHANGED, DOSE REDUCED, DRUG INTERRUPTED, DRUG WITHDRAWN
- Outcome: RECOVERED/RESOLVED, RECOVERING/RESOLVING, NOT RECOVERED/NOT RESOLVED, RECOVERED WITH SEQUELAE, FATAL

### 9.3 Laboratory Assessments

Laboratory samples will be collected at every scheduled visit. The safety lab panel includes:

| Test Code | Test Name | Units | Normal Range |
|-----------|-----------|-------|-------------|
| HGB | Hemoglobin | g/dL | 12.0–17.5 |
| WBC | White Blood Cell Count | 10⁹/L | 4.0–11.0 |
| PLAT | Platelet Count | 10⁹/L | 150–400 |
| CREAT | Creatinine | mg/dL | 0.6–1.2 |
| ALT | Alanine Aminotransferase | U/L | 7–56 |
| AST | Aspartate Aminotransferase | U/L | 10–40 |

Laboratory samples will be analyzed at a central laboratory. Results will be flagged as LOW, NORMAL, or HIGH relative to the normal reference range.

### 9.4 Expected Adverse Events (from Phase II data)

| Adverse Event | Expected Rate (Active Arms) | Expected Rate (Placebo) |
|---------------|-----------------------------|-------------------------|
| Fatigue | 25% | 10% |
| Nausea | 20% | 8% |
| Headache | 15% | 12% |
| Diarrhea | 12% | 5% |
| Neutropenia | 10% | 2% |
| Pyrexia | 10% | 5% |
| Decreased appetite | 8% | 4% |
| Anemia | 8% | 3% |
| Arthralgia | 6% | 4% |
| Elevated ALT | 7% | 2% |
| Rash | 5% | 2% |
| Thrombocytopenia | 5% | 1% |
| Peripheral neuropathy | 4% | 1% |

SAE rate: approximately 5% (active arms), 2% (placebo).

---

## 10. Visit Schedule (Schedule of Assessments)

### 10.1 Visit Windows

| Visit | Study Day | Target Week | Window (±days) | Assessments |
|-------|-----------|-------------|----------------|-------------|
| Screening | Day -28 to -1 | — | — | ICF, demographics, medical history, inclusion/exclusion, labs, vital signs, tumor assessment |
| Baseline (V1) | Day 1 | Week 0 | 0 | Randomization, baseline labs, vital signs, first dose |
| Visit 2 (V2) | Day 29 | Week 4 | ±3 | AE review, labs, vital signs, drug accountability |
| Visit 3 (V3) | Day 57 | Week 8 | ±3 | AE review, labs, vital signs, tumor assessment |
| Visit 4 (V4) | Day 85 | Week 12 | ±5 | AE review, labs, vital signs, drug accountability |
| Visit 5 (V5) | Day 113 | Week 16 | ±5 | AE review, labs, vital signs, tumor assessment |
| Visit 6 (V6) | Day 141 | Week 20 | ±5 | AE review, labs, vital signs, drug accountability |
| Visit 7 (V7) / EOT | Day 169 | Week 24 | ±5 | AE review, labs, vital signs, tumor assessment, end-of-treatment |
| Follow-up | Day 199 | Week 28 | ±7 | Safety follow-up (30 days post last dose), AE resolution, survival status |

### 10.2 Protocol Deviation Expectations

Based on prior experience in similar studies:
- Approximately 5% of visits are expected to fall outside the visit window
- The most common deviation is timing (visits occurring outside the ±day window)
- Major deviations (e.g., missed visits, wrong dose administered) are expected in <2% of visits

---

## 11. Statistical Considerations

### 11.1 Sample Size Justification

A sample size of approximately 900 randomized subjects (360:360:180) provides 80% power to detect a hazard ratio of 0.75 for OS (Compound X vs Placebo and Compound Y vs Placebo) at a two-sided significance level of 0.025 (Bonferroni-adjusted for two comparisons), assuming a median OS of 8 months in the placebo arm and an enrollment period of 12 months with a minimum follow-up of 12 months.

### 11.2 Analysis Populations

| Population | Definition | Primary Use |
|------------|-----------|-------------|
| Intent-to-Treat (ITT) | All randomized subjects | Efficacy analyses |
| Safety | All randomized subjects who received at least one dose of study drug | Safety analyses |
| Per-Protocol (PP) | All ITT subjects without major protocol deviations | Sensitivity analyses |
| Screen Failure | All screened subjects who were not randomized | Enrollment metrics |

### 11.3 Interim Analyses

One interim analysis for futility is planned after 50% of the expected OS events have been observed. The independent Data Monitoring Committee (DMC) will review unblinded data and may recommend early stopping for futility using the Lan-DeMets spending function (O'Brien-Fleming boundary).

---

## 12. Data Handling and Record Keeping

### 12.1 Electronic Data Capture

All clinical data will be collected using a validated EDC system. Data will be entered by authorized site personnel per CDASH-aligned eCRF specifications.

### 12.2 Data Standards

- Data collection: CDASH v2.2
- Tabulation datasets: CDISC SDTM v1.7 / SDTMIG v3.3
- Analysis datasets: CDISC ADaM v2.1 / ADaMIG v1.1
- Metadata: Define-XML v2.1
- Medical coding: MedDRA v27.0 (adverse events), WHODrug (concomitant medications)
- Controlled terminology: CDISC CT (current published version at time of database lock)

### 12.3 Data Quality

Data quality will be ensured through:
- Programmatic edit checks in the EDC system
- Central statistical monitoring for data anomalies
- Medical review of all SAEs and AEs leading to treatment discontinuation
- 100% source data verification for key safety endpoints at high-enrolling sites

---

## 13. Safety Reporting

- SAEs must be reported to the sponsor within 24 hours of awareness
- SUSARs (Suspected Unexpected Serious Adverse Reactions) will be reported to regulatory authorities per ICH E6(R3) and applicable local requirements
- An independent DMC will review safety data at regular intervals (approximately every 6 months)

---

## 14. Regulatory and Ethical Compliance

This study will be conducted in compliance with:
- ICH E6(R3) Good Clinical Practice
- Declaration of Helsinki (2013 revision)
- Applicable local regulatory requirements in each participating country
- 21 CFR Parts 11, 50, 56, and 312 (for US sites)
- EU Clinical Trials Regulation (EU) No 536/2014 (for EU sites)
- PMDA requirements (for Japan sites)

---

## 15. Mapping to Data Generator Configuration

The following table maps protocol parameters to the `config.py` parameters used in synthetic data generation:

| Protocol Parameter | Config Parameter | Value | Source |
|--------------------|-----------------|-------|--------|
| Protocol ID | `PROTOCOL_ID` | "ONCO-2024-001" | Section 1 |
| Phase | `PHASE` | "Phase III" | Section 1 |
| Number of sites | `NUM_SITES` | 12 | Section 5.2 |
| Countries | `COUNTRIES` | US(5), UK(2), DE(2), JP(2), CA(1) | Section 5.2 |
| Screened subjects | `NUM_SCREENED` | 1200 | Section 5.1 |
| Screen failure rate | `SCREEN_FAIL_RATE` | 0.25 | Section 5.1; evidence in data_assumptions.md §1 |
| Screen failure reasons | `SCREEN_FAIL_REASONS` | See distribution | Section 5.1; evidence in data_assumptions.md §2 |
| Discontinuation rate | `DISCONTINUATION_RATE` | 0.15 | Section 6.2; evidence in data_assumptions.md §3 |
| Discontinuation reasons | `DISCONTINUATION_REASONS` | See distribution | Section 6.2; evidence in data_assumptions.md §4 |
| Treatment arms | `TREATMENT_ARMS` | CMPX, CMPY, PBO | Section 4.4 |
| Randomization ratio | `ARM_WEIGHTS` | 2:2:1 | Section 4.3 |
| Study start | `STUDY_START` | 2024-01-15 | Section 1 |
| Treatment duration | `TREATMENT_WEEKS` | 24 | Section 4.4 |
| Visit schedule | `VISIT_SCHEDULE` | Screening, BL, Wk4-24, FU | Section 10.1 |
| Visit windows | `VISIT_WINDOWS` | ±3 to ±7 days | Section 10.1 |
| Protocol deviation rate | `DEVIATION_RATE` | 0.05 | Section 10.2; evidence in data_assumptions.md §8 |
| Lab panel | `LAB_TESTS` | HGB, WBC, PLAT, CREAT, ALT, AST | Section 9.3 |
| Lab normal ranges | `LAB_TESTS[*].low/high` | Per Section 9.3 table | Section 9.3; evidence in data_assumptions.md §7 |
| Missing lab rate | `MISSING_LAB_RATE` | 0.08 | Operational norm; evidence in data_assumptions.md §7 |
| AE terms and rates | `AE_TERMS` | Per Section 9.4 table | Section 9.4; evidence in data_assumptions.md §5 |
| AE rate by arm | `AE_PROB` | Active: 35-40%, Placebo: 20% | Section 9.4; evidence in data_assumptions.md §5 |
| SAE rate | `SAE_RATE` | Active: 5%, Placebo: 2% | Section 9.4 |
| Minimum age | `MIN_AGE` | 18 | Section 5.3 (IC #1) |
| Demographics | `DEMOGRAPHICS` | See distribution | evidence in data_assumptions.md §10 |
| MedDRA version | — | v27.0 | Section 12.2 |
| SDTM version | — | v1.7 / SDTMIG v3.3 | Section 12.2 |