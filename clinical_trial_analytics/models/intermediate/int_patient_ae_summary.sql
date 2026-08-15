WITH int_ae AS (
    SELECT *, 
    CASE 
        WHEN AESEV='MILD' THEN 1
        WHEN AESEV='MODERATE' THEN 2 
        WHEN AESEV='SEVERE' THEN 3 
        ELSE 0
    END as severitynum 
    FROM {{ref('stg_ae')}}
)
SELECT USUBJID,
COUNT(AESEQ) as ae_count, 
CASE 
    WHEN MAX(severitynum)=3 THEN 'SEVERE'
    WHEN MAX(severitynum)=2 THEN 'MODERATE'
    WHEN MAX(severitynum)=1 THEN 'MILD'
END as max_severity,
MAX(AESER) as has_sae, 
MAX(CASE WHEN AEREL IN ('RELATED', 'POSSIBLY RELATED') THEN 'Y' ELSE 'N' END) as has_related_ae,
MIN(AESTDTC) as first_ae_date, 
MAX(AESTDTC) as last_ae_date, 
AVG(ae_duration_days) as avg_ae_duration_days, 
COUNT(CASE WHEN AESEV='SEVERE' THEN 1 END) as severe_ae_count
FROM int_ae
GROUP BY USUBJID 