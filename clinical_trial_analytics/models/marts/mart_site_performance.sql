WITH int_mart_site AS (
    SELECT SITEID, COUNTRY, 
    COUNT(USUBJID) as total_screened, 
    COUNT(CASE WHEN RFSTDTC IS NOT NUll THEN 1 END) as total_enrolled, 
    COUNT(CASE WHEN RFSTDTC IS NULL THEN 1 END) as screen_failure_count, 
    COUNT(CASE WHEN DSDECOD='COMPLETED' THEN 1 END) as completed_count
    FROM {{ref('stg_dm')}}
    GROUP BY SITEID, COUNTRY
)
SELECT *, 
ROUND(CAST(screen_failure_count AS FLOAT)/total_screened * 100, 1) as screen_failure_pct, 
total_enrolled - completed_count as discontinued_count, 
ROUND(CAST(completed_count AS FLOAT)/total_enrolled * 100, 1) as completion_pct
FROM int_mart_site 
