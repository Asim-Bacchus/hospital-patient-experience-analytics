from pathlib import Path
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = Path("db/hcahps.duckdb")
FIG_DIR = Path("dashboard/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

def savefig(name: str):
    path = FIG_DIR / name
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"✅ Saved {path}")

def main():
    con = duckdb.connect(str(DB_PATH))

    # 1) Correlations bar chart
    corr_df = con.execute("""
        SELECT
          'Nurse communication' AS kpi, CORR(nurse_comm_stars, overall_rating_stars) AS corr FROM hospital_kpis_2024
        UNION ALL SELECT
          'Doctor communication', CORR(doctor_comm_stars, overall_rating_stars) FROM hospital_kpis_2024
        UNION ALL SELECT
          'Staff responsiveness', CORR(staff_responsiveness_stars, overall_rating_stars) FROM hospital_kpis_2024
        UNION ALL SELECT
          'Cleanliness', CORR(cleanliness_stars, overall_rating_stars) FROM hospital_kpis_2024
        UNION ALL SELECT
          'Recommend hospital', CORR(recommend_stars, overall_rating_stars) FROM hospital_kpis_2024
        ORDER BY corr DESC;
    """).df()

    plt.figure()
    plt.bar(corr_df["kpi"], corr_df["corr"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Correlation with Overall Rating")
    plt.title("Which KPIs Track Most with Overall Hospital Rating?")
    savefig("01_correlations_with_overall.png")

    # 2) Bottom 10 states by overall rating (min hospital_count to avoid tiny samples)
    bottom_states_df = con.execute("""
        SELECT
          state,
          COUNT(*) AS hospital_count,
          AVG(overall_rating_stars) AS avg_overall
        FROM hospital_kpis_2024
        GROUP BY state
        HAVING COUNT(*) >= 20
        ORDER BY avg_overall ASC
        LIMIT 10;
    """).df()

    plt.figure()
    plt.bar(bottom_states_df["state"], bottom_states_df["avg_overall"])
    plt.ylabel("Average Overall Rating")
    plt.title("Bottom 10 States by Overall Rating (States with ≥20 Hospitals)")
    savefig("02_bottom_states_overall.png")

    # 3) Bottom 10 states by nurse communication (min hospital_count)
    bottom_nurse_df = con.execute("""
        SELECT
          state,
          COUNT(*) AS hospital_count,
          AVG(nurse_comm_stars) AS avg_nurse
        FROM hospital_kpis_2024
        GROUP BY state
        HAVING COUNT(*) >= 20
        ORDER BY avg_nurse ASC
        LIMIT 10;
    """).df()

    plt.figure()
    plt.bar(bottom_nurse_df["state"], bottom_nurse_df["avg_nurse"])
    plt.ylabel("Average Nurse Communication Stars")
    plt.title("Bottom 10 States by Nurse Communication (States with ≥20 Hospitals)")
    savefig("03_bottom_states_nurse_comm.png")

    # 4) Scatter: nurse communication vs overall rating + slope annotation
    scatter_df = con.execute("""
        SELECT nurse_comm_stars, overall_rating_stars
        FROM hospital_kpis_2024;
    """).df()

    slope = con.execute("""
        SELECT regr_slope(overall_rating_stars, nurse_comm_stars)
        FROM hospital_kpis_2024;
    """).fetchone()[0]

    plt.figure()
    plt.scatter(scatter_df["nurse_comm_stars"], scatter_df["overall_rating_stars"], alpha=0.15)
    plt.xlabel("Nurse Communication (Stars)")
    plt.ylabel("Overall Hospital Rating (Stars)")
    plt.title(f"Nurse Communication vs Overall Rating (Slope ≈ {slope:.3f})")
    savefig("04_scatter_nurse_vs_overall.png")

    con.close()

if __name__ == "__main__":
    main()