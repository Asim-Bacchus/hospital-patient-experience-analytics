# Healthcare Operations Analytics
## Understanding Hospital Performance Through Patient Experience Data

> A SQL-based analysis of 4,000+ U.S. hospitals using CMS HCAHPS data, finding nurse communication as the strongest operational correlate of patient satisfaction across all care dimensions tested.

---

## Project Overview

Hospitals are complex operational systems. While clinical outcomes often dominate performance discussions, patient experience metrics provide a powerful lens into how effectively a hospital's day-to-day operations function.

This project analyzes national CMS HCAHPS (Hospital Consumer Assessment of Healthcare Providers and Systems) survey data to answer a practical operational question:

> **Which hospitals underperform on patient experience metrics, and how does performance vary across states and care dimensions?**

Using publicly available CMS data (445,000+ rows across 22,000+ facilities), I structured, filtered, and transformed hospital-level survey data into standardized performance indicators suitable for operational analysis.

The analysis finds that nurse communication is the strongest operational correlate of overall hospital satisfaction (r = 0.79), with a one-star increase associated with a 0.68-star increase in overall rating. A deeper sub-dimension analysis reveals that patients consistently rate nurses higher on courtesy and respect (85.7% "always") than on explanation clarity (74.1% "always"), suggesting the communication gap is not attitudinal but informational. State-level underperformance consistently aligns with weaker communication metrics, pointing to frontline interpersonal care as the primary driver of patient experience variation.

---

## Business Context

HCAHPS scores are more than survey results. They are publicly reported quality benchmarks, tied to Medicare reimbursement, closely monitored by operations leadership, and influential in patient retention and reputation.

If patient experience reflects operational health, what patterns emerge when we analyze it at scale?

---

## Dataset

**Source:** Centers for Medicare & Medicaid Services (CMS) -- data.cms.gov
**Dataset:** HCAHPS Patient Survey -- Hospital (2024 Reporting Year)
**Size:** 445,563 rows | 22,279 facilities

The raw dataset is structured in long format and includes multiple reporting types (percentages, linear mean scores, and star ratings). This analysis works across both layers: star ratings for facility-level KPI comparison, and raw percent scores for sub-dimension analysis where continuous measures preserve more signal.

---

## KPI Definition

The following CMS-defined star ratings were used for the primary analysis:

| KPI | Description |
|-----|-------------|
| `nurse_comm_stars` | Nurse communication star rating |
| `doctor_comm_stars` | Doctor communication star rating |
| `staff_responsiveness_stars` | Staff responsiveness star rating |
| `cleanliness_stars` | Hospital cleanliness star rating |
| `recommend_stars` | Would recommend hospital star rating |
| `overall_rating_stars` | Overall hospital rating |

Each KPI is reported on a 1-5 star scale.

The sub-dimension analysis uses raw percent scores from three individual HCAHPS survey questions that compose the nurse communication composite:

| Measure ID | Survey Question |
|------------|----------------|
| `H_NURSE_RESPECT_A_P` | How often did nurses treat you with courtesy and respect? |
| `H_NURSE_LISTEN_A_P` | How often did nurses listen carefully to you? |
| `H_NURSE_EXPLAIN_A_P` | How often did nurses explain things in a way you could understand? |

---

## Methodology

### 1. Data Filtering and Cleaning (SQL + DuckDB)
- Queried raw CSV directly using DuckDB without manual import
- Filtered to star-rating measures only for primary KPI analysis
- Limited analysis to 2024 reporting period
- Removed null and "Not Available" entries
- Standardized facility identifiers

### 2. Data Transformation
- Pivoted long-format survey data into wide hospital-level KPI table
- Produced one row per facility with structured performance metrics
- Exported processed dataset to `data/processed/`

### 3. Primary Analysis
- Computed state-level KPI averages and rankings
- Calculated Pearson correlations between each KPI and overall rating
- Applied simple linear regression to estimate effect size of nurse communication
- Identified bottom-performing states by overall rating and nurse communication

### 4. Sub-Dimension Analysis
- Extracted raw "always" percent scores for the three nurse communication survey items
- Pivoted into a facility-level table and correlated each sub-dimension against overall rating
- Computed national averages per sub-dimension to identify where the communication gap is largest
- Ran state-level breakdowns per sub-dimension to test whether underperforming states are weak across all three behaviors or concentrated in specific ones

---

## Results

### 1. National Drivers of Overall Hospital Rating

| KPI | Correlation (r) |
|-----|----------------|
| Recommend hospital | 0.862 |
| Nurse communication | **0.792** |
| Doctor communication | 0.734 |
| Staff responsiveness | 0.726 |
| Cleanliness | 0.597 |

While "recommend hospital" is outcome-adjacent, nurse communication is the strongest operational correlate of overall rating, outperforming doctor communication, staff responsiveness, and cleanliness.

---

### 2. Estimated Operational Impact

Using simple linear regression:

> A **1-star increase in nurse communication** is associated with an estimated **+0.684-star increase** in overall hospital rating.

On a 1-5 scale, this represents a substantial effect size with meaningful operational implications.

---

### 3. State-Level Performance Patterns

Among states with 20 or more facilities, low overall performance consistently aligns with low nurse communication scores. The same states appear in both bottom-10 lists:

- New Jersey (avg overall: 2.75 | avg nurse comm: 2.73)
- New York (avg overall: 2.81 | avg nurse comm: 2.84)
- Florida (avg overall: 2.94 | avg nurse comm: 2.70)

This pattern suggests that frontline interpersonal care quality is a meaningful differentiator in statewide performance variation, more so than physical facility conditions.

---

### 4. Nurse Communication Sub-Dimension Breakdown

Decomposing the nurse communication composite into its three component survey questions reveals that sub-dimension percent scores correlate more strongly with overall rating (r = 0.83-0.85) than the composite star rating alone (r = 0.79). This reflects greater signal preserved in continuous percent measures versus ordinal star ratings.

| Sub-Dimension | Correlation with Overall Rating | National "Always" Rate |
|---------------|--------------------------------|----------------------|
| Nurses listened carefully | **0.847** | 75.9% |
| Nurses treated with respect | 0.843 | 85.7% |
| Nurses explained clearly | 0.834 | 74.1% |

The national averages surface a meaningful operational gap: patients report nurses treat them with courtesy at a much higher rate (85.7%) than they explain things clearly (74.1%). An 11-point spread between respect and explanation suggests the communication problem is not attitudinal but informational. Nurses are largely perceived as kind; they are less consistently perceived as clear.

All three sub-dimensions show nearly equal correlation strength with overall satisfaction, which means nurse communication quality is holistic. Targeted interventions on a single behavior are unlikely to move the needle as much as broader communication practice improvements.

State-level breakdowns confirm that underperforming states (NJ, NY, FL, MD, CA) appear consistently across all three sub-dimension bottom-10 lists, reinforcing that these are systemic patterns rather than isolated weaknesses.

---

## Operational Implications

If patient experience is treated as an operational performance metric rather than a marketing outcome, this analysis points to frontline communication quality as the highest-leverage area for improvement, with nurse interactions as the primary driver.

The sub-dimension findings add specificity to that recommendation. The gap between how often nurses are courteous (85.7%) versus how often they explain things clearly (74.1%) suggests that communication training focused on information delivery, plain-language explanation of medications and discharge instructions, and active listening protocols may yield more impact than environment-focused or attitude-focused interventions alone.

For hospital systems, this implies that process design, staffing models, and structured communication frameworks (such as AIDET or teach-back methodology) are high-leverage intervention points. States and facilities that underperform on communication metrics show consistent alignment with lower overall ratings across all three nurse communication behaviors, making this composite a practical leading indicator worth monitoring at both the facility and state level.

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
│   ├── 05_analysis.sql
│   └── 06_nurse_comm_breakdown.sql
├── src/
│   ├── make_figures.py
│   └── run_sql.py                  # Pipeline runner
├── dashboard/
│   └── figures/                    # Visualizations
├── reports/
│   └── insights_report.md
└── requirements.txt
```

---
## Tools and Skills Demonstrated

- SQL querying, filtering, and aggregation (DuckDB)
- Long-to-wide data transformation (PIVOT)
- KPI design aligned with business objectives
- Pearson correlation and simple linear regression
- Sub-dimension decomposition of composite survey measures
- Healthcare quality metric interpretation (HCAHPS, CMS)
- Analytical storytelling and performance reporting
- Reproducible data pipeline design

---

## Portfolio Context

This project is the second in a two-part healthcare operations analytics portfolio:

| Project | Focus |
|---------|-------|
| Preventable Punchlisting Analysis | Root-cause analysis of operational failure in healtcare IT deployment workflows |
| Hospital Patient Experience Analytics *(this project)* | Performance monitoring and structured insight generation from national healthcare data |

Together they demonstrate a full analyst cycle:

**Diagnose operational breakdown → Build performance monitoring systems.**

---

## Author

Asim Bacchus
[LinkedIn](https://www.linkedin.com/in/asimbacchus/) | [GitHub](https://github.com/Asim-Bacchus)
