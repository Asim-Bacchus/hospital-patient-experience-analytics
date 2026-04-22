-- Basic structure check
DESCRIBE star_ratings_2024;

-- Distribution of star ratings
SELECT
  star_rating,
  COUNT(*) AS count
FROM star_ratings_2024
GROUP BY star_rating
ORDER BY star_rating;

-- Count by state
SELECT
  state,
  COUNT(*) AS count
FROM star_ratings_2024
GROUP BY state
ORDER BY count DESC;