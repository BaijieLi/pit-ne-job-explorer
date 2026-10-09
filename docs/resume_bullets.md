# Resume Bullets

Use the version that best matches the role. This public repository uses
synthetic examples, so resume wording should emphasize the reusable pipeline,
classification logic, explorer interface, and data governance decisions.

## Software Engineering Version

- Built a Python and Streamlit job explorer that normalizes job postings,
  deduplicates records, classifies Public Interest Technology relevance, and
  exposes searchable filters for domain, sector, level, and location type.
- Designed modular pipeline components for schema normalization, rule-based
  classification, summary exports, and interactive exploration, with 9
  automated tests covering the core data flow.
- Implemented public-safe project packaging with synthetic examples,
  documentation, source policy notes, and generated dashboard preview assets.

## Data Engineering Version

- Created a reusable job-posting ETL pipeline that standardizes raw exports,
  removes duplicates, assigns PIT relevance labels, and produces classified job
  and summary CSV outputs.
- Developed transparent scoring rules using public-interest, technology,
  governance, sector, and commercial-language signals, preserving matched
  keywords for auditability.
- Structured the project for future source adapters while keeping raw scraped
  data, private project notes, and generated outputs out of version control.

## Data Analyst Version

- Built a synthetic Public Interest Technology job dataset and analysis
  workflow to summarize roles by PIT label, domain, sector, experience level,
  and location type.
- Created a Streamlit explorer prototype with search and filters to help users
  browse PIT-aligned job pathways across technical, policy, research, privacy,
  and design domains.
- Documented the classification methodology and limitations so uncertain roles
  can be reviewed rather than treated as final automated labels.

## Short Project Description

Python data pipeline and Streamlit explorer for collecting, cleaning,
classifying, and visualizing Public Interest Technology job postings with a
public-safe synthetic demo dataset.

## Technical Keywords

Python, Streamlit, ETL, data cleaning, deduplication, rule-based
classification, job postings, data visualization, pytest, public interest
technology, data governance.
