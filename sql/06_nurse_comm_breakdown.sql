-- =============================================================
-- 06_nurse_comm_breakdown.sql
-- Nurse Communication Sub-Dimension Analysis
-- Decomposes the nurse communication composite into its three
-- component behaviors and correlates each with overall rating.
-- =============================================================
 
-- Step 1: Pivot sub-dimension "Always" percentages and overall
-- star rating into one row per facility.
 
CREATE OR REPLACE TABLE nurse_comm_breakdown AS
WITH base AS (
    SELECT
        "Facility ID"                                       AS facility_id,
        "Facility Name"                                     AS facility_name,
        "State"                                             AS state,
        "HCAHPS Measure ID"                                 AS measure_id,
        TRY_CAST("HCAHPS Answer Percent" AS DOUBLE)         AS answer_pct,
        TRY_CAST("Patient Survey Star Rating" AS INTEGER)   AS star_rating
    FROM read_csv_auto('data/raw/HCAHPS-Hospital.csv')
    WHERE "End Date" = '12/31/2024'
      AND "HCAHPS Measure ID" IN (
          'H_NURSE_RESPECT_A_P',
          'H_NURSE_LISTEN_A_P',
          'H_NURSE_EXPLAIN_A_P',
          'H_STAR_RATING'
      )
)
SELECT
    facility_id,
    facility_name,
    state,
    MAX(CASE WHEN measure_id = 'H_NURSE_RESPECT_A_P' THEN answer_pct END) AS pct_always_respect,
    MAX(CASE WHEN measure_id = 'H_NURSE_LISTEN_A_P'  THEN answer_pct END) AS pct_always_listen,
    MAX(CASE WHEN measure_id = 'H_NURSE_EXPLAIN_A_P' THEN answer_pct END) AS pct_always_explain,
    MAX(CASE WHEN measure_id = 'H_STAR_RATING'        THEN star_rating END) AS overall_star_rating
FROM base
GROUP BY facility_id, facility_name, state
HAVING
    pct_always_respect   IS NOT NULL
    AND pct_always_listen  IS NOT NULL
    AND pct_always_explain IS NOT NULL
    AND overall_star_rating IS NOT NULL;
 
 
-- Step 2: Correlations between each sub-dimension and overall rating.
-- This tells us which specific nurse behavior drives satisfaction most.
 
SELECT
    ROUND(CORR(pct_always_respect, overall_star_rating), 3) AS r_respect_vs_overall,
    ROUND(CORR(pct_always_listen,  overall_star_rating), 3) AS r_listen_vs_overall,
    ROUND(CORR(pct_always_explain, overall_star_rating), 3) AS r_explain_vs_overall
FROM nurse_comm_breakdown;
 
 
-- Step 3: National averages per sub-dimension.
-- Baseline to contextualize state or facility-level comparisons.
 
SELECT
    ROUND(AVG(pct_always_respect), 1) AS national_avg_respect,
    ROUND(AVG(pct_always_listen),  1) AS national_avg_listen,
    ROUND(AVG(pct_always_explain), 1) AS national_avg_explain
FROM nurse_comm_breakdown;
 
 
-- Step 4: State-level averages for all three sub-dimensions.
-- Filtered to states with >= 20 facilities for reliability.
 
SELECT
    state,
    COUNT(*)                               AS facility_count,
    ROUND(AVG(pct_always_respect), 2)      AS avg_respect,
    ROUND(AVG(pct_always_listen),  2)      AS avg_listen,
    ROUND(AVG(pct_always_explain), 2)      AS avg_explain,
    ROUND(AVG(overall_star_rating), 2)     AS avg_overall_rating
FROM nurse_comm_breakdown
GROUP BY state
HAVING COUNT(*) >= 20
ORDER BY avg_overall_rating ASC;
 
 
-- Step 5: Bottom 10 states by each sub-dimension.
-- Identifies where specific communication behaviors break down most.
 
-- Respect
SELECT 'respect' AS dimension, state, ROUND(AVG(pct_always_respect), 2) AS avg_pct
FROM nurse_comm_breakdown
GROUP BY state HAVING COUNT(*) >= 20
ORDER BY avg_pct ASC LIMIT 10;
 
-- Listening
SELECT 'listen' AS dimension, state, ROUND(AVG(pct_always_listen), 2) AS avg_pct
FROM nurse_comm_breakdown
GROUP BY state HAVING COUNT(*) >= 20
ORDER BY avg_pct ASC LIMIT 10;
 
-- Explanation
SELECT 'explain' AS dimension, state, ROUND(AVG(pct_always_explain), 2) AS avg_pct
FROM nurse_comm_breakdown
GROUP BY state HAVING COUNT(*) >= 20
ORDER BY avg_pct ASC LIMIT 10;
