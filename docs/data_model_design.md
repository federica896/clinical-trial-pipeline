# Clinical Trial Data Model — CDISC SDTM Aligned

## Overview

This pipeline models data for a Phase III oncology trial (ONCO-2024-001).
Naming, variable ordering, and attributes follow CDISC SDTM Implementation Guide (v3.3) conventions.

**Variable ordering rule:** Identifiers → Topic → Qualifiers → Timing (per SDTMIG v3.3 Section 3.1)

## Variable Attribute Conventions

Per the SDTM standard and SAS V5 transport file (XPT) format requirements:

| Attribute | Constraint | Notes |
|-----------|-----------|-------|
| Variable name | Max 8 characters | Alphanumeric, no special characters |
| Variable label | Max 40 characters | Unique within domain |
| Data types | Char or Num only | SDTM recognizes only these two types; Define-XML provides richer types (integer, float, date, datetime) |
| Char length | Set to actual max data length | FDA rule FDAC036: minimize file size by assigning length based on actual data |
| Num length | 8 bytes | All numeric values stored as 8-byte floats in XPT |
| Date/time values | Char, ISO 8601 format | Stored as character strings (e.g., "2024-01-15" or "2024-01-15T10:30:00") |
| Controlled terms | Uppercase | Per CDISC Controlled Terminology (CT) |

> **Note on this project:** Since we are building an analytics pipeline in DuckDB (not generating XPT files for regulatory submission), dates are stored as VARCHAR in the raw layer per SDTM convention, then cast to native DATE types in the dbt staging layer. Character lengths are documented for reference but not enforced at the database level.

> **CT notation:** `*` = sponsor-defined terms permitted; `**` = external dictionary (e.g., MedDRA)

## Core Designations

| Code | Meaning | Description |
|------|---------|-------------|
| Req | Required | Must be included in every submission dataset |
| Exp | Expected | Should be included if collected or derivable |
| Perm | Permissible | May be included if relevant to the study |

---

## Source Entities (Raw)

### 1. DM — Demographics (Special Purpose Domain)

DM is a special-purpose domain with a fixed structure. One record per subject.

| # | Variable | Label | Role | SDTM Type | Length | Format / CT | Core |
|---|----------|-------|------|-----------|--------|-------------|------|
| 1 | STUDYID | Study Identifier | Identifier | Char | 20 | | Req |
| 2 | DOMAIN | Domain Abbreviation | Identifier | Char | 2 | "DM" | Req |
| 3 | USUBJID | Unique Subject Identifier | Identifier | Char | 30 | STUDYID-SITEID-SUBJID | Req |
| 4 | SUBJID | Subject Identifier for the Study | Identifier | Char | 8 | | Req |
| 5 | RFSTDTC | Subject Reference Start Date/Time | Record Qualifier | Char | 19 | ISO 8601 datetime | Exp |
| 6 | RFENDTC | Subject Reference End Date/Time | Record Qualifier | Char | 19 | ISO 8601 datetime | Exp |
| 7 | SITEID | Study Site Identifier | Record Qualifier | Char | 8 | | Req |
| 8 | BRTHDTC | Date/Time of Birth | Record Qualifier | Char | 10 | ISO 8601 date | Perm |
| 9 | AGE | Age | Record Qualifier | Num | 8 | Derived: RFSTDTC − BRTHDTC | Exp |
| 10 | AGEU | Age Units | Record Qualifier | Char | 6 | CT: AGEU ("YEARS") | Exp |
| 11 | SEX | Sex | Record Qualifier | Char | 1 | CT: SEX (M, F) | Req |
| 12 | RACE | Race | Record Qualifier | Char | 40 | CT: RACE * | Exp |
| 13 | ETHNIC | Ethnicity | Record Qualifier | Char | 30 | CT: ETHNIC * | Perm |
| 14 | ARMCD | Planned Arm Code | Record Qualifier | Char | 20 | | Req |
| 15 | ARM | Description of Planned Arm | Record Qualifier | Char | 40 | | Req |
| 16 | COUNTRY | Country | Record Qualifier | Char | 3 | ISO 3166 alpha-3 | Req |
| 17 | DMDTC | Date/Time of Collection | Timing | Char | 19 | ISO 8601 | Perm |
| 18 | DMDY | Study Day of Collection | Timing | Num | 8 | Derived | Perm |

**Additional variables for our analytics (non-standard, would go in SUPPDM in a real submission):**

| Variable | Label | SDTM Type | Length | Format / CT | Notes |
|----------|-------|-----------|--------|-------------|-------|
| DSDECOD | Disposition Decoded | Char | 20 | CT: NCOMPLT * | Completed / Discontinued / Screen Failure / Ongoing |
| DSSTDTC | Disposition Date | Char | 10 | ISO 8601 date | |

> **Deviation note:** In a real submission, disposition data belongs in the DS domain. We include DSDECOD/DSSTDTC here for simplicity in our analytics pipeline and document this deviation.

---

### 2. AE — Adverse Events (Events Class)

Variable order: Identifiers → Topic → Qualifiers → Timing. One record per adverse event per subject.

| # | Variable | Label | Role | SDTM Type | Length | Format / CT | Core |
|---|----------|-------|------|-----------|--------|-------------|------|
| 1 | STUDYID | Study Identifier | Identifier | Char | 20 | | Req |
| 2 | DOMAIN | Domain Abbreviation | Identifier | Char | 2 | "AE" | Req |
| 3 | USUBJID | Unique Subject Identifier | Identifier | Char | 30 | | Req |
| 4 | AESEQ | Sequence Number | Identifier | Num | 8 | | Req |
| 5 | AETERM | Reported Term for the AE | Topic | Char | 200 | Free text | Req |
| 6 | AEDECOD | Dictionary-Derived Term | Synonym Qualifier | Char | 200 | MedDRA PT ** | Perm |
| 7 | AESEV | Severity/Intensity | Record Qualifier | Char | 10 | CT: SEV (MILD, MODERATE, SEVERE) | Exp |
| 8 | AESER | Serious Event | Record Qualifier | Char | 1 | CT: NY (Y, N) | Exp |
| 9 | AEREL | Causality | Record Qualifier | Char | 20 | CT: REL * | Exp |
| 10 | AEACN | Action Taken with Study Treatment | Record Qualifier | Char | 40 | CT: ACN * | Exp |
| 11 | AEOUT | Outcome of Adverse Event | Record Qualifier | Char | 40 | CT: OUT * | Exp |
| 12 | AESTDTC | Start Date/Time of AE | Timing | Char | 19 | ISO 8601 | Exp |
| 13 | AEENDTC | End Date/Time of AE | Timing | Char | 19 | ISO 8601 | Exp |
| 14 | AESTDY | Study Day of Start of AE | Timing | Num | 8 | Derived | Perm |
| 15 | AEENDY | Study Day of End of AE | Timing | Num | 8 | Derived | Perm |

---

### 3. LB — Laboratory Test Results (Findings Class)

Variable order: Identifiers → Topic → Qualifiers → Timing. One record per lab test per visit per subject.

| # | Variable | Label | Role | SDTM Type | Length | Format / CT | Core |
|---|----------|-------|------|-----------|--------|-------------|------|
| 1 | STUDYID | Study Identifier | Identifier | Char | 20 | | Req |
| 2 | DOMAIN | Domain Abbreviation | Identifier | Char | 2 | "LB" | Req |
| 3 | USUBJID | Unique Subject Identifier | Identifier | Char | 30 | | Req |
| 4 | LBSEQ | Sequence Number | Identifier | Num | 8 | | Req |
| 5 | LBTESTCD | Lab Test Short Name | Topic | Char | 8 | CT: LBTESTCD * | Req |
| 6 | LBTEST | Lab Test Name | Synonym Qualifier | Char | 40 | CT: LBTEST * | Req |
| 7 | LBORRES | Result in Original Units | Result Qualifier | Char | 20 | | Exp |
| 8 | LBORRESU | Original Units | Variable Qualifier | Char | 20 | CT: UNIT * | Exp |
| 9 | LBORNRLO | Normal Range Lower Limit (Orig) | Variable Qualifier | Char | 20 | | Exp |
| 10 | LBORNRHI | Normal Range Upper Limit (Orig) | Variable Qualifier | Char | 20 | | Exp |
| 11 | LBSTRESC | Character Result in Std Units | Result Qualifier | Char | 20 | | Exp |
| 12 | LBSTRESN | Numeric Result in Std Units | Result Qualifier | Num | 8 | | Exp |
| 13 | LBSTRESU | Standard Units | Variable Qualifier | Char | 20 | CT: UNIT * | Exp |
| 14 | LBNRIND | Reference Range Indicator | Record Qualifier | Char | 10 | CT: NRIND (NORMAL, LOW, HIGH) | Exp |
| 15 | VISITNUM | Visit Number | Timing | Num | 8 | | Exp |
| 16 | VISIT | Visit Name | Timing | Char | 40 | | Perm |
| 17 | LBDTC | Date/Time of Specimen Collection | Timing | Char | 19 | ISO 8601 | Exp |
| 18 | LBDY | Study Day of Specimen Collection | Timing | Num | 8 | Derived | Perm |

> **Note on result fields:** SDTM requires both original (LBORRES/LBORRESU) and standard (LBSTRESN/LBSTRESC/LBSTRESU) result representations. In our synthetic data, original and standard values are identical since no unit conversion is needed. Normal range limits (LBORNRLO/LBORNRHI) are stored as Char per SDTM convention, even when values are numeric.

---

### 4. SV — Subject Visits (Special Purpose Domain)

SV is a special-purpose domain. One record per subject per actual visit.

| # | Variable | Label | Role | SDTM Type | Length | Format / CT | Core |
|---|----------|-------|------|-----------|--------|-------------|------|
| 1 | STUDYID | Study Identifier | Identifier | Char | 20 | | Req |
| 2 | DOMAIN | Domain Abbreviation | Identifier | Char | 2 | "SV" | Req |
| 3 | USUBJID | Unique Subject Identifier | Identifier | Char | 30 | | Req |
| 4 | VISITNUM | Visit Number | Timing | Num | 8 | | Req |
| 5 | VISIT | Visit Name | Timing | Char | 40 | | Perm |
| 6 | SVSTDTC | Start Date/Time of Visit | Timing | Char | 19 | ISO 8601 | Exp |
| 7 | SVENDTC | End Date/Time of Visit | Timing | Char | 19 | ISO 8601 | Exp |

**Additional variable for our analytics:**

| Variable | Label | SDTM Type | Length | Format / CT | Notes |
|----------|-------|-----------|--------|-------------|-------|
| SVUPDES | Unplanned Visit Description | Char | 200 | Free text | Used to flag protocol deviations |

> **Deviation note:** SVUPDES is a standard SDTM variable but is typically used for unscheduled visits. We repurpose it to flag visit window deviations for our analytics.

---

### 5. TS — Trial Summary (Trial Design Domain)

One record per trial summary parameter.

| # | Variable | Label | Role | SDTM Type | Length | Format / CT | Core |
|---|----------|-------|------|-----------|--------|-------------|------|
| 1 | STUDYID | Study Identifier | Identifier | Char | 20 | | Req |
| 2 | DOMAIN | Domain Abbreviation | Identifier | Char | 2 | "TS" | Req |
| 3 | TSSEQ | Sequence Number | Identifier | Num | 8 | | Req |
| 4 | TSPARMCD | Trial Summary Parameter Short Name | Topic | Char | 8 | CT: TSPARMCD * | Req |
| 5 | TSPARM | Trial Summary Parameter Name | Synonym Qualifier | Char | 40 | CT: TSPARM * | Req |
| 6 | TSVAL | Parameter Value | Record Qualifier | Char | 200 | | Req |

---

## Relationships

```
DM.USUBJID ──1:M──→ AE.USUBJID
DM.USUBJID ──1:M──→ LB.USUBJID
DM.USUBJID ──1:M──→ SV.USUBJID
DM.SITEID  ────────→ Site metadata in TS
```

## Key Design Decisions

1. **STUDYID and DOMAIN** included in every table as per SDTM requirements
2. **Variable ordering** follows SDTMIG v3.3: Identifiers → Topic → Qualifiers → Timing
3. **Variable attributes** (labels, types, lengths) documented per SAS V5 XPT conventions
4. **USUBJID format**: `STUDYID-SITEID-SUBJID` (e.g., `ONCO-2024-001-SITE-001-0001`)
5. **All dates stored as Char** in ISO 8601 format per SDTM convention — cast to DATE in dbt staging layer
6. **All numeric values** are 8-byte (Num 8) per XPT format — no integer/float distinction at SDTM level
7. **Character lengths** set to actual maximum data length per FDA rule FDAC036
8. **Disposition in DM** rather than separate DS domain — documented as intentional simplification
9. **LB includes both original and standard result fields** (LBORRES/LBSTRESN) per SDTM standard
10. **AGE derived** from BRTHDTC and RFSTDTC, which is standard SDTM practice

## Realistic Data Patterns

- ~1200 screened subjects across 12 sites
- ~15% screen failures (DSDECOD = 'Screen Failure')
- ~10% early discontinuations
- ~5% protocol deviations (visit windows violated, flagged in SV.SVUPDES)
- ~8% missing lab values
- AE rates differ by treatment arm (Drug A: 40%, Drug B: 35%, Placebo: 20%)
- 2:2:1 randomization ratio (Drug A : Drug B : Placebo)
- Treatment-related AE causality higher in active arms vs placebo

## Controlled Terminology Reference

| Variable | Codelist ID | Extensible | Values Used |
|----------|------------|------------|-------------|
| SEX | C66731 | No | M, F |
| RACE | C74457 | Yes | WHITE, BLACK OR AFRICAN AMERICAN, ASIAN, AMERICAN INDIAN OR ALASKA NATIVE, OTHER |
| ETHNIC | C66790 | No | HISPANIC OR LATINO, NOT HISPANIC OR LATINO |
| AGEU | C66781 | No | YEARS |
| AESEV (SEV) | C66769 | No | MILD, MODERATE, SEVERE |
| AESER (NY) | C66742 | No | Y, N |
| AEREL (REL) | C66728 | Yes | RELATED, POSSIBLY RELATED, NOT RELATED |
| AEACN (ACN) | C66767 | Yes | DOSE NOT CHANGED, DOSE REDUCED, DRUG WITHDRAWN |
| AEOUT (OUT) | C66768 | No | RECOVERED/RESOLVED, RECOVERING/RESOLVING, NOT RECOVERED/NOT RESOLVED, FATAL |
| LBNRIND (NRIND) | C78736 | No | NORMAL, LOW, HIGH |
| LBTESTCD | C65047 | Yes | HGB, WBC, PLAT, CREAT, ALT, AST |
| COUNTRY | C66729 | N/A | ISO 3166 alpha-3 codes |

> **CT version note:** Controlled terminology codelist IDs reference CDISC CT published packages. In a real submission, the specific CT version used would be declared in Define-XML.