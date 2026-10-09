# Architecture

## Pipeline Overview

```text
source export or scraper output
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

The Streamlit app provides search and filters over classified jobs. It is a
public-facing prototype and should use synthetic, permissioned, or reviewed data
only.

