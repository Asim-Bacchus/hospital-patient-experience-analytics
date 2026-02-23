-- sql/04_export_processed.sql
-- Purpose: Export clean hospital KPI table to data/processed as CSV

COPY (
  SELECT *
  FROM hospital_kpis_2024
)
TO 'data/processed/hospital_kpis_2024.csv'
(FORMAT CSV, HEADER);