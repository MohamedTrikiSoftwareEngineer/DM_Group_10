# ACDC member explorer

Interactive EDA dashboard for Deliverable 1, Option 3.

## Run it

Install the packages, then run the app from this folder:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The dashboard reads `acdc_dataset.csv` from the same folder.

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
