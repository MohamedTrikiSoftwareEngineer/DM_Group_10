"""Interactive EDA dashboard for the ACDC member data.

The dashboard applies the notebook cleaning and feature engineering, then gives
stakeholders basic filters, distribution charts and a member drill-down.

Run it with either of these:
    streamlit run Group10_EDA_Bonus_Code/streamlit_app.py    from the repository root
    streamlit run streamlit_app.py                           from this folder
"""
import pathlib

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_FILE = pathlib.Path(__file__).resolve().parent / "acdc_dataset.csv"
DAYS_PER_MONTH = 365.25 / 12
NO_END_DATE = pd.Timestamp("1970-01-01")
FALLBACK_REFERENCE_DATE = pd.Timestamp("2024-01-01")
SCALE_RATIO_THRESHOLD = 50

CHART_COLOR = "#0F7B6C"  # teal reads better on white than the default plotly blue
CHART_EDGE_COLOR = "#FFFFFF"  # thin lines that keep the histogram bins apart
PANEL_COLOR = "#F4F6F7"  # light panel so the white bin edges stay visible
GRID_COLOR = "#DCE3E5"  # gridlines dark enough to follow on the light panel
ACTIVE_COLOR = "#2E7D32"  # green for active members
ENDED_COLOR = "#C62828"  # red for ended members
STATUS_COLORS = {"Active": ACTIVE_COLOR, "Ended": ENDED_COLOR}
HISTOGRAM_BINS = 20
DISCRETE_VALUE_LIMIT = 15  # attributes with few distinct values get one bar per value
SKEW_THRESHOLD = 2.0  # very right-skewed attributes also get a log1p view

TIER_ORDER = ["hot_desk", "flex", "dedicated_desk", "full_time", "private_office"]
PLAN_LABELS = {
    "hot_desk": "Hot Desk",
    "flex": "Flex",
    "dedicated_desk": "Dedicated Desk",
    "full_time": "Full Time",
    "private_office": "Private Office",
}
PLAN_MAP = {
    "flex": "flex",
    "hot_desk": "hot_desk",
    "hotdesk": "hot_desk",
    "dedicated_desk": "dedicated_desk",
    "dedicateddesk": "dedicated_desk",
    "full_time": "full_time",
    "fulltime": "full_time",
    "private_office": "private_office",
    "privateoffice": "private_office",
}
GENDER_MAP = {
    "female": "Female",
    "f": "Female",
    "male": "Male",
    "m": "Male",
    "other": "Other",
    "o": "Other",
}
COUNTRY_MAP = {
    "portugal": "Portugal",
    "pt": "Portugal",
    "portucal": "Portugal",
    "germany": "Germany",
    "de": "Germany",
    "deutschland": "Germany",
    "united kingdom": "United Kingdom",
    "uk": "United Kingdom",
    "gb": "United Kingdom",
    "u.k.": "United Kingdom",
    "spain": "Spain",
    "es": "Spain",
    "españa": "Spain",
    "espana": "Spain",
    "france": "France",
    "fr": "France",
    "netherlands": "Netherlands",
    "the netherlands": "Netherlands",
    "nl": "Netherlands",
    "holland": "Netherlands",
    "ireland": "Ireland",
    "ie": "Ireland",
    "other (europe)": "Other (Europe)",
}
INDUSTRY_MAP = {
    "information technology": "Information Technology",
    "it": "Information Technology",
    "tech": "Information Technology",
    "consulting": "Consulting",
    "design & creative": "Design & Creative",
    "design/creative": "Design & Creative",
    "design and creative": "Design & Creative",
    "marketing & pr": "Marketing & PR",
    "marketing/pr": "Marketing & PR",
    "marketing and pr": "Marketing & PR",
    "finance": "Finance",
    "legal": "Legal",
    "education": "Education",
    "health": "Health",
    "real estate": "Real Estate",
    "realestate": "Real Estate",
    "real-estate": "Real Estate",
    "unknown": "Unknown",
    "other": "Other",
}
DATE_COLS = ["membership_start", "membership_end", "last_badge_swipe"]
NUMERIC_INPUTS = [
    "age", "n_colleagues_on_account", "plan_days_per_week", "days_since_last_visit",
    "total_visits", "avg_weekly_visits", "entitled_visits_last_period",
    "actual_visits_last_period", "meeting_room_hours", "event_space_hours",
    "guest_passes_issued", "n_renewals",
]
COUNT_COLUMNS = [
    "total_visits", "avg_weekly_visits", "entitled_visits_last_period",
    "actual_visits_last_period", "meeting_room_hours", "event_space_hours",
    "guest_passes_issued", "n_renewals",
]
USAGE_PAIRS = [
    ("uses_meeting_rooms", "meeting_room_hours"),
    ("uses_event_space", "event_space_hours"),
    ("uses_guest_passes", "guest_passes_issued"),
]
VARIABLE_LABELS = {
    "age": "Age",
    "membership_months": "Membership length, months",
    "total_visits": "Total visits",
    "avg_weekly_visits": "Average weekly visits",
    "days_since_last_visit": "Days since last visit",
    "plan_usage_rate": "Plan allowance used",
    "number_of_addons_used": "Number of add-ons used",
    "monthly_value": "Monthly value, EUR",
    "lifetime_value": "Lifetime value, EUR",
}
MEMBER_LABELS = {
    "member_id": "Member ID",
    "age": "Age",
    "membership_months": "Membership length, months",
    "total_visits": "Total visits",
    "avg_weekly_visits": "Average weekly visits",
    "plan_usage_rate": "Plan allowance used",
    "number_of_addons_used": "Number of add-ons used",
    "monthly_value": "Monthly value, EUR",
    "lifetime_value": "Lifetime value, EUR",
    "days_since_last_visit": "Days since last visit",
    "days_since_last_visit_active": "Days since last visit, active members",
    "plan_tier_ordinal": "Plan level, 1 to 5",
}
DEFAULT_DRILL_COLUMNS = [
    "member_id", "Plan", "Status", "Gender", "Country", "age",
    "membership_months", "total_visits", "plan_usage_rate",
    "number_of_addons_used", "monthly_value", "lifetime_value",
]


def parse_mixed_dates(series):
    text = series.astype("string").str.strip()
    is_day_first = text.str.contains("/", regex=False).fillna(False)
    parsed = pd.Series(pd.NaT, index=text.index, dtype="datetime64[ns]")
    parsed.loc[~is_day_first] = pd.to_datetime(text[~is_day_first], format="%Y-%m-%d", errors="coerce")
    parsed.loc[is_day_first] = pd.to_datetime(text[is_day_first], format="%d/%m/%Y", errors="coerce")
    return parsed


def parse_ltv(series):
    text = series.astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(text, errors="coerce")


def to_bool(series):
    return series.astype(str).str.strip().str.lower().isin(["true", "1", "yes", "y"])


def standardise(series, mapping, replace_spaces=False):
    values = series.astype("string").str.strip().str.lower()
    if replace_spaces:
        values = values.str.replace(" ", "_")
    return values.map(mapping)


def clean_data(raw):
    log = []

    def add_log(step, action, rows_left, affected):
        log.append({
            "Step": step,
            "What was done": action,
            "Rows affected": int(affected),
            "Rows left": int(rows_left),
        })

    add_log("Raw file", f"Loaded {len(raw)} rows and {raw.shape[1]} columns.", len(raw), len(raw))

    raw_dates = raw[DATE_COLS].apply(parse_mixed_dates)
    raw_days = pd.to_numeric(raw["days_since_last_visit"], errors="coerce")
    implied_dates = raw_dates["last_badge_swipe"] + pd.to_timedelta(raw_days, unit="D")
    valid_active = (
        (raw_days != 999)
        & (raw_days >= 0)
        & implied_dates.notna()
        & (raw_dates["membership_end"] == NO_END_DATE)
    )
    reference_date = implied_dates[valid_active].mode().iloc[0] if valid_active.any() else FALLBACK_REFERENCE_DATE

    df = raw.drop_duplicates(subset="member_id").copy()
    add_log(
        "Repeated member IDs",
        "Removed rows that repeated a member ID.",
        len(df),
        len(raw) - len(df),
    )

    columns_without_id = [column for column in raw.columns if column != "member_id"]
    rows_before = len(df)
    df = df.drop_duplicates(subset=columns_without_id).copy()
    add_log(
        "Rows identical except member ID",
        "Removed rows that matched every column other than member ID.",
        len(df),
        rows_before - len(df),
    )

    label_columns = ["gender", "country", "industry", "plan_tier"]
    labels_before = df[label_columns].astype("string")
    df["gender"] = standardise(df["gender"], GENDER_MAP)
    df["country"] = standardise(df["country"], COUNTRY_MAP)
    df["industry"] = standardise(df["industry"], INDUSTRY_MAP)
    df["plan_tier"] = standardise(df["plan_tier"], PLAN_MAP, replace_spaces=True)
    df["flag_label_changed"] = (labels_before.notna() & (labels_before != df[label_columns].astype("string"))).any(axis=1)
    add_log(
        "Category labels",
        "Mapped spelling variants in gender, country, industry and plan tier.",
        len(df),
        df["flag_label_changed"].sum(),
    )

    df["flag_industry_unknown"] = df["industry"] == "Unknown"
    df.loc[df["flag_industry_unknown"], "industry"] = pd.NA
    add_log(
        "Unknown industry",
        "Set Unknown industry labels to missing.",
        len(df),
        df["flag_industry_unknown"].sum(),
    )

    df["plan_days_per_week"] = pd.to_numeric(df["plan_days_per_week"], errors="coerce")
    df["flag_plan_inferred"] = df["plan_tier"].isna() & (df["plan_days_per_week"] == 7)
    df.loc[df["flag_plan_inferred"], "plan_tier"] = "private_office"
    add_log(
        "Missing plan inferred",
        "Inferred Private Office when the plan was missing and the plan had 7 days per week.",
        len(df),
        df["flag_plan_inferred"].sum(),
    )

    missing_plan_rows = int(df["plan_tier"].isna().sum())
    df = df[df["plan_tier"].notna()].copy()
    add_log(
        "Missing plan removed",
        "Removed rows whose plan could not be determined from the available fields.",
        len(df),
        missing_plan_rows,
    )

    slash_date_rows = int(
        df[DATE_COLS]
        .apply(lambda series: series.astype("string").str.contains("/", regex=False).fillna(False))
        .any(axis=1)
        .sum()
    )
    add_log(
        "Date formats",
        "Parsed ISO dates and day-first slash dates in the same columns.",
        len(df),
        slash_date_rows,
    )

    for column in DATE_COLS:
        df[column] = parse_mixed_dates(df[column])

    add_log(
        "Reference date",
        f"Used {reference_date:%Y-%m-%d}, inferred from active members where visit dates and recency agreed.",
        len(df),
        valid_active.sum(),
    )

    df["is_active"] = df["membership_end"] == NO_END_DATE
    df["status"] = df["is_active"].map({True: "active", False: "ended"})
    df["membership_end"] = df["membership_end"].mask(df["is_active"])
    df["days_since_last_visit"] = pd.to_numeric(df["days_since_last_visit"], errors="coerce")

    tenure_end = df["membership_end"].fillna(reference_date)
    testable_days = (df["days_since_last_visit"] != 999) & (df["days_since_last_visit"] >= 0)
    implied_end = df["last_badge_swipe"] + pd.to_timedelta(df["days_since_last_visit"], unit="D")
    day_gap = (implied_end - tenure_end).dt.days.where(testable_days)

    conflicts = pd.concat([
        df["membership_end"] < df["membership_start"],
        df["last_badge_swipe"] < df["membership_start"],
        df["last_badge_swipe"] > df["membership_end"],
        df["last_badge_swipe"] > reference_date,
        df["days_since_last_visit"] < 0,
        day_gap.abs() > 1,
    ], axis=1)
    conflict_rows = int(conflicts.any(axis=1).sum())
    df = df[~conflicts.any(axis=1)].copy()
    add_log(
        "Date conflicts",
        "Removed rows with impossible or inconsistent date sequences.",
        len(df),
        conflict_rows,
    )

    df["membership_months"] = (df["membership_end"].fillna(reference_date) - df["membership_start"]).dt.days / DAYS_PER_MONTH
    add_log(
        "Membership length",
        "Created membership_months from the start date to the end date, or to the reference date for active members.",
        len(df),
        len(df),
    )

    for column in NUMERIC_INPUTS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["is_team_account"] = to_bool(df["is_team_account"])
    uses_columns = [column for column in df.columns if column.startswith("uses_")]
    for column in uses_columns:
        df[column] = to_bool(df[column])

    df["flag_age_invalid"] = (df["age"] < 18) | (df["age"] > 80)
    df.loc[df["flag_age_invalid"], "age"] = pd.NA
    add_log(
        "Invalid ages",
        "Set ages below 18 or above 80 to missing.",
        len(df),
        df["flag_age_invalid"].sum(),
    )

    placeholder = df["n_colleagues_on_account"] == -1
    df["flag_colleagues_placeholder"] = placeholder
    df.loc[placeholder & ~df["is_team_account"], "n_colleagues_on_account"] = 0
    df.loc[placeholder & df["is_team_account"], "n_colleagues_on_account"] = pd.NA
    add_log(
        "Colleague placeholder",
        "Set -1 colleagues to 0 for individual accounts and to missing for team accounts.",
        len(df),
        placeholder.sum(),
    )

    valid_days_by_plan = df[df["plan_days_per_week"].between(1, 7)].groupby("plan_tier")["plan_days_per_week"].max()
    df["flag_plan_days_invalid"] = df["plan_days_per_week"].isin([0, 9])
    df.loc[df["flag_plan_days_invalid"], "plan_days_per_week"] = df["plan_tier"].map(valid_days_by_plan)
    add_log(
        "Invalid plan days",
        "Recovered plan days 0 or 9 from the member plan.",
        len(df),
        df["flag_plan_days_invalid"].sum(),
    )

    negative_rows = 0
    for column in COUNT_COLUMNS:
        flag = f"flag_{column}_negative"
        df[flag] = df[column] < 0
        negative_rows += int(df[flag].sum())
        df.loc[df[flag], column] = pd.NA
    add_log(
        "Negative counts",
        "Set negative visits, hours, passes and renewals to missing.",
        len(df),
        negative_rows,
    )

    df["flag_days_since_999"] = df["days_since_last_visit"] == 999
    recomputed_days = (df["membership_end"].fillna(reference_date) - df["last_badge_swipe"]).dt.days
    df.loc[df["flag_days_since_999"], "days_since_last_visit"] = recomputed_days
    add_log(
        "999 recency code",
        "Recomputed days since last visit where the raw value was 999.",
        len(df),
        df["flag_days_since_999"].sum(),
    )

    usage_zero_rows = 0
    for use_column, value_column in USAGE_PAIRS:
        not_negative = ~df[f"flag_{value_column}_negative"]
        missing_unused = df[value_column].isna() & ~df[use_column] & not_negative
        usage_zero_rows += int(missing_unused.sum())
        df.loc[missing_unused, value_column] = 0
    add_log(
        "Unused services",
        "Set missing meeting, event and guest-pass values to 0 when the service was not used.",
        len(df),
        usage_zero_rows,
    )

    df["flag_visits_scale_error"] = (df["total_visits"] > 1000) | (df["avg_weekly_visits"] > 7)
    df["flag_visits_below_last_period"] = df["total_visits"] < df["actual_visits_last_period"]
    df["flag_meeting_use_conflict"] = ~df["uses_meeting_rooms"] & (df["meeting_room_hours"] > 0)
    add_log(
        "Suspect visits",
        "Flagged visit values that look about 10 times too high. The values were not changed.",
        len(df),
        df["flag_visits_scale_error"].sum(),
    )

    df["lifetime_value"] = parse_ltv(df["lifetime_value"])
    add_log(
        "Lifetime value text",
        "Removed currency symbols, spaces and thousands separators before converting to numbers.",
        len(df),
        df["lifetime_value"].notna().sum(),
    )

    df["flag_ltv_negative"] = df["lifetime_value"] < 0
    df.loc[df["flag_ltv_negative"], "lifetime_value"] = pd.NA
    add_log(
        "Negative lifetime value",
        "Set negative lifetime values to missing.",
        len(df),
        df["flag_ltv_negative"].sum(),
    )

    is_zero = df["lifetime_value"] == 0
    plausible_zero = is_zero & (df["total_visits"] <= 5) & (df["membership_months"] < 1) & (df["n_renewals"] == 0)
    df["flag_ltv_zero_as_missing"] = is_zero & ~plausible_zero
    df.loc[df["flag_ltv_zero_as_missing"], "lifetime_value"] = pd.NA
    add_log(
        "Zero lifetime value",
        "Set implausible zeros to missing. Kept zeros only for very short memberships with few visits.",
        len(df),
        df["flag_ltv_zero_as_missing"].sum(),
    )

    positive_value = (df["lifetime_value"] > 0) & (df["membership_months"] >= 1)
    monthly_value = (df["lifetime_value"] / df["membership_months"]).where(positive_value)
    value_ratio = monthly_value / monthly_value.groupby(df["plan_tier"]).transform("median")
    df["flag_ltv_scale_error"] = value_ratio >= SCALE_RATIO_THRESHOLD
    df.loc[df["flag_ltv_scale_error"], "lifetime_value"] = df["lifetime_value"] / 100
    add_log(
        "Lifetime value scale errors",
        "Divided values at least 50 times the member plan median by 100. This remains a hypothesis until ACDC confirms it.",
        len(df),
        df["flag_ltv_scale_error"].sum(),
    )

    df["number_of_addons_used"] = df[uses_columns].sum(axis=1)
    df["plan_usage_rate"] = (
        df["actual_visits_last_period"] / df["entitled_visits_last_period"]
    ).where(df["entitled_visits_last_period"] > 0)
    df["days_since_last_visit_active"] = (reference_date - df["last_badge_swipe"]).dt.days.where(df["is_active"])
    df["monthly_value"] = df["lifetime_value"] / df["membership_months"]
    df["plan_tier_ordinal"] = df["plan_tier"].map({tier: index + 1 for index, tier in enumerate(TIER_ORDER)})
    add_log(
        "Engineered features",
        "Created membership_months, plan_usage_rate, number_of_addons_used, monthly_value, days_since_last_visit_active and plan_tier_ordinal.",
        len(df),
        len(df),
    )

    df["Plan"] = df["plan_tier"].map(PLAN_LABELS)
    df["Status"] = df["status"].str.title()
    df["Gender"] = df["gender"].fillna("(missing)")
    df["Industry"] = df["industry"].fillna("(missing)")
    df["Country"] = df["country"].fillna("(missing)")

    return {"df": df.reset_index(drop=True), "reference_date": reference_date, "log": log}


@st.cache_data(show_spinner="Cleaning the dataset...")
def load_cleaned(path):
    return clean_data(pd.read_csv(path, sep=";"))


st.set_page_config(page_title="ACDC member explorer", layout="wide")
st.title("ACDC member explorer")
st.caption("Interactive EDA dashboard using the cleaned member data and engineered features from the main notebook.")

try:
    result = load_cleaned(DATA_FILE)
except FileNotFoundError:
    st.error(
        f"Could not find {DATA_FILE.name} next to streamlit_app.py. "
        f"The app looked in {DATA_FILE.parent}."
    )
    st.stop()

df = result["df"]
reference_date = result["reference_date"]

st.sidebar.header("Filters")
plan_options = [PLAN_LABELS[tier] for tier in TIER_ORDER]
status_options = ["active", "ended"]
country_options = sorted(df["Country"].unique())

plans = st.sidebar.multiselect("Plan", plan_options, default=plan_options)
statuses = st.sidebar.multiselect("Status", status_options, default=status_options)
countries = st.sidebar.multiselect("Country", country_options, default=country_options)

age_min = int(df["age"].min())
age_max = int(df["age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))

membership_min = float(df["membership_months"].min())
membership_max = float(df["membership_months"].max())
membership_range = st.sidebar.slider("Membership length range in months", membership_min, membership_max, (membership_min, membership_max))

mask = df["Plan"].isin(plans) & df["status"].isin(statuses) & df["Country"].isin(countries)
if age_range != (age_min, age_max):
    mask &= df["age"].between(age_range[0], age_range[1])
if membership_range != (membership_min, membership_max):
    mask &= df["membership_months"].between(membership_range[0], membership_range[1])

view = df[mask]
st.sidebar.metric("Members shown", f"{len(view):,} of {len(df):,}")

if view.empty:
    st.warning("No members match these filters.")
    st.stop()

first, second, third, fourth = st.columns(4)
first.metric("Members shown", f"{len(view):,}")
second.metric("Active members", f"{view['is_active'].mean():.1%}")
median_ltv = view["lifetime_value"].median()
third.metric("Median lifetime value", f"EUR {median_ltv:,.0f}" if pd.notna(median_ltv) else "No data")
fourth.metric("Median membership length", f"{view['membership_months'].median():.1f} months")

with st.expander("Cleaning applied"):
    st.caption("This table shows each cleaning step, what it changed and how many members were affected.")
    st.dataframe(pd.DataFrame(result["log"]), width="stretch")
    st.caption(f"Reference date: {reference_date:%d %B %Y}. Cleaned base: {len(df):,} members.")

st.subheader("Members by plan")
plan_counts = view["Plan"].value_counts().rename_axis("Plan").reset_index(name="Members")
fig = px.bar(plan_counts, x="Plan", y="Members", text="Members")
fig.update_traces(marker_color=CHART_COLOR)
st.plotly_chart(fig, width="stretch")

def styled_histogram(plot_data, column, axis_label, bins=None, bin_edges=None):
    """Histogram with the shared colour and bin styling used across this section."""
    if bins is None:
        fig = px.histogram(plot_data, x=column)
    else:
        fig = px.histogram(plot_data, x=column, nbins=bins)
    fig.update_layout(
        xaxis_title=axis_label,
        yaxis_title="Members",
        bargap=0.08,
        plot_bgcolor=PANEL_COLOR,
        xaxis_showgrid=False,
        yaxis_gridcolor=GRID_COLOR,
    )
    fig.update_traces(
        marker_color=CHART_COLOR,
        marker_line_color=CHART_EDGE_COLOR,
        marker_line_width=1.5,
    )
    if bin_edges is not None:
        fig.update_traces(xbins=bin_edges)
    return fig


st.subheader("Distribution of one attribute")
chosen = st.selectbox("Attribute", list(VARIABLE_LABELS), format_func=lambda column: VARIABLE_LABELS[column])
data = view[[chosen]].dropna()
if data.empty:
    st.info("No members in this selection have a value for this attribute.")
else:
    values = data[chosen]
    discrete = values.nunique() <= DISCRETE_VALUE_LIMIT
    skewed = not discrete and values.skew() > SKEW_THRESHOLD
    integer_edges = None
    if discrete:
        integer_edges = dict(
            start=float(values.min()) - 0.5, end=float(values.max()) + 0.5, size=1
        )

    histogram, box = st.columns(2)
    with histogram:
        fig = styled_histogram(data, chosen, VARIABLE_LABELS[chosen], HISTOGRAM_BINS, integer_edges)
        st.plotly_chart(fig, width="stretch")
    with box:
        fig = px.box(data, x=chosen)
        fig.update_layout(
            xaxis_title=VARIABLE_LABELS[chosen],
            plot_bgcolor=PANEL_COLOR,
            xaxis_showgrid=False,
            yaxis_gridcolor=GRID_COLOR,
        )
        fig.update_traces(
            marker_color=CHART_COLOR,
            fillcolor="#D7EDE8",
            line_color=CHART_COLOR,
        )
        st.plotly_chart(fig, width="stretch")

    if skewed:
        log_data = pd.DataFrame({chosen: np.log1p(values.clip(lower=0))})
        fig = styled_histogram(
            log_data, chosen, f"{VARIABLE_LABELS[chosen]} (log1p)", HISTOGRAM_BINS
        )
        st.plotly_chart(fig, width="stretch")
        st.caption(
            "The lower histogram uses log1p so the many small values stay readable next to "
            "the few very large ones. It is a display transformation, not a change to the "
            "cleaned data."
        )

    bin_note = "one bar per value" if discrete else f"{HISTOGRAM_BINS} equal-width bins"
    st.caption(
        f"{len(data):,} members have a value for this attribute. "
        f"The histogram uses {bin_note}, each bar edged in white so the bins stay apart."
    )

st.subheader("Lifetime value by plan")
fig = px.box(
    view,
    x="Plan",
    y="lifetime_value",
    color="Status",
    color_discrete_map=STATUS_COLORS,
    log_y=True,
)
fig.update_layout(xaxis_title="Plan", yaxis_title="Lifetime value, EUR (log scale)")
st.plotly_chart(fig, width="stretch")

st.subheader("Membership length and monthly value")
scatter_data = view[["membership_months", "monthly_value", "Plan", "Status"]].dropna()
if scatter_data.empty:
    st.info("No members in this selection have both membership length and monthly value.")
else:
    original, transformed = st.columns(2)
    with original:
        fig = px.scatter(
            scatter_data,
            x="membership_months",
            y="monthly_value",
            color="Status",
            color_discrete_map=STATUS_COLORS,
            hover_data=["Plan"],
        )
        fig.update_layout(xaxis_title="Membership length, months", yaxis_title="Monthly value, EUR")
        st.plotly_chart(fig, width="stretch")
    with transformed:
        transformed_data = scatter_data.copy()
        transformed_data["monthly_value_log1p"] = np.log1p(transformed_data["monthly_value"])
        fig = px.scatter(
            transformed_data,
            x="membership_months",
            y="monthly_value_log1p",
            color="Status",
            color_discrete_map=STATUS_COLORS,
            hover_data=["Plan"],
        )
        fig.update_layout(xaxis_title="Membership length, months", yaxis_title="Monthly value, log1p(EUR)")
        st.plotly_chart(fig, width="stretch")
    st.caption(
        "The right chart uses log1p to reduce the visual effect of extreme values. "
        "It is a display transformation, not a change to the cleaned data."
    )

st.subheader("Summary of the selected members")
summary = view[list(VARIABLE_LABELS)].describe().T
summary = summary.rename_axis("Attribute").rename(index=VARIABLE_LABELS).round(2)
st.dataframe(summary, width="stretch")

st.subheader("Drill down to members")
drill = view.copy()

drill_plan = st.selectbox("Plan", ["All plans"] + plan_options)
drill_status = st.selectbox("Status", ["All statuses"] + ["Active", "Ended"])
drill_country = st.selectbox("Country", ["All countries"] + country_options)
drill_industry = st.selectbox("Industry", ["All industries"] + sorted(df["Industry"].unique()))
drill_gender = st.selectbox("Gender", ["All genders"] + sorted(df["Gender"].unique()))

show_all = st.checkbox("Show all matching rows", value=False)
row_limit = st.number_input(
    "Rows to show",
    min_value=1,
    max_value=10000,
    value=50,
    step=10,
    disabled=show_all,
)

if drill_plan != "All plans":
    drill = drill[drill["Plan"] == drill_plan]
if drill_status != "All statuses":
    drill = drill[drill["Status"] == drill_status]
if drill_country != "All countries":
    drill = drill[drill["Country"] == drill_country]
if drill_industry != "All industries":
    drill = drill[drill["Industry"] == drill_industry]
if drill_gender != "All genders":
    drill = drill[drill["Gender"] == drill_gender]

st.write(f"{len(drill):,} members match the drill-down filters.")

if drill.empty:
    st.warning("No members match these drill-down filters.")
else:
    table = drill[DEFAULT_DRILL_COLUMNS].copy()
    if not show_all:
        table = table.head(int(row_limit))

    numeric_columns = table.select_dtypes(include=[np.number]).columns
    table[numeric_columns] = table[numeric_columns].round(2)
    st.dataframe(table.rename(columns=MEMBER_LABELS), width="stretch")
    st.caption(f"Showing {len(table):,} of {len(drill):,} matching members.")
