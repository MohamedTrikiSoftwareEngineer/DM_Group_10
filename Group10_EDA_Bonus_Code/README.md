
# deployed website link:

https://group10-acdc-eda-dashboard.streamlit.app/

# ACDC member explorer

Interactive EDA dashboard for Deliverable 1, Option 3.

## Run it

Install the packages, then start the app:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Both commands work from this folder or from the repository root, using
`streamlit run Group10_EDA_Bonus_Code/streamlit_app.py`. The app always reads
the copy of `acdc_dataset.csv` that sits next to it, so the folder can be moved
or zipped and still run.

## Deploy it

On Streamlit Community Cloud, connect this repository and set the three app
fields to:

- branch: `Mohamed`;
- app entry point: `Group10_EDA_Bonus_Code/streamlit_app.py`;
- Python requirements file: `Group10_EDA_Bonus_Code/requirements.txt`.

The requirements file at the repository root is for the notebook and does not
install Streamlit, so it must not be used here. No API keys or secrets are
needed, the app makes no network calls, and it never writes to the data.

## Cleaning

The app applies the notebook cleaning rules:

- remove repeated member IDs and identical rows;
- standardise gender, country, industry and plan labels;
- infer missing Private Office plans where 7 days per week is present;
- parse ISO and day-first dates;
- remove rows with date conflicts;
- create `membership_months`;
- handle invalid ages, placeholder colleague counts and invalid plan days;
- handle negative counts, the 999 recency code and unused service fields;
- convert lifetime value, handle implausible zeros and apply the scale-error hypothesis;
- create the engineered features.

The Cleaning applied section lists each step and the number of affected rows.

## Features

The dashboard uses these dataset names:

- `membership_months`;
- `plan_usage_rate`;
- `number_of_addons_used`;
- `monthly_value`;
- `days_since_last_visit_active`;
- `plan_tier_ordinal`.

## Exploration

The sidebar filters by plan, status, country, age and membership length.

The page provides:

- KPIs for the selected members;
- a cleaning summary;
- a distribution chart for one selected attribute;
- lifetime value by plan;
- membership length against monthly value;
- a log1p view beside the monthly value chart to reduce the visual effect of extreme values;
- a summary table;
- a drill-down table.

In the distribution chart each bin is edged in white so the bars stay apart. Count-like attributes get one bar per value, and attributes with a long tail get a second log1p histogram so the bulk of the members is still visible.

The drill-down follows the sidebar filters and can be narrowed further by plan, status, country, industry and gender. Stakeholders can also choose the number of rows to show.

## Files

- `streamlit_app.py`: the Streamlit dashboard and notebook cleaning rules;
- `requirements.txt`: packages needed to run it;
- `acdc_dataset.csv`: the semicolon-separated ACDC data.
