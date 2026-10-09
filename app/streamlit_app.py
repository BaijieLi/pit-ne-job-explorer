"""Streamlit explorer for classified PIT job postings."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from pit_ne_job_explorer.classification import classify_records
from pit_ne_job_explorer.normalization import deduplicate_records, normalize_records


DEFAULT_OUTPUT = Path("outputs/classified_jobs.csv")
DEFAULT_EXAMPLE = Path("data/examples/synthetic_job_postings.csv")


@st.cache_data
def load_jobs() -> pd.DataFrame:
    source = DEFAULT_OUTPUT if DEFAULT_OUTPUT.exists() else DEFAULT_EXAMPLE
    raw = pd.read_csv(source)
    records = classify_records(deduplicate_records(normalize_records(raw.to_dict("records"))))
    return pd.DataFrame(records)


jobs = load_jobs()

st.set_page_config(page_title="PIT-NE Job Explorer", layout="wide")
st.title("PIT-NE Job Explorer")

label_options = sorted(jobs["pit_label"].dropna().unique())
domain_options = sorted(jobs["domain"].dropna().unique())
sector_options = sorted(jobs["sector"].dropna().unique())
level_options = sorted(jobs["experience_level"].dropna().unique())

col1, col2, col3, col4 = st.columns(4)
with col1:
    labels = st.multiselect("PIT label", label_options, default=label_options)
with col2:
    domains = st.multiselect("Domain", domain_options, default=domain_options)
with col3:
    sectors = st.multiselect("Sector", sector_options, default=sector_options)
with col4:
    levels = st.multiselect("Level", level_options, default=level_options)

query = st.text_input("Search title, employer, or description")

filtered = jobs[
    jobs["pit_label"].isin(labels)
    & jobs["domain"].isin(domains)
    & jobs["sector"].isin(sectors)
    & jobs["experience_level"].isin(levels)
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
metric_cols[3].metric("Domains", filtered["domain"].nunique())

st.dataframe(
    filtered[
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
    use_container_width=True,
    hide_index=True,
)

