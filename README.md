# Healthcare Operations Analytics
## Understanding Hospital Performance Through Patient Experience Data

> A SQL-based analysis of 4,000+ U.S. hospitals using CMS HCAHPS data, identifying nurse communication as the strongest operational correlate of patient satisfaction

---

## Project Overview

Hospitals are complex operational systems. While clinical outcomes often dominate performance discussions, patient experience metrics provide a powerful lens into how effectively a hospital's day-to-day operations function.

This project analyzes national CMS HCAHPS (Hospital Consumer Assessment of Healthcare Providers and Systems) survey data to answer a practical operational question:

> **Which hospitals underperform on patient experience metrics, and how does performance vary across states and care dimensions?**

Using publicly available CMS data (445,000+ rows across 22,000+ facilities), I structured, filtered, and transformed hospital-level survey data into standardized performance indicators suitable for operational analysis.

The analysis finds that nurse communication is the strongest operational predictor of overall hospital satisfaction (r = 0.79), with a one-star increase associated with a 0.68-star increase in overall rating. State-level underperformance consistently aligns with weaker communication metrics, suggesting frontline interpersonal care is a primary driver of patient experience variation.

---

## Business Context

HCAHPS scores are more than survey results. They are:

- Publicly reported quality benchmarks
- Tied to hospital reimbursement
- Closely monitored by operations leadership
- Influential in patient retention and reputation

Understanding variation in these metrics helps identify operational weaknesses in communication, responsiveness, and facility management.

If patient experience reflects operational health, what patterns emerge when we analyze it at scale?

---

## Dataset

**Source:** Centers for Medicare & Medicaid Services (CMS) — data.cms.gov  
**Dataset:** HCAHPS Patient Survey — Hospital (2024 Reporting Year)  
**Size:** 445,563 rows | 22,279 facilities

The raw dataset is structured in long format and includes multiple reporting types (percentages, linear mean scores, and star ratings). To ensure comparability and clarity, this analysis focuses exclusively on standardized star-rating measures.

---

## KPI Definition

The following CMS-defined star ratings were used:

| KPI | Description |
|-----|-------------|
| `nurse_comm_stars` | Nurse communication star rating |
| `doctor_comm_stars` | Doctor communication star rating |
| `staff_responsiveness_stars` | Staff responsiveness star rating |
| `cleanliness_stars` | Hospital cleanliness star rating |
| `recommend_stars` | Would recommend hospital star rating |
| `overall_rating_stars` | Overall hospital rating |

Each KPI is reported on a 1–5 star scale.

---

## Methodology

### 1. Data Filtering & Cleaning (SQL + DuckDB)
- Queried raw CSV directly using DuckDB without manual import
- Filtered to star-rating measures only
- Limited analysis to 2024 reporting period
- Removed null and "Not Available" entries
- Standardized facility identifiers

### 2. Data Transformation
- Pivoted long-format survey data into wide hospital-level KPI table
- Produced one row per facility with structured performance metrics
- Exported processed dataset to `data/processed/`

### 3. Analysis
- Computed state-level KPI averages and rankings
- Calculated Pearson correlations between each KPI and overall rating
- Applied simple linear regression to estimate effect size of nurse communication
- Identified bottom-performing states by both overall rating and nurse communication

---

## Results

### 1️⃣ National Drivers of Overall Hospital Rating

| KPI | Correlation (r) |
|-----|----------------|
| Recommend hospital | 0.862 |
| Nurse communication | **0.792** |
| Doctor communication | 0.734 |
| Staff responsiveness | 0.726 |
| Cleanliness | 0.597 |

While "recommend hospital" is outcome-adjacent, **nurse communication is the strongest operational predictor of overall rating** — outperforming doctor communication, staff responsiveness, and cleanliness.

---

### 2️⃣ Estimated Operational Impact

Using simple linear regression:

> A **1-star increase in nurse communication** is associated with an estimated **+0.684-star increase in overall hospital rating**.

On a 1–5 scale, this represents a substantial effect size with meaningful operational implications.

---

### 3️⃣ State-Level Performance Patterns

Among states with ≥20 facilities, low overall performance consistently aligns with low nurse communication scores. The same states appear in both bottom-10 lists:

- New Jersey (avg overall: 2.75 | avg nurse comm: 2.73)
- New York (avg overall: 2.81 | avg nurse comm: 2.84)
- Florida (avg overall: 2.94 | avg nurse comm: 2.70)

This pattern suggests that frontline interpersonal care quality is a meaningful differentiator in statewide performance variation — not physical facility conditions.

---

## Operational Implications

If patient experience is treated as an operational performance metric rather than a marketing outcome, this analysis suggests that investments in frontline communication quality — particularly nursing staff interaction — may yield greater impact on satisfaction scores than environment-focused improvements alone.

For hospital systems, this implies that process design, staffing models, and communication training may be high-leverage intervention points. States and facilities that underperform on communication metrics show consistent alignment with lower overall ratings, making nurse communication a practical leading indicator worth monitoring.

---

## Project Structure

```
hospital-patient-experience-analytics/
├── README.md
├── data/
│   ├── raw/                        # Original CMS HCAHPS CSV
│   └── processed/
│       └── hospital_kpis_2024.csv  # Clean hospital-level KPI table
├── db/
│   └── hcahps.duckdb               # DuckDB database
├── sql/
│   ├── 01_filter_star_ratings.sql
│   ├── 02_explore_star_ratings.sql
│   ├── 03_build_hospital_kpis.sql
│   ├── 04_export_processed.sql
│   └── 05_analysis.sql
├── src/
│   └── run_sql.py                  # Pipeline runner
├── dashboard/
│   └── figures/                    # Visualizations
├── reports/
│   └── insights_report.md
└── requirements.txt
```

---

## Tools & Skills Demonstrated

- SQL querying, filtering, and aggregation (DuckDB)
- Long-to-wide data transformation (PIVOT)
- KPI design aligned with business objectives
- Correlation and regression analysis
- Healthcare quality metric interpretation
- Analytical storytelling and performance reporting
- Reproducible data pipeline design

---

## Portfolio Context

This project is the second in a two-part healthcare operations analytics portfolio:

| Project | Focus |
|---------|-------|
| Preventable Punchlisting Analysis | Root-cause analysis of operational failure in IT deployment workflows |
| Hospital Patient Experience Analytics *(this project)* | Performance monitoring and structured insight generation from national healthcare data |

Together they demonstrate a full analyst cycle:

**Diagnose operational breakdown → Build performance monitoring systems.**

---

## Author

Asim Bacchus  
[LinkedIn](#) | [GitHub](#)
