SELECT d.STUDYID, d.USUBJID, d.SUBJID, d.SITEID, 
d.AGE, d.AGEU, d.SEX, d.RACE, d.COUNTRY, d.ARMCD, d.ARM, 
CAST(RFSTDTC AS DATE) as TRTSDT, 
CAST(RFENDTC AS DATE) as TRTEDT, 
DATEDIFF('day', RFSTDTC, RFENDTC) as TRTDUR, 
'Y' as ITTFL, 
CASE WHEN RFSTDTC IS NOT NULL THEN 'Y' ELSE 'N' END as SAFFL, 
DSDECOD, 
CASE WHEN DSDECOD != 'COMPLETED' THEN DSDECOD ELSE NULL END as DCSREAS, 
COALESCE(a.ae_count, 0) as ae_count,
COALESCE(a.max_severity, 'NONE') as max_severity,
COALESCE(a.has_sae, 'N') as has_sae,
COALESCE(l.abnormal_pct, 0) as abnormal_lab_pct
FROM {{ref('stg_dm')}} d LEFT JOIN {{ref('int_patient_ae_summary')}} a
ON d.USUBJID = a.USUBJID 
LEFT JOIN {{ref('int_patient_lab_summary')}} l
ON d.USUBJID = l.USUBJID 
WHERE RFSTDTC IS NOT NULL