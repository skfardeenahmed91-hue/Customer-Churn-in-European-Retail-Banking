# European Bank — Customer Churn Analytics Dashboard

An interactive Streamlit companion to the *Customer Churn Analytics in European
Retail Banking* research paper. It lets stakeholders explore every finding in
the report against live, filterable data instead of static charts.

## What's included

- `app.py` — the Streamlit application (single file, ~490 lines)
- `cleaned_segmented.csv` — the cleaned, validated, segmentation-enriched dataset
  the app reads (10,000 customers; see the research paper, Section 5, for how
  it was built)
- `requirements.txt` — pinned Python dependencies

## Running it locally

```bash
# 1. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app (run this from inside the streamlit_app folder,
#    so app.py can find cleaned_segmented.csv alongside it)
streamlit run app.py
```

Streamlit will open the dashboard automatically in your default browser at
`http://localhost:8501`. If it doesn't, open that address manually.

## Using the dashboard

The sidebar holds nine filters — Geography, Gender, Age Group, Credit Score
Band, Tenure Group, Balance Segment, Number of Products, Activity Status, and
Customer Tier. Every KPI, chart, and table on all four tabs recalculates
live as filters change, so you can, for example, isolate Germany alone to
reproduce the 32.44% market-level churn rate reported in Section 6.2 of the
research paper, or isolate the 46–60 age band within Germany to reproduce the
67.33% figure discussed in Section 6.5.

**Tabs (Core Modules):**

1. **Overall Churn Summary** — headline KPIs, churn composition, and a
   configurable segment-comparison chart and table.
2. **Geography Explorer** — churn rate and Geographic Risk Index by market,
   the Geography × Age heatmap, and the gender gap by market.
3. **Age & Tenure Comparison** — churn by age group and tenure group, an
   Age × Tenure heatmap, the product-holding "churn cliff," and the
   engagement drop indicator.
4. **High-Value Customer Explorer** — premium-segment KPIs, revenue-at-risk
   figures, the balance-vs-salary signal comparison, and a downloadable,
   filtered high-value customer list.

## Deploying it for stakeholders

For a shareable, always-on link rather than a local session, deploy the
`streamlit_app/` folder as-is to
[Streamlit Community Cloud](https://streamlit.io/cloud) (free for public
repos), or to any platform that runs a standard Streamlit app (e.g. an
internal server, Azure App Service, or a Docker container built from this
folder). No code changes are required — `app.py` reads its data from the
relative path `cleaned_segmented.csv`, so keep both files together.

## Data note

`cleaned_segmented.csv` contains no personally identifying information beyond
a numeric `CustomerId`; the `Surname` field present in the original source
extract was dropped during data preparation (see research paper, Section
5.2) and is not included here.
