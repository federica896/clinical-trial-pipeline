SELECT * REPLACE (
    CAST(LBDTC AS TIMESTAMP) as LBDTC
)
FROM {{source('raw', 'lb')}}