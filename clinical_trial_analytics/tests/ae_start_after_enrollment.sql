-- Returns rows where AE started before enrollment: should be zero
SELECT
    a.USUBJID,
    a.AESTDTC,
    d.RFSTDTC
FROM {{ ref('stg_ae') }} a
JOIN {{ ref('stg_dm') }} d ON a.USUBJID = d.USUBJID
WHERE a.AESTDTC < d.RFSTDTC