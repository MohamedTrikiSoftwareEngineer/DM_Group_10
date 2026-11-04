# Raw dataset

```
data/raw/acdc_dataset.csv    15,465 rows x 31 columns, 2.7 MB
```

The course extract is committed here so that a fresh clone runs the notebook end to end with no
manual setup step.

- **Source:** course-provided ACDC member extract (the sample dataset referenced in the project
  guidelines), supplied to Group 10 for Deliverable 1.
- **Format:** semicolon-separated CSV, 31 columns, one row per membership record. The notebook reads
  it with `sep=";"` — a comma read produces a single-column frame, which is the most common way this
  file is mis-loaded.
- **As received:** 15,465 rows. The notebook reduces this to 15,450 and records every removal and every
  flag in `data/processed/acdc_cleaned.csv`.
- **Distribution:** committed with the group's decision so the analysis is reproducible for the marker.
  It remains course-provided material, not the group's data to redistribute further; if the instructors
  ask for it to be removed, deleting the file and re-running the notebook is enough.
