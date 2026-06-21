# Hospital Operations KPI Dashboard

An interactive, single-page dashboard tracking core operational KPIs across
six hospital departments — built to demonstrate dashboard design and data
storytelling for non-technical stakeholders (the same skill applied in a
Tableau/Power BI context, here built as a dependency-light web app instead).

> **Note on data:** the dataset is **synthetic**, generated to reflect how
> real hospital operations data behaves — metrics are related to one another
> (e.g. rising bed occupancy drives longer wait times, which drags down
> satisfaction) rather than independently randomized. No real patient or
> hospital data is used. Generation logic is in
> [`src/generate_data.py`](src/generate_data.py).

**[Live demo →](#deploying-a-live-link)**
https://imonr215.github.io/healthcare-kpi-dashboard/

## What it shows

- **6 KPI cards** — admissions, length of stay, 30-day readmission rate, bed
  occupancy, ED wait time, patient satisfaction — each with a status color,
  a vs.-prior-month delta, and a 6-month sparkline
- **Department filter** — click a department to re-scope every chart and KPI
  card to that department, with the hospital-wide trend shown as a faint
  reference line for comparison
- **Trend chart** — any KPI, over all 24 months, switchable via dropdown
- **Department comparison** — the same KPI, side-by-side across departments,
  for the latest month
- **An actual insight, not just charts** — a scatter plot of occupancy vs.
  wait time with the computed correlation, calling out *why* satisfaction
  moves the way it does (capacity strain, not bedside care quality, is the
  biggest lever in this dataset)

Built with vanilla JS + [Chart.js](https://www.chartjs.org/) — no framework,
no build step, no backend. It's one HTML file.

## Repo structure

```
.
├── data/
│   └── hospital_ops_monthly.csv     # generated dataset (144 rows)
├── src/
│   ├── generate_data.py             # synthetic data generation
│   └── build_dashboard.py           # injects data into the HTML template
├── templates/
│   └── dashboard_template.html      # the dashboard, with a data placeholder
├── index.html                       # generated — open this, or deploy it
├── run_all.py                       # regenerates data + rebuilds index.html
└── requirements.txt
```

## How to run

```bash
pip install -r requirements.txt
python run_all.py
open index.html        # macOS; on Windows/Linux just double-click it
```

The dataset is seeded, so this is fully reproducible.

## Why a web dashboard instead of Tableau/Power BI

Tableau and Power BI are point-and-click tools — they don't produce a file
that's natural to host in a code portfolio, and a static export loses the
interactivity that's the whole point of a KPI dashboard. Building the same
KPI-card-plus-drilldown pattern as a small, dependency-light web app shows
the same dashboard-design and stakeholder-communication thinking, plus
front-end and data-pipeline skills Tableau/Power BI alone don't demonstrate.
The underlying CSV is plain and tidy, so it would also drop into either tool
directly if you wanted a literal Tableau/Power BI version alongside this one.

## Tech stack

Python (data generation) · vanilla JavaScript · Chart.js · HTML/CSS
