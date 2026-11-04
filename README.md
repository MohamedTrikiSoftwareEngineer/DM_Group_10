# github repo link

https://github.com/MohamedTrikiSoftwareEngineer/DM_Group_10

# ACDC Coworking EDA: Group 10

Data Mining, NOVA IMS, Fall 2026-2027 | Deliverable 1, due 4 November 2026

This deliverable explores the ACDC membership data, assesses its quality, engineers features and proposes customer groups to test in Deliverable 2. No clustering model is trained here.

## Graded files

- [Jupyter notebook](notebooks/Group10_EDA_Code.ipynb): full analysis, with all cells executed and figures shown inline.
- [Discussion slides](Discussion_Slides/Group10_EDA_Slides.pdf): a cover and five content slides with the main findings.
- [Bonus dashboard](Group10_EDA_Bonus_Code/README.md): the interactive EDA explorer, live at https://group10-acdc-eda-dashboard.streamlit.app/.

The raw course extract is in `data/raw/`, so the notebook runs without any download.

## Running the notebook

Set up the environment with either pip or conda.

**pip**

```bash
python -m venv dt_mining

# Windows
dt_mining\Scripts\activate

# macOS / Linux
source dt_mining/bin/activate

pip install -r requirements.txt
jupyter notebook notebooks/Group10_EDA_Code.ipynb
```

**conda**

```bash
conda env create -f environment.yml
conda activate dt_mining
jupyter notebook notebooks/Group10_EDA_Code.ipynb
```

Then select **Restart & Run All**. The notebook only reads the raw extract and writes no files. It looks for `acdc_dataset.csv` next to itself, then in `data/raw/`, then in `../data/raw/`, so it also runs from a copied folder.

## Notebook contents

1. Setup: versions, palette and variable documentation
2. Data understanding: shape, types and first statistics
3. Data-quality assessment: duplicates, missing values, types, contradictions, implausible values and heavy tails
4. Data-quality handling: documented decisions, one flag per rule and a quality log
5. Univariate analysis: distributions, spread and category frequencies
6. Relationships: value vs. usage, plan vs. status and within-group correlations
7. Time trends and add-ons: joins, leaves, cohorts, add-on consistency and co-usage, and the missingness pattern
8. Feature engineering: base derivations and engineered features, each justified
9. Engineered feature patterns: distributions, correlations and a redundancy test
10. Anomaly screening: a single labelled diagnostic, with members flagged but not removed
11. Clustering-reliability risks: a register measured in members and ranked by impact
12. Behavioural signals and group hypotheses: six candidate groups and the rule for the expected cluster count
13. Conclusion: answers to the brief's four questions and the hand-over to Deliverable 2

Valid extreme values are kept. The anomaly score is used to report and compare members, not to delete or cap them. The notebook runs no clustering, dimensionality reduction or train/test split.

## Team

- Gustavo Carvalho
- Diogo Gaspar
- Mohamed Triki

## AI usage statement

In line with the course guidelines, this statement is also disclosed on the notebook cover. ChatGPT and Claude were used for coding syntax help (pandas operations and matplotlib formatting), for brainstorming exploratory customer hypotheses and for proofreading text descriptions. All analytical insights, cleaning decisions and business interpretations are the group's own work.

## Group branches

Machine Learning homework (Everything & Then Some, repeat purchase prediction).

| Branch | Owner |
|---|---|
| `gustavo` | Gustavo |
| `Diogo` | Diogo |
| `vasco` | Vasco |
| `mohamed` | Mohamed |
