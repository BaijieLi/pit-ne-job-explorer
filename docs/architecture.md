# Architecture

## Pipeline Overview

```text
public ATS boards or CSV source data
  -> source adapters
  -> normalize job fields
  -> deduplicate postings
  -> classify PIT relevance
  -> summarize distributions
  -> export CSVs
  -> explore in Streamlit
```

## Components

### Normalization

Maps varied input column names into a canonical job-posting schema. This layer
also infers basic fields such as location type, experience level, sector, and
domain when source data does not provide them.

### Source Adapters

Fetches public postings from configured Greenhouse and Lever boards, preserving
the original employer-hosted posting link in `job_url`. Each source is listed in
`data/source_registry.json` so new employers can be reviewed and added without
changing the parsing code.

### Deduplication

Removes repeated postings using job URLs when available and a normalized
title-employer-location key when URLs are missing.

### Classification

Scores postings with transparent keyword rules across public-interest,
technology, and governance categories. The output labels are `PIT`, `REVIEW`,
and `NON_PIT` so uncertain roles can be audited instead of silently accepted.

### Analysis

Aggregates classified records by label, domain, sector, experience level, and
location type. These summaries are designed for dashboards and client-facing
updates.

### Explorer

The Streamlit app provides search, category filters, and clickable application
links over classified jobs. It is a public-facing prototype and should use
synthetic, permissioned, or reviewed public-source data only.

## Data Storage

Generated outputs are written to `outputs/`, which is ignored by Git. This keeps
local live-job snapshots separate from the public repository while allowing the
job board to run locally with fresh data.
