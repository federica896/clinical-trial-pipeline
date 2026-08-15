WITH int_lb AS (
    SELECT USUBJID, 
    COUNT(LBSEQ) as total_lab_count, 
    COUNT(CASE WHEN LBNRIND IN ('LOW', 'HIGH') THEN 1 END) as abnormal_count, 
    COUNT(CASE WHEN LBNRIND = 'HIGH' THEN 1 END) as high_count,  
    COUNT(CASE WHEN LBNRIND = 'LOW' THEN 1 END) as low_count,  
    COUNT(DISTINCT VISITNUM) as total_visits_with_labs
    FROM {{ref('stg_lb')}} 
    GROUP BY USUBJID
)
SELECT *, 
ROUND(CAST(abnormal_count AS FLOAT)/total_lab_count*100, 1) AS abnormal_pct
FROM int_lb
