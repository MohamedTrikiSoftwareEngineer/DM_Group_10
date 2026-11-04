# ACDC Member Segmentation: Exploratory Data Analysis

Data Mining, NOVA IMS, 2026-27. Group 10, Delivery 1.

## Summary

Amazing Creative Desk Coworking (ACDC) wants to segment its members. This deliverable covers the exploratory stage, following CRISP-DM: we audit and clean the membership data (15,465 rows and 31 columns, 14,840 members after cleaning), explore it, build features and propose the groups to test in Deliverable 2. No clustering model is trained here.

## What is in this repository

| Path | Content |
|---|---|
| `notebooks/Group10_EDA_Code.ipynb` | The analysis, with all cells executed |
| `notebooks/acdc_dataset.csv` | The original dataset from Moodle, separated by `;` |
| `Discussion_Slides/Group10_EDA_Slides.pdf` | Discussion slides (`.pptx` version in the same folder) |
| `Group10_EDA_Bonus_Code/` | Bonus: interactive dashboard, with its own README and requirements |
| `requirements.txt`, `environment.yml` | The notebook environment, for pip and for conda |

The notebook has six sections:

1. Business Understanding
2. Data Understanding: raw data audit
3. Data Preparation: cleaning
4. Data Understanding: exploration of the cleaned data
5. Data Preparation: engineered features
6. Towards Modelling

## How to run the notebook

Clone the repository:

```bash
git clone https://github.com/MohamedTrikiSoftwareEngineer/DM_Group_10.git
cd DM_Group_10
```

Then create the environment with **one** of the two options below. Both use **Python 3.11** and install the same package versions.

**Option 1: conda** (installs Python 3.11 for you)

```bash
conda env create -f environment.yml
conda activate dt_mining
jupyter notebook notebooks/Group10_EDA_Code.ipynb
```

**Option 2: pip** (needs Python 3.11 already installed)

```bash
# Windows
py -3.11 -m venv dt_mining
dt_mining\Scripts\activate

# macOS / Linux
python3.11 -m venv dt_mining
source dt_mining/bin/activate

pip install -r requirements.txt
jupyter notebook notebooks/Group10_EDA_Code.ipynb
```

**Data file:** the notebook reads `acdc_dataset.csv` from its own folder. The repository already has it there. If you only downloaded the `.ipynb`, put the original `;`-separated CSV in the same folder, with that name.

## Bonus dashboard

Live version: https://group10-acdc-eda-dashboard.streamlit.app/

To run it locally, follow `Group10_EDA_Bonus_Code/README.md`.

## Team

Diogo Gaspar, Gustavo Carvalho and Mohamed Triki.

## AI usage statement

**Diogo** used Claude Code, connected to Deepnote through MCP, to brainstorm directions to explore, to investigate data problems in more depth and test conclusions against the data, and to write code to our specification, including reviewing and consolidating the group's earlier code into the final notebook. It was also used to understand each other's code, to organise our reasoning and conclusions into concise Markdown, to produce the slides from a plan the group had defined, and for version control and the READMEs.

**Gustavo** used ChatGPT, connected to Deepnote through MCP, to clarify doubts, to help identify and correct errors in the notebook code (mainly data visualization in seaborn and matplotlib, and syntax in pandas and numpy), and to review grammar and wording so the written explanations were clearer.

**Mohamed** used Qoder for coding help (pandas operations and matplotlib formatting), building the dashboard, brainstorming exploratory customer hypotheses, proofreading and repository work.

Overall, our contribution exceeded that of the AI tools. We used them to write code, check results and analyse large volumes of data faster, to structure our writing and to brainstorm. The group made the final decisions on what to explore, which conclusions to draw and what to include, and takes responsibility for the submitted work.
