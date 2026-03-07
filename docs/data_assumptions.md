# Data Generation Assumptions: Evidence Base

This document provides the evidence base for every parameter used in the ClinicalTrialPipe synthetic data generator. Each assumption is traced to published literature or documented as an operational norm. Parameters without published evidence are clearly marked.

*Last updated: March 2026*

---

## 1. Screen Failure Rate

**Parameter:** 25% of screened subjects fail to enroll

**Evidence:**

A cross-industry study of 76 global Phase II/III trials (2016–2019) across 20 pharmaceutical companies reported an overall average screen failure rate of 36.3%, up from 34.7% in 2012 (Applied Clinical Trials, "Can Recruitment and Retention Get Any Worse?"). Oncology trials specifically saw worsening rates during this period.

In genitourinary Phase III cancer trials, the mean screen failure rate was 25–26%, with a range of 12–45% depending on the trial and cancer subtype (Wong et al., J Clin Oncol 2016; 34:2_suppl, 176; Sridhar et al., Clin Genitourin Cancer 2017).

A multi-center analysis of early-phase oncology trials across three French cancer centers (2020–2022) reported screen failure rates of 21–26% (Gustave Roussy, Oncopole Toulouse, Centre Léon Bérard; published in ScienceDirect 2025).

**Rationale for 25%:** We select 25% as a mid-range estimate consistent with Phase III solid tumor trials. This is conservative relative to the 36% industry average but representative of well-designed oncology trials with established inclusion criteria.

---

## 2. Screen Failure Reasons

**Parameter distribution:**

| Reason | Proportion | CDISC Coded Value |
|--------|-----------|-------------------|
| Did not meet eligibility criteria | 60% | SCREEN FAILURE - ELIGIBILITY |
| Patient/subject refusal | 20% | SCREEN FAILURE - CONSENT WITHDRAWN |
| Laboratory values out of range | 15% | SCREEN FAILURE - LAB VALUES |
| Other | 5% | SCREEN FAILURE - OTHER |

**Evidence:**

A post hoc analysis of a Phase III oncology trial (Journals LWW, Cancer Research Statistics and Treatment, 2021) found that 61% of screened patients were not enrolled because they did not meet eligibility criteria, while 39% refused to participate.

A multi-center French analysis (2020–2022, N=202 screen failures) found the following breakdown: radiological reasons 29.2%, biological/lab abnormalities 23.8% (including vital organ dysfunction), clinical deterioration 22.3%, administrative 10.9%, and performance status deterioration 11.9%.

A study of genitourinary Phase III trials reported that 91% of screen failures in prostate cancer trials and 84% in renal cancer trials were due to ineligibility (Wong et al., 2016).

**Rationale:** Our distribution consolidates clinical/radiological/PS reasons under "eligibility criteria" (60%) since these all reflect protocol inclusion/exclusion failures. Lab values are separated (15%) as they represent a distinct operational category relevant to our lab domain. Patient refusal (20%) aligns with the 20–39% range reported across studies. "Other" (5%) covers administrative/logistic reasons.

---

## 3. Discontinuation Rate

**Parameter:** 15% of enrolled subjects discontinue treatment prior to study completion (excluding disease progression)

**Evidence:**

The same cross-industry study (2016–2019) reported an overall average dropout rate of 19.1%, up from 15.3% in 2012 (Applied Clinical Trials, 2024 update).

A JNCCN analysis of Phase III oncology trials supporting FDA approvals found that early drug discontinuation averaged 21.6% in experimental arms and 19.9% in control arms. Discontinuation specifically due to adverse effects was 13.2% in experimental arms versus 8.5% in controls (JNCCN, Vol 19, Issue 12, 2021).

An ASCO abstract analyzing Phase III oncology trial dropout across 5 cancer centers in British Columbia (1999–2013) found that dropout was mainly attributable to toxicities, with rates varying by tumor type — lung cancer had the highest dropout (82%) and breast cancer the lowest (28%) (Malhi et al., J Clin Oncol 2015; 33:15_suppl, e17731).

**Rationale for 15%:** We model 15% non-progression discontinuation. In real trials, disease progression is the largest single driver of discontinuation (~60–70%), but since our synthetic data does not model tumor response/progression, we focus on the remaining causes. The 15% rate aligns with the lower end of non-progression discontinuation reported in the literature and is appropriate for a 24-week treatment period.

---

## 4. Discontinuation Reasons

**Parameter distribution (among those who discontinue):**

| Reason | Proportion | CDISC Coded Value |
|--------|-----------|-------------------|
| Adverse event | 40% | ADVERSE EVENT |
| Withdrew consent | 20% | WITHDRAWAL BY SUBJECT |
| Physician decision | 15% | PHYSICIAN DECISION |
| Lost to follow-up | 10% | LOST TO FOLLOW-UP |
| Protocol deviation | 10% | PROTOCOL VIOLATION |
| Other | 5% | OTHER |

**Evidence:**

A survey of clinical research coordinators across oncology trials in Korea found that, excluding disease progression, the main reasons for study withdrawal were adverse events (10.6% of all enrolled, highest non-progression reason), withdrawal of consent (5.5%), and other controllable factors including loss to follow-up and medication non-adherence (3.8%) (PMC, 2022).

The JNCCN analysis reported that AE-related discontinuation was the dominant non-progression cause (13.2% experimental, 8.5% control), confirming adverse events as the primary driver.

In RCTs using placebo or best supportive care as control (N=47), placebo discontinuation due to an AE occurred in approximately 3% of patients (Annals of Oncology, 2016).

The IMvigor010 trial reported that in the observation arm, 20.5% of patients were censored due to consent withdrawal, protocol violation/noncompliance, or lost to follow-up combined (Cancer, 2021).

**Rationale:** Our distribution weights adverse events most heavily (40%) consistent with the literature showing toxicity as the primary non-progression discontinuation driver. Consent withdrawal (20%) and physician decision (15%) together represent the next tier. Lost to follow-up (10%) and protocol deviation (10%) are less common in well-run Phase III trials but occur at meaningful rates. This distribution applies only to the ~15% who discontinue, so the absolute rates (e.g., AE discontinuation = 40% × 15% = 6% of enrolled) are consistent with published data.

---

## 5. Adverse Event Rates

**Parameter:** Overall AE incidence 35–40% (active arms), 20% (placebo)

**Evidence:**

AE rates vary substantially by compound and tumor type. Our rates are drawn from the protocol's fictional Phase II data (Section 9.4) and are broadly consistent with published Phase III oncology trials where Grade 1–4 all-cause AE rates typically range from 30–90% depending on the compound.

The Annals of Oncology analysis found that grade 3/4 AEs related to placebo or best supportive care occurred in approximately 25% of patients, confirming that placebo arms are not AE-free.

**Rationale:** Our per-AE-term rates from the protocol (Section 9.4) produce overall AE incidences within plausible ranges. The active-to-placebo differential is the clinically meaningful signal our dashboard is designed to detect. Exact rates are fictional but structurally realistic.

---

## 6. AE Severity/Seriousness/Outcome Correlations

**Parameter:** Severity, seriousness, and outcome are correlated (not independent)

**Evidence:**

No single study provides a universal correlation matrix, but the relationship is well-established in clinical pharmacology and regulatory guidance:

- NCI CTCAE v5.0 defines severity grades where Grade 3 (severe) and above typically require medical intervention
- ICH E2A defines "serious" by consequence (hospitalization, disability, life-threatening, death), which is correlated with but distinct from severity
- Fatal outcomes by definition only occur with serious AEs
- Dose modifications (reduction, withdrawal) are protocol-driven responses to higher severity

**Our correlation model:**

| Severity | P(Serious) | P(Outcome=Fatal) | P(Action=Dose reduced or withdrawn) |
|----------|-----------|-------------------|-------------------------------------|
| MILD | 2% | 0% | 5% |
| MODERATE | 15% | 0% | 20% |
| SEVERE | 60% | 5% | 70% |

**Rationale:** These are modeled probabilities, not from a single published source. They reflect the clinical logic that severe events are far more likely to be serious, to lead to dose modifications, and (rarely) to be fatal. The exact probabilities are operational estimates consistent with standard clinical trial safety reporting patterns.

---

## 7. Laboratory Parameters

**Parameter:** Normal ranges and expected distributions for 6 lab tests

| Test | Units | Normal Range | Mean (enrolled pop) | SD | Source |
|------|-------|-------------|--------------------|----|--------|
| HGB | g/dL | 12.0–17.5 | 13.5 | 1.8 | Standard hematology reference |
| WBC | 10⁹/L | 4.0–11.0 | 7.0 | 2.5 | Standard hematology reference |
| PLAT | 10⁹/L | 150–400 | 250 | 60 | Standard hematology reference |
| CREAT | mg/dL | 0.6–1.2 | 0.9 | 0.2 | Standard chemistry reference |
| ALT | U/L | 7–56 | 25 | 12 | Standard chemistry reference |
| AST | U/L | 10–40 | 22 | 10 | Standard chemistry reference |

**Evidence:**

Normal reference ranges are drawn from standard clinical laboratory references (e.g., Tietz Clinical Guide to Laboratory Tests, Harrison's Principles of Internal Medicine). These ranges are used by most central laboratories worldwide.

Mean values are set within the normal range but account for the oncology population (e.g., HGB mean of 13.5 is slightly below the midpoint, reflecting the mild anemia common in advanced cancer patients meeting the inclusion criterion of HGB ≥10.0 g/dL).

**Rationale for missing lab rate (8%):** This is an operational estimate. No single meta-analysis quantifies missing lab rates across oncology trials, but 5–10% is considered typical in industry for missed or unevaluable samples. Reasons include missed visits, hemolyzed samples, insufficient volume, and lab processing errors.

---

## 8. Visit Schedule and Protocol Deviations

**Parameter:** 5% of visits fall outside the protocol-specified visit window

**Evidence:**

Visit window compliance varies by trial complexity, number of sites, and monitoring intensity. A specific meta-analysis for visit window deviations was not identified in the literature. The 5% rate is an operational estimate based on the following considerations:

- Well-monitored Phase III trials with central oversight typically achieve >90% visit window compliance
- Protocol deviations reports submitted to IRBs/ECs commonly cite visit timing as the most frequent minor deviation category
- FDA inspection findings frequently note visit window deviations as minor GCP findings

**Rationale:** 5% is conservative for a well-run Phase III trial. Rates in less monitored or decentralized trials may be higher (10–15%).

---

## 9. Site-Level Variation

**Parameter:** Sites vary in enrollment rate, screen failure rate, and protocol deviation frequency

**Evidence:**

Inter-site variability is well-documented in clinical trials but quantitative data is sparse in public literature. The following patterns are modeled:

- High-enrolling sites: 5 US sites enroll the majority of subjects, consistent with the known pattern that a small number of sites often contribute disproportionately to enrollment
- Screen failure variation: ±5 percentage points around the mean (25%), reflecting real differences in site pre-screening practices
- Protocol deviation variation: some sites have consistently higher deviation rates, reflecting differences in site quality and experience

**Rationale:** These patterns are based on standard operational experience in multi-site clinical trials and are not drawn from a specific publication.

---

## 10. Demographic Distribution

**Parameter:**

| Variable | Distribution | Rationale |
|----------|-------------|-----------|
| Age | 45–80 years, median ~62 | Oncology Phase III trials in solid tumors typically enroll patients with median age 58–65 |
| Sex | 55% Male, 45% Female | Slightly male-skewed consistent with many solid tumor indications |
| Race | WHITE 65%, ASIAN 15%, BLACK 10%, OTHER 10% | Reflects multi-country enrollment (US, UK, DE, JP, CA) |
| Ethnicity | NOT HISPANIC OR LATINO 88%, HISPANIC OR LATINO 12% | Consistent with US/European/Japanese enrollment |

**Evidence:**

Demographic distributions reflect the typical enrolled populations in global Phase III solid tumor trials. Exact distributions vary by indication and geography. The FDA and EMA have both emphasized the need for greater diversity in clinical trials, and current enrollment patterns are shifting.

**Rationale:** These distributions are modeled to produce realistic demographic data for analytics without claiming to represent any specific patient population.

---

## Summary of Parameters with Evidence Quality

| Parameter | Value | Evidence Quality | Notes |
|-----------|-------|-----------------|-------|
| Screen failure rate | 25% | **Strong** — multiple meta-analyses | Range 20–40% across studies |
| Screen failure reasons | See Section 2 | **Strong** — multi-center studies | Eligibility is dominant cause |
| Discontinuation rate | 15% | **Strong** — industry surveys + trial data | Excludes disease progression |
| Discontinuation reasons | See Section 4 | **Moderate** — survey data + trial reports | AE is dominant non-progression cause |
| AE rates by arm | Protocol-defined | **Moderate** — consistent with published ranges | Fictional compound, realistic rates |
| AE correlations | See Section 6 | **Clinical logic** — no single quantitative source | Based on CTCAE/ICH E2A definitions |
| Lab normal ranges | Standard reference | **Strong** — textbook values | Standard clinical laboratory ranges |
| Lab means/SDs | See Section 7 | **Moderate** — oncology population adjustments | Reflects inclusion criteria |
| Missing lab rate | 8% | **Operational norm** — no meta-analysis found | Industry estimate 5–10% |
| Protocol deviations | 5% | **Operational norm** — no meta-analysis found | Conservative for well-run trials |
| Site variation | Modeled | **Operational norm** | Based on industry experience |
| Demographics | See Section 10 | **Moderate** — consistent with published trial demographics | Multi-country enrollment |

---

## References

1. Applied Clinical Trials. "Can Recruitment and Retention Get Any Worse?" (2024 update). Industry survey of 76 global Phase II/III trials, 2016–2019.
2. Wong SE, North SA, Sweeney C, et al. Screen failure rates in contemporary Phase II/III therapeutic trials in genitourinary malignancies. J Clin Oncol. 2016;34(2_suppl):176.
3. Sridhar SS, et al. Screen Failure Rates in Contemporary Randomized Clinical Phase II/III Therapeutic Trials in Genitourinary Malignancies. Clin Genitourin Cancer. 2017.
4. Post hoc analysis of screening log of Phase III trial. Cancer Research, Statistics, and Treatment. 2021.
5. Addressing screening failures in early-phase clinical trials in oncology. ScienceDirect. 2025. Multi-center French study (Gustave Roussy, Oncopole Toulouse, Centre Léon Bérard).
6. Malhi N, Gresham G, Eigl BJ, et al. Characterizing discontinuation and withdrawal from phase III oncology clinical trials. J Clin Oncol. 2015;33(15_suppl):e17731.
7. Quantifying Withdrawal of Consent, Loss to Follow-Up, Early Drug Discontinuation, and Censoring in Oncology Trials. JNCCN. 2021;19(12):1433.
8. Participation in and withdrawal from cancer clinical trials: A survey of clinical research coordinators. PMC. 2022.
9. The reporting of adverse events in oncology Phase III trials. Annals of Oncology. 2016.
10. Early Termination of Oncology Clinical Trials in the United States. PMC. 2023.