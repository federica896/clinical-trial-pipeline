-- Returns rows Lab VISITNUM is not matching an actual visit in SV: should be zero
SELECT l.USUBJID
FROM {{ref('stg_lb')}} l 
WHERE NOT EXISTS (
    SELECT 1 
    FROM {{ref('stg_sv')}} s
    WHERE l.USUBJID = s.USUBJID and l.VISITNUM = s.VISITNUM
)