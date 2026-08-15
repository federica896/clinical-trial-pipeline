-- Returns rows where AE end date is before the start date: should be zero
SELECT USUBJID, AESTDTC, AEENDTC
FROM {{ref('stg_ae')}}
WHERE AEENDTC < AESTDTC