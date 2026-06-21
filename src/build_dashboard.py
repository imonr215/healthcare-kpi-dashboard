"""
build_dashboard.py

Reads the synthetic hospital-ops dataset and injects it (plus a couple of
precomputed correlation insights) into the HTML template, producing a
single self-contained index.html — no server, no build step, no external
data file needed at runtime. Just open it in a browser, or deploy via
GitHub Pages.

Run:
    python src/build_dashboard.py
Output:
    index.html
"""

import json

import pandas as pd

DATA_PATH = "data/hospital_ops_monthly.csv"
TEMPLATE_PATH = "templates/dashboard_template.html"
OUTPUT_PATH = "index.html"


def main():
    df = pd.read_csv(DATA_PATH)
    records = df.to_dict(orient="records")
    data_json = json.dumps(records, separators=(",", ":"))

    insights = {
        "occ_wait_corr": round(
            df["bed_occupancy_rate"].corr(df["ed_wait_time_minutes"]), 4
        ),
        "wait_satisfaction_corr": round(
            df["ed_wait_time_minutes"].corr(df["patient_satisfaction_score"]), 4
        ),
    }
    insights_json = json.dumps(insights)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("/*__DATA_JSON__*/", data_json)
    html = html.replace("/*__INSIGHTS_JSON__*/", insights_json)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {OUTPUT_PATH} ({len(html):,} bytes, {len(records)} data rows)")


if __name__ == "__main__":
    main()
