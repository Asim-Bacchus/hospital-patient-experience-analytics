-- sql/05_analysis.sql
-- Purpose: Core analysis - state averages + bottom performers

-- 1️⃣ State-level averages
CREATE OR REPLACE TABLE state_averages AS
SELECT
  state,
  COUNT(*) AS hospital_count,
  ROUND(AVG(nurse_comm_stars), 2) AS avg_nurse_comm,
  ROUND(AVG(doctor_comm_stars), 2) AS avg_doctor_comm,
  ROUND(AVG(staff_responsiveness_stars), 2) AS avg_staff_resp,
  ROUND(AVG(cleanliness_stars), 2) AS avg_cleanliness,
  ROUND(AVG(recommend_stars), 2) AS avg_recommend,
  ROUND(AVG(overall_rating_stars), 2) AS avg_overall
FROM hospital_kpis_2024
GROUP BY state
ORDER BY avg_overall ASC;

-- 2️⃣ Bottom performers (1-star overall)
CREATE OR REPLACE TABLE bottom_performers AS
SELECT *
FROM hospital_kpis_2024
WHERE overall_rating_stars = 1
ORDER BY state;