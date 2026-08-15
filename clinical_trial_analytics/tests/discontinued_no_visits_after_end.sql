-- Returns rows if visit is after RFENDTC: should be zero
SELECT VISIT
FROM {{ref('stg_dm')}} d INNER JOIN {{ref('stg_sv')}} s
ON d.USUBJID = s.USUBJID 
WHERE s.SVSTDTC > d.RFENDTC