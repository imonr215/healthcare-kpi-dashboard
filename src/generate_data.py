"""
generate_data.py

Generates a synthetic, monthly hospital-operations dataset across six
departments over a 24-month period. Metrics are deliberately *related* to
one another the way real operational data is (e.g. rising occupancy drives
longer wait times, which drags down satisfaction) rather than independently
randomized, so the dashboard built on top of it tells a coherent story.

Run:
    python src/generate_data.py
Output:
    data/hospital_ops_monthly.csv
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 7
N_MONTHS = 24
START = "2024-01"

DEPARTMENTS = {
    # name: (base_admissions, los_base, readmit_base, occ_base, satisfaction_base,
    #        seasonal_amplitude, winter_seasonality)
    "Emergency":  dict(adm=860, los=1.8, readmit=0.09, occ=82, sat=78, amp=0.22, winter=True),
    "Cardiology": dict(adm=210, los=4.6, readmit=0.21, occ=88, sat=82, amp=0.08, winter=True),
    "Surgery":    dict(adm=260, los=3.4, readmit=0.13, occ=85, sat=84, amp=0.05, winter=False),
    "Oncology":   dict(adm=140, los=5.8, readmit=0.20, occ=83, sat=79, amp=0.03, winter=False),
    "Pediatrics": dict(adm=190, los=2.3, readmit=0.08, occ=74, sat=88, amp=0.35, winter=True),
    "ICU":        dict(adm=95,  los=7.2, readmit=0.15, occ=91, sat=76, amp=0.10, winter=True),
}


def generate(n_months: int = N_MONTHS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    months = pd.period_range(START, periods=n_months, freq="M")
    rows = []

    # Hospital-wide capacity strain trend: occupancy drifts up over the
    # two-year window (a realistic "demand is outpacing capacity" arc).
    occ_trend = np.linspace(0, 9, n_months)

    for dept, p in DEPARTMENTS.items():
        for i, month in enumerate(months):
            month_of_year = month.month
            # Winter seasonality peaks in Dec/Jan/Feb for flu-sensitive depts
            seasonal = (
                np.cos((month_of_year - 1) / 12 * 2 * np.pi) if p["winter"] else 0.0
            )

            admissions = max(
                5,
                round(
                    p["adm"] * (1 + p["amp"] * seasonal)
                    + rng.normal(0, p["adm"] * 0.05)
                ),
            )
            discharges = max(5, round(admissions * rng.uniform(0.93, 1.03)))

            los = max(
                0.5,
                p["los"] + 0.3 * seasonal * (1 if p["winter"] else 0) + rng.normal(0, 0.25),
            )

            readmit_rate = np.clip(
                p["readmit"] + 0.01 * (i / n_months) + rng.normal(0, 0.012), 0.03, 0.35
            )

            occupancy = np.clip(
                p["occ"] + occ_trend[i] + 4 * p["amp"] * seasonal + rng.normal(0, 1.8),
                55,
                108,
            )

            # Wait time is driven mainly by occupancy strain, with a
            # department-specific baseline (ED runs highest by nature)
            wait_baseline = 48 if dept == "Emergency" else 18
            wait_time = max(
                4,
                wait_baseline
                + 1.6 * max(0, occupancy - 80)
                + rng.normal(0, 4.5),
            )

            satisfaction = np.clip(
                p["sat"]
                - 0.18 * max(0, wait_time - 25)
                - 0.25 * max(0, occupancy - 88)
                + rng.normal(0, 2.2),
                35,
                99,
            )

            rows.append(
                {
                    "month": str(month),
                    "department": dept,
                    "admissions": int(admissions),
                    "discharges": int(discharges),
                    "avg_los_days": round(los, 2),
                    "readmission_rate_30d": round(readmit_rate, 4),
                    "bed_occupancy_rate": round(occupancy, 1),
                    "ed_wait_time_minutes": round(wait_time, 1),
                    "patient_satisfaction_score": round(satisfaction, 1),
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate()
    df.to_csv("data/hospital_ops_monthly.csv", index=False)
    print(f"Wrote {len(df)} rows to data/hospital_ops_monthly.csv")
    print(df.head(8))
    print("\nCorrelation, occupancy vs wait time:",
          round(df["bed_occupancy_rate"].corr(df["ed_wait_time_minutes"]), 3))
    print("Correlation, wait time vs satisfaction:",
          round(df["ed_wait_time_minutes"].corr(df["patient_satisfaction_score"]), 3))
