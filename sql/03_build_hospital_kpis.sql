-- sql/03_build_hospital_kpis.sql
-- Purpose: Pivot star rating measures into one row per hospital (6 KPI columns)

CREATE OR REPLACE TABLE hospital_kpis_2024 AS
SELECT
  facility_id,
  facility_name,
  state,

  MAX(CASE WHEN question = 'Nurse communication - star rating'
           THEN CAST(star_rating AS INTEGER) END) AS nurse_comm_stars,

  MAX(CASE WHEN question = 'Doctor communication - star rating'
           THEN CAST(star_rating AS INTEGER) END) AS doctor_comm_stars,

  MAX(CASE WHEN question = 'Staff responsiveness - star rating'
           THEN CAST(star_rating AS INTEGER) END) AS staff_responsiveness_stars,

  MAX(CASE WHEN question = 'Cleanliness - star rating'
           THEN CAST(star_rating AS INTEGER) END) AS cleanliness_stars,

  MAX(CASE WHEN question = 'Recommend hospital - star rating'
           THEN CAST(star_rating AS INTEGER) END) AS recommend_stars,

  MAX(CASE WHEN question = 'Overall hospital rating - star rating'
           THEN CAST(star_rating AS INTEGER) END) AS overall_rating_stars

FROM star_ratings_2024
WHERE star_rating != 'Not Available'
  AND question IN (
    'Nurse communication - star rating',
    'Doctor communication - star rating',
    'Staff responsiveness - star rating',
    'Cleanliness - star rating',
    'Recommend hospital - star rating',
    'Overall hospital rating - star rating'
  )
GROUP BY facility_id, facility_name, state;