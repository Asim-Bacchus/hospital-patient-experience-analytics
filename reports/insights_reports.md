# Hospital Patient Experience Analytics (HCAHPS, 2024)

## Executive Summary
Using CMS HCAHPS hospital survey data (2024), I built a reproducible SQL + DuckDB pipeline to produce a clean hospital-level KPI dataset (1–5 star ratings). The analysis shows that **interpersonal care metrics**—especially **nurse communication**—track most strongly with overall patient satisfaction.

## Dataset
- Source: CMS HCAHPS Patient Survey (Hospital)
- Processed output: `data/processed/hospital_kpis_2024.csv`
- Unit of analysis: one row per hospital

## KPIs Used
- Nurse communication (stars)
- Doctor communication (stars)
- Staff responsiveness (stars)
- Cleanliness (stars)
- Recommend hospital (stars)
- Overall hospital rating (stars)

## Key Findings (National)
**Correlation with overall hospital rating:**
- Recommend hospital: **0.862** (outcome-adjacent)
- Nurse communication: **0.792** (strongest operational metric)
- Doctor communication: **0.734**
- Staff responsiveness: **0.726**
- Cleanliness: **0.597**

**Estimated impact (simple linear regression slope):**
- A **1-star increase in nurse communication** is associated with an estimated **+0.684 stars** in overall hospital rating (on average).

## State-Level Pattern
State averages show consistent underperformance in nurse communication among states that also rank low on overall rating.
Among larger-sample states, low nurse communication and low overall ratings frequently co-occur (e.g., **NJ, NY, FL**), suggesting a statewide pattern in patient-facing experience.

See figures:
- `dashboard/figures/02_bottom_states_overall.png`
- `dashboard/figures/03_bottom_states_nurse_comm.png`

## Visuals
- Correlations: `dashboard/figures/01_correlations_with_overall.png`
- Bottom states (overall): `dashboard/figures/02_bottom_states_overall.png`
- Bottom states (nurse comm): `dashboard/figures/03_bottom_states_nurse_comm.png`
- Scatter (nurse vs overall): `dashboard/figures/04_scatter_nurse_vs_overall.png`

## Methodology (Brief)
1. Filter raw HCAHPS dataset to star rating measures (2024)
2. Remove “Not Available”
3. Pivot long-format measures into a wide hospital KPI table
4. Compute state averages and national relationships (correlation + regression slope)

## Limitations
- Correlation/regression here are **associational** (not causal).
- Ratings are discrete (1–5) and may compress variance.
- State comparisons can be influenced by hospital mix and reporting differences.

## Recommendations (Operational Interpretation)
If a hospital system is prioritizing patient experience improvements, the analysis suggests that **frontline communication quality**, particularly nurse communication, is a high-leverage area relative to physical environment measures like cleanliness.

## Reproducibility
- SQL pipeline: `sql/`
- Execution: `python src/run_sql.py`
- Figures: `python src/make_figures.py`