# ACDC member explorer

Bonus for Deliverable 1 of Group 10: an interactive dashboard to explore the ACDC members. It applies the cleaning rules of the notebook and shows the same 14,840 members.

Live version: https://group10-acdc-eda-dashboard.streamlit.app/

## Run it locally

From this folder, with Python 3.11:

```bash
# Windows
py -3.11 -m venv venv
venv\Scripts\activate

# macOS / Linux
python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app reads the `acdc_dataset.csv` in this folder, so nothing else is needed.

## What it shows

The sidebar filters by plan, status, country, age and membership length. The page shows:

- KPIs for the selected members;
- a summary of the cleaning steps, with the number of rows affected by each;
- the distribution of a chosen attribute;
- lifetime value by plan;
- membership length against monthly value;
- a summary table and a drill-down table.

## Files

- `streamlit_app.py`: the dashboard and the cleaning rules;
- `requirements.txt`: the packages it needs;
- `acdc_dataset.csv`: the original `;`-separated dataset.
