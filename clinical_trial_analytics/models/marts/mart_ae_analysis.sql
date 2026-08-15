WITH arm_counts AS (
    SELECT ARMCD, ARM,
    COUNT(DISTINCT USUBJID) as enrolled_count
    FROM {{ ref('stg_dm') }}
    WHERE RFSTDTC IS NOT NULL
    GROUP BY ARMCD, ARM
),
ae_metrics AS (
    SELECT ARMCD,
    COUNT(DISTINCT a.USUBJID) as subjects_with_ae,
    COUNT(AESEQ) as total_aes,
    COUNT(CASE WHEN AESEV = 'MILD' THEN 1 END) as mild_count,
    COUNT(CASE WHEN AESEV = 'MODERATE' THEN 1 END) as moderate_count,
    COUNT(CASE WHEN AESEV = 'SEVERE' THEN 1 END) as severe_count,
    COUNT(CASE WHEN AESER = 'Y' THEN 1 END) as sae_count,
    COUNT(CASE WHEN AEREL IN ('RELATED', 'POSSIBLY RELATED') THEN 1 END) as related_count
    FROM {{ ref('stg_ae') }} a
    JOIN {{ ref('stg_dm') }} d ON a.USUBJID = d.USUBJID
    GROUP BY ARMCD
)
SELECT *,
ROUND(CAST(subjects_with_ae AS FLOAT) / enrolled_count * 100, 1) as ae_rate_pct
FROM arm_counts
JOIN ae_metrics USING (ARMCD)