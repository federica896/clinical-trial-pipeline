-- Returns rows where screen failed subjects have AEs: should be zero
SELECT d.USUBJID
FROM {{ref('stg_dm')}} d INNER JOIN {{ref('stg_ae')}} a
ON d.USUBJID = a.USUBJID 
WHERE d.RFSTDTC IS NULL 