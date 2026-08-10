import os
import sys
import pandas as pd 
import pandera.pandas as pa

class DmSchema(pa.DataFrameModel):
    STUDYID: str = pa.Field(eq="ONCO-2024-001")
    DOMAIN: str = pa.Field(eq="DM")
    USUBJID: str = pa.Field(unique=True)
    SUBJID: str 
    RFSTDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", nullable=True)
    RFENDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", nullable=True)
    SITEID: str = pa.Field(str_matches=r"^SITE-\d{3}$")
    BRTHDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}$")
    AGE: float = pa.Field(ge=18, le=100)
    AGEU: str = pa.Field(eq="YEARS")
    SEX: str = pa.Field(isin=["M", "F"])
    RACE: str = pa.Field(isin=["WHITE", "ASIAN", "BLACK OR AFRICAN AMERICAN", "AMERICAN INDIAN OR ALASKA NATIVE", "OTHER"])
    ETHNIC: str = pa.Field(isin=["HISPANIC OR LATINO", "NOT HISPANIC OR LATINO"])
    ARMCD: str = pa.Field(isin=["CMPX", "CMPY", "PBO"], nullable=True)
    ARM: str = pa.Field(isin=["Compound X 200mg BID", "Compound Y 150mg QD", "Placebo"], nullable=True)
    COUNTRY: str = pa.Field(isin=["USA", "GBR", "DEU", "JPN", "CAN"])
    DMDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
    DMDY: float = pa.Field(eq=1.0, nullable=True)
    DSDECOD: str = pa.Field(isin=["COMPLETED", "ADVERSE EVENT", "WITHDRAWAL BY SUBJECT", "PHYSICIAN DECISION", "LOST TO FOLLOW-UP", "PROTOCOL VIOLATION", "OTHER", "ELIGIBILITY CRITERIA NOT MET", "CONSENT WITHDRAWN", "LAB VALUES OUT OF RANGE"])
    DSSTDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}$")

    class Config:
        strict = True
        ordered = True
        coerce = True

    @pa.dataframe_check
    def screen_failure_no_arm(cls, df):
        """If RFSTDTC is null, ARMCD must be null"""
        mask = df["RFSTDTC"].isna()
        return mask.eq(df["ARMCD"].isna()) | ~mask

    @pa.dataframe_check
    def enrolled_has_arm(cls, df):
        """If RFSTDTC is not null, ARMCD must not be null"""
        mask = df["RFSTDTC"].notna()
        return ~mask | df["ARMCD"].notna()

    @pa.dataframe_check
    def end_after_start(cls, df):
        """RFENDTC >= RFSTDTC when both exist"""
        mask = df["RFSTDTC"].notna() & df["RFENDTC"].notna()
        return ~mask | (df["RFENDTC"] >= df["RFSTDTC"])

    @pa.dataframe_check
    def usubjid_contains_ids(cls, df):
        """USUBJID contains SITEID and SUBJID"""
        site_check = df.apply(lambda r: r["SITEID"] in r["USUBJID"], axis=1)
        subj_check = df.apply(lambda r: r["SUBJID"] in r["USUBJID"], axis=1)
        return site_check & subj_check
  

class AeSchema(pa.DataFrameModel):
    STUDYID: str = pa.Field(eq="ONCO-2024-001")
    DOMAIN: str = pa.Field(eq="AE")
    USUBJID: str 
    AESEQ: float = pa.Field(ge=1)
    AETERM: str
    AEDECOD: str
    AESEV: str = pa.Field(isin=["MILD", "MODERATE", "SEVERE"])
    AESER: str = pa.Field(isin=["Y", "N"])
    AEREL: str = pa.Field(isin=["RELATED", "POSSIBLY RELATED", "NOT RELATED"])
    AEACN: str = pa.Field(isin=["DOSE NOT CHANGED", "DOSE REDUCED", "DRUG WITHDRAWN"])
    AEOUT: str = pa.Field(isin=["RECOVERED/RESOLVED", "RECOVERING/RESOLVING", "NOT RECOVERED/NOT RESOLVED", "FATAL"])
    AESTDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
    AEENDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", nullable=True)
    AESTDY: float = pa.Field(ge=1.0)
    AEENDY: float = pa.Field(ge=1.0, nullable=True)

    class Config:
        strict = True
        ordered = True
        coerce = True
    
    @pa.dataframe_check
    def aeend_after_aest(cls, df):
        """AEENDTC > AESTDTC"""
        mask = df["AESTDTC"].notna() & df["AEENDTC"].notna()
        return ~mask | (df["AEENDTC"] >= df["AESTDTC"])


class LbSchema(pa.DataFrameModel):
    STUDYID: str = pa.Field(eq="ONCO-2024-001")
    DOMAIN: str = pa.Field(eq="LB")
    USUBJID: str 
    LBSEQ: float = pa.Field(ge=1)
    LBTESTCD: str = pa.Field(isin=["HGB", "WBC", "PLAT", "CREAT", "ALT", "AST"])
    LBTEST: str = pa.Field(isin=["Hemoglobin", "White Blood Cell Count", "Platelet Count", "Creatinine", "Alanine Aminotransferase", "Aspartate Aminotransferase"])
    LBORRES: str
    LBORRESU: str = pa.Field(isin=["g/dL", "10^9/L", "mg/dL", "U/L"])
    LBORNRLO: float = pa.Field(ge=0)
    LBORNRHI: float = pa.Field(ge=0)
    LBSTRESC: str
    LBSTRESN: float = pa.Field(ge=0)
    LBSTRESU: str = pa.Field(isin=["g/dL", "10^9/L", "mg/dL", "U/L"])
    LBNRIND: str = pa.Field(isin=["LOW", "NORMAL", "HIGH"])
    VISITNUM: float = pa.Field(ge=0)
    VISIT: str
    LBDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
    LBDY: float

    class Config:
        strict = True
        ordered = True
        coerce = True
    
    @pa.dataframe_check
    def ranges_check(cls, df):
        """LBORNRHI > LBORNRLO"""
        mask = df["LBORNRHI"].notna() & df["LBORNRLO"].notna()
        return ~mask | (df["LBORNRHI"] > df["LBORNRLO"])

    @pa.dataframe_check
    def test_name_check(cls, df):
        """LBSTRESN matches LBORRES"""
        return df["LBSTRESN"] == df["LBORRES"].astype(float)


class SvSchema(pa.DataFrameModel):
    STUDYID: str = pa.Field(eq="ONCO-2024-001")
    DOMAIN: str = pa.Field(eq="SV")
    USUBJID: str 
    VISITNUM: float = pa.Field(ge=0)
    VISIT: str = pa.Field(isin=["Screening", "Baseline", "Week 4", "Week 8", "Week 12", "Week 16", "Week 20", "Week 24 / EOT", "Follow-up (Week 28)"])
    SVSTDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
    SVENDTC: str = pa.Field(str_matches=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
    SVUPDES: str = pa.Field(isin=["VISIT OUTSIDE WINDOW", ""], nullable=True)

    class Config:
        strict = True
        ordered = True
        coerce = True
    
    @pa.dataframe_check
    def enddate_after_startdate(cls, df):
        """SVENDTC >= SVSTDTC"""
        mask = df["SVSTDTC"].notna() & df["SVENDTC"].notna()
        return ~mask | (df["SVENDTC"] >= df["SVSTDTC"])

class TsSchema(pa.DataFrameModel):
    STUDYID: str = pa.Field(eq="ONCO-2024-001")
    DOMAIN: str = pa.Field(eq="TS")
    TSSEQ: float = pa.Field(ge=1)
    TSPARMCD: str = pa.Field(unique=True)
    TSPARM: str
    TSVAL: str

    class Config:
        strict = True
        ordered = True
        coerce = True
    
