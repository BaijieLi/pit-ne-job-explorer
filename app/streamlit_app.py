"""Streamlit explorer for classified PIT job postings."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from pit_ne_job_explorer.classification import classify_records
from pit_ne_job_explorer.normalization import deduplicate_records, normalize_records


DEFAULT_OUTPUT = Path("outputs/classified_jobs.csv")
DEFAULT_EXAMPLE = Path("data/examples/synthetic_job_postings.csv")


st.set_page_config(page_title="PIT-NE Job Explorer", layout="wide")


@st.cache_data
def load_jobs() -> pd.DataFrame:
    source = DEFAULT_OUTPUT if DEFAULT_OUTPUT.exists() else DEFAULT_EXAMPLE
    raw = pd.read_csv(source)
    records = classify_records(deduplicate_records(normalize_records(raw.to_dict("records"))))
    return pd.DataFrame(records)


jobs = load_jobs()

st.title("PIT-NE Job Explorer")

label_options = sorted(jobs["pit_label"].dropna().unique())
employer_options = sorted(jobs["employer"].dropna().unique())
domain_options = sorted(jobs["domain"].dropna().unique())
sector_options = sorted(jobs["sector"].dropna().unique())
level_options = sorted(jobs["experience_level"].dropna().unique())
location_type_options = sorted(jobs["location_type"].dropna().unique())

col1, col2, col3 = st.columns(3)
with col1:
    labels = st.multiselect("PIT label", label_options, default=label_options)
with col2:
    employers = st.multiselect("Employer", employer_options, default=employer_options)
with col3:
    domains = st.multiselect("Domain", domain_options, default=domain_options)

col4, col5, col6 = st.columns(3)
with col4:
    sectors = st.multiselect("Sector", sector_options, default=sector_options)
with col5:
    levels = st.multiselect("Level", level_options, default=level_options)
with col6:
    location_types = st.multiselect(
        "Location type", location_type_options, default=location_type_options
    )

query = st.text_input("Search title, employer, or description")

filtered = jobs[
    jobs["pit_label"].isin(labels)
    & jobs["employer"].isin(employers)
    & jobs["domain"].isin(domains)
    & jobs["sector"].isin(sectors)
    & jobs["experience_level"].isin(levels)
    & jobs["location_type"].isin(location_types)
]
if query:
    query_lower = query.lower()
    filtered = filtered[
        filtered[["title", "employer", "description"]]
        .fillna("")
        .agg(" ".join, axis=1)
        .str.lower()
        .str.contains(query_lower, regex=False)
    ]

metric_cols = st.columns(4)
metric_cols[0].metric("Jobs", len(filtered))
metric_cols[1].metric("PIT", int((filtered["pit_label"] == "PIT").sum()))
metric_cols[2].metric("Review", int((filtered["pit_label"] == "REVIEW").sum()))
metric_cols[3].metric("Employers", filtered["employer"].nunique())

display = filtered.sort_values(["pit_score", "employer", "title"], ascending=[False, True, True])
st.dataframe(
    display[
        [
            "title",
            "employer",
            "location",
            "pit_label",
            "pit_score",
            "domain",
            "sector",
            "experience_level",
            "location_type",
            "job_url",
        ]
    ],
    width="stretch",
    hide_index=True,
    column_config={
        "job_url": st.column_config.LinkColumn("Apply link", display_text="Open posting"),
        "pit_score": st.column_config.NumberColumn("PIT score", format="%.2f"),
    },
)
