-- sql/01_filter_star_ratings.sql
-- Purpose: Create a filtered table of HCAHPS star rating measures for 2024.

CREATE OR REPLACE TABLE star_ratings_2024 AS
SELECT
  "Facility ID" AS facility_id,
  "Facility Name" AS facility_name,
  "State" AS state,
  "HCAHPS Question" AS question,
  "HCAHPS Answer Description" AS answer_desc,
  "Patient Survey Star Rating" AS star_rating,
  "Start Date" AS start_date,
  "End Date" AS end_date
FROM read_csv_auto('data/raw/HCAHPS-Hospital.csv')
WHERE
  lower("HCAHPS Question") LIKE '%star rating%'
  AND "Start Date" >= '2024-01-01'
  AND "Patient Survey Star Rating" IS NOT NULL;