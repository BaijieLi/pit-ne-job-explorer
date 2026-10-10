# Project Plan

## Phase 1: Public Scaffold

- Create a clean repository structure. Done.
- Add synthetic example data. Done.
- Implement normalization, deduplication, classification, and analysis. Done.
- Add tests for the core pipeline. Done.

## Phase 2: Data Collection

- Review source permissions before adding scraper adapters.
- Add source-specific collectors only for allowed sources. Done for the initial
  Greenhouse, Lever, and Breezy adapters.
- Track failed or expired posting links.
- Store raw data outside Git.

## Phase 3: Classification and Review

- Refine the PIT coding guide.
- Add a reviewed sample set for label quality checks.
- Improve domain, sector, and level inference.
- Add reviewer notes or audit outputs.

## Phase 4: Job Explorer

- Expand the Streamlit explorer with filters for domain, location type,
  experience level, employer, PIT label, and sector. Done.
- Include direct links to original postings. Done.
- Add screenshots using synthetic or share-approved data. Done for live-source
  explorer preview.
- Add methodology and source-disclaimer pages.
- Prepare resume bullets and portfolio summary. Done.
