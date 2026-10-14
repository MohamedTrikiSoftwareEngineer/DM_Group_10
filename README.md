# ACDC Coworking — Customer Segmentation (Group 10, Deliverable 1)

**Course**: Data Mining, NOVA IMS, Fall 2026-2027
**Group**: 10
**Deliverable**: 1 — Exploratory Data Analysis, due 4 November 2026
**Business case**: Amazing Creative Desk Coworking (ACDC) customer segmentation

This deliverable audits, cleans and explores the ACDC member data, engineers 12 features from it and
states hypotheses about customer groups. **No clustering model is trained here** — that is Deliverable 2.
The notebook is the single source of truth: every figure, every number and every cleaning decision in the
slide deck is produced by running it.

---

## What the repository contains

```
notebooks/Group10_EDA_Code.ipynb           147 cells (99 code, 48 markdown), 29 figures, 0 errors   — 5 pts
Discussion_Slides/Group10_EDA_Slides.pdf   a cover plus 5 slides, 16:9, no speaker notes          — 15 pts
data/raw/acdc_dataset.csv                    the course extract, committed — 15,465 rows x 31 columns
data/raw/README.md                           what the extract is, and how it must be read
requirements.txt                           pinned runtime dependencies — the pip route
environment.yml                            the same pins as a conda environment — the conda route
```

---

## Running the analysis from a fresh clone

**1. Create the environment.** Two routes, one pinned stack — Python 3.11 with the versions that produced
these outputs, so either choice reproduces the analysis.

**A. Conda** — from `environment.yml`:

```bash
conda env create -f environment.yml
conda activate dt_mining
python -m ipykernel install --user --name dt_mining --display-name "Python (dt_mining)"
```

**B. pip + venv** — from `requirements.txt`:

```bash
python -m venv dt_mining

# Windows (PowerShell)
.\dt_mining\Scripts\Activate.ps1
# macOS / Linux
source dt_mining/bin/activate

pip install -r requirements.txt
python -m ipykernel install --user --name dt_mining --display-name "Python (dt_mining)"
```

`environment.yml` deliberately pins the analysis packages through a `pip:` block rather than conda
packages, so both routes resolve the same versions and conda-forge is not relied on to mirror every PyPI
release.

**2. The dataset is already in the repository.** `data/raw/acdc_dataset.csv` is the course extract — 15,465 rows,
31 columns, semicolon-separated — committed so a clone runs with no setup step beyond the environment.
`data/raw/README.md` describes it and stays course-provided material rather than the group's to redistribute
further.

**3. Run the notebook end to top.** Open `notebooks/Group10_EDA_Code.ipynb`, select the kernel
**Python (dt_mining)**, then *Run > Run All*. The notebook creates its own output folders; nothing outside the
repository is needed and no internet access is required. Figures are displayed inline only; nothing is
saved as an image file. The notebook writes two data files:

| Output | Contents |
|---|---|
| `data/processed/acdc_cleaned.csv` | 15,450 rows x 103 columns: 31 original + 52 flag columns + 12 engineered features + 8 derived |
| `data/processed/results.json` | every number quoted anywhere in the deliverable |

A full run takes a few minutes. The committed notebook already carries the executed outputs, so reading it
needs no setup at all.

---

## What the analysis found

All figures below are computed inside the notebook and re-derivable from `data/processed/acdc_cleaned.csv`.

- **15,465 records received, 15,450 after cleaning.** Duplicates and structurally impossible rows were removed
  only where the evidence supported it; every removal is recorded.
- **`plan_days` of 0 and 9 are kept and flagged, not deleted** (43 and 54 rows). They are a data-quality signal,
  not noise, and clustering in Deliverable 2 must decide whether to trust them.
- **Country is missing for 429 members** and is left missing rather than imputed, because the gap is informative
  about the channel the member arrived through.
- **Lifetime value is extremely heavy-tailed**: median EUR 1,667.76 against a mean of EUR 7,339.91 and a P99 of
  EUR 26,125.39. The top 1% of members account for 45.83% of total recorded value.
- **Zero-LTV is not one phenomenon**: 1,742 members have zero LTV, of whom 180 hold dedicated desks and 83 private
  offices — a contracted desk that records no usage behaves differently from an unused hot desk.
- **A multidimensional anomaly view** (row-normalised distance to the median profile, combined with 1.5 IQR fences)
  isolates 155 members who carry 21.07% of revenue, and 36.77% of them are still active.
- **Retention risk concentrates by tier**: `hot_desk` is the least retained tier at 13.35%, which is the hypothesis
  Deliverable 2 should test rather than assume.

---

## Method and conventions

Only techniques taught in the course are used: `pandas`, `numpy`, `matplotlib` (object-oriented style), `seaborn`
and `scipy.spatial.distance.cdist`. No modelling library is imported, because no model is trained in this
deliverable.

Every cleaning rule follows the same shape — **evidence, decision, fix, `flag_*` column** — so nothing is silently
changed and the marker can audit each decision against the raw file. The 74% figure for ended memberships is a
**cumulative status share across the three-year window, not an annual churn rate**; the deck says so
explicitly because the two readings imply different segmentations.

Paths are relative (`os.path.join`), the notebook runs from `notebooks/`, and imports stay in the first code cell.

---

## Team

| Member | Student number |
|---|---|
| Gustavo Carvalho | `[student number]` |
| Diogo Gaspar | `[student number]` |
| Mohamed Triki | `[student number]` |
| Vasco Vaz | `[student number]` |

## AI usage statement

AI usage statement: [TO BE COMPLETED BY THE GROUP: tools used, tasks, how outputs were verified]

All analysis, interpretations and recommendations in this deliverable are the group's own.
