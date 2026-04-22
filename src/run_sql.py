from pathlib import Path
import duckdb

DB_PATH = Path("db/hcahps.duckdb")
SQL_DIR = Path("sql")


def run_sql_files():
    if not SQL_DIR.exists():
        raise FileNotFoundError(f"Missing SQL directory: {SQL_DIR.resolve()}")

    con = duckdb.connect(str(DB_PATH))
    sql_files = sorted(SQL_DIR.glob("*.sql"))

    if not sql_files:
        raise ValueError("No SQL files found in sql/ directory.")

    print(f"📂 Running {len(sql_files)} SQL files...\n")

    for file in sql_files:
        print(f"▶ Running {file.name}")
        sql = file.read_text(encoding="utf-8")
        con.execute(sql)

    print("\n✅ All SQL files executed successfully.")

    # Show tables
    tables = con.execute("SHOW TABLES;").fetchall()
    print("\n📊 Tables in database:")
    for t in tables:
        print(f" - {t[0]}")

    # 🔍 Explore outputs
    print("\n📋 Star rating values:")
    print(
        con.execute(
            "SELECT DISTINCT star_rating FROM star_ratings_2024 ORDER BY star_rating"
        )
        .df()
        .to_string()
    )

    print("\n📋 Distinct measures:")
    print(
        con.execute(
            "SELECT DISTINCT question FROM star_ratings_2024"
        )
        .df()
        .to_string()
    
    
    )
    print("\n📋 Sample hospital KPIs:")
    print(con.execute("SELECT * FROM hospital_kpis_2024 LIMIT 5").df().to_string(index=False))

    print("\n📋 Null check (how many hospitals missing each KPI):")
    print(
        con.execute("""
        SELECT
        SUM(CASE WHEN nurse_comm_stars IS NULL THEN 1 ELSE 0 END) AS missing_nurse,
        SUM(CASE WHEN doctor_comm_stars IS NULL THEN 1 ELSE 0 END) AS missing_doctor,
        SUM(CASE WHEN staff_responsiveness_stars IS NULL THEN 1 ELSE 0 END) AS missing_staff_resp,
        SUM(CASE WHEN cleanliness_stars IS NULL THEN 1 ELSE 0 END) AS missing_clean,
        SUM(CASE WHEN recommend_stars IS NULL THEN 1 ELSE 0 END) AS missing_recommend,
        SUM(CASE WHEN overall_rating_stars IS NULL THEN 1 ELSE 0 END) AS missing_overall
        FROM hospital_kpis_2024;
        """).df().to_string(index=False)
    )

    print("\n📊 State Averages (Lowest Overall First):")
    print(
        con.execute("SELECT * FROM state_averages LIMIT 10")
        .df()
        .to_string(index=False)
    )
    print("\n📊 Correlation check:")
    print(con.execute("""
        SELECT 
            ROUND(CORR(staff_responsiveness_stars, overall_rating_stars), 3) AS staff_vs_overall,
            ROUND(CORR(nurse_comm_stars, overall_rating_stars), 3) AS nurse_vs_overall,
            ROUND(CORR(doctor_comm_stars, overall_rating_stars), 3) AS doctor_vs_overall,
            ROUND(CORR(cleanliness_stars, overall_rating_stars), 3) AS clean_vs_overall
        FROM hospital_kpis_2024
    """).df().to_string(index=False))
    print("\n📈 Nurse Communication Impact (Regression Slope):")
    print(con.execute("""
        SELECT
            ROUND(regr_slope(overall_rating_stars, nurse_comm_stars), 3) AS slope
        FROM hospital_kpis_2024
    """).df().to_string(index=False))
    print("\n📉 Bottom 10 States by Nurse Communication:")
    print(con.execute("""
        SELECT state,
            ROUND(AVG(nurse_comm_stars), 2) AS avg_nurse_comm
        FROM hospital_kpis_2024
        GROUP BY state
        ORDER BY avg_nurse_comm ASC
        LIMIT 10
    """).df().to_string(index=False))
    print("\n📊 Recommend vs Overall:")
    print(con.execute("""
        SELECT 
            ROUND(CORR(recommend_stars, overall_rating_stars), 3) AS recommend_vs_overall
        FROM hospital_kpis_2024
    """).df().to_string(index=False))
    print("\n📊 Nurse Sub-Dimension Correlations with Overall Rating:")
    print(con.execute("""
        SELECT
            ROUND(CORR(pct_always_respect, overall_star_rating), 3) AS r_respect_vs_overall,
            ROUND(CORR(pct_always_listen,  overall_star_rating), 3) AS r_listen_vs_overall,
            ROUND(CORR(pct_always_explain, overall_star_rating), 3) AS r_explain_vs_overall
        FROM nurse_comm_breakdown
    """).df().to_string(index=False))

    print("\n📊 National Averages by Sub-Dimension:")
    print(con.execute("""
        SELECT
            ROUND(AVG(pct_always_respect), 1) AS national_avg_respect,
            ROUND(AVG(pct_always_listen),  1) AS national_avg_listen,
            ROUND(AVG(pct_always_explain), 1) AS national_avg_explain
        FROM nurse_comm_breakdown
    """).df().to_string(index=False))

    print("\n📉 Bottom 10 States by Sub-Dimension (Respect):")
    print(con.execute("""
        SELECT state, ROUND(AVG(pct_always_respect), 2) AS avg_respect
        FROM nurse_comm_breakdown
        GROUP BY state HAVING COUNT(*) >= 20
        ORDER BY avg_respect ASC LIMIT 10
    """).df().to_string(index=False))

    print("\n📉 Bottom 10 States by Sub-Dimension (Listening):")
    print(con.execute("""
        SELECT state, ROUND(AVG(pct_always_listen), 2) AS avg_listen
        FROM nurse_comm_breakdown
        GROUP BY state HAVING COUNT(*) >= 20
        ORDER BY avg_listen ASC LIMIT 10
    """).df().to_string(index=False))

    print("\n📉 Bottom 10 States by Sub-Dimension (Explanation):")
    print(con.execute("""
        SELECT state, ROUND(AVG(pct_always_explain), 2) AS avg_explain
        FROM nurse_comm_breakdown
        GROUP BY state HAVING COUNT(*) >= 20
        ORDER BY avg_explain ASC LIMIT 10
    """).df().to_string(index=False))
    con.close()


if __name__ == "__main__":
    run_sql_files()