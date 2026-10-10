# Methodology

## Working Definition

A Public Interest Technology job applies technical, digital, data, policy, or
design expertise toward public-interest outcomes. Examples include roles focused
on privacy, civil rights, accessibility, public health, responsible AI, civic
services, digital rights, and technology governance.

## Classification Approach

The first public version uses transparent rules rather than a black-box model.
Each posting is scored based on:

- public-interest terms such as equity, accessibility, public health, civil
  rights, digital rights, and community impact
- technology terms such as data, software, cybersecurity, AI, machine learning,
  digital platforms, and privacy engineering
- governance terms such as policy, regulation, compliance, ethics, research,
  and accountability
- organization sector signals such as government and nonprofit employers
- commercial-only language such as sales, revenue growth, and customer
  acquisition, which can reduce the score

The output labels intentionally include `REVIEW` because some interdisciplinary
roles need human judgment.

## Source Policy

Future scraper adapters should only be added for sources that permit collection
or provide data through approved APIs, feeds, exports, or permissioned handoff.
Sources that prohibit scraping should be documented and excluded.

The current live-fetch prototype uses company-hosted public ATS endpoints:

- Greenhouse Job Board API for published board postings.
- Lever Postings API for published public postings.
- Breezy public JSON boards for published public postings.

Generated job CSVs are treated as local outputs because live postings can expire
and source descriptions may change. The public repository keeps source adapter
code and source metadata, while generated datasets remain under `outputs/`.
