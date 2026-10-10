# Deployment

This app is ready for Streamlit Community Cloud deployment.

## Streamlit Community Cloud Settings

Use these values when creating the app:

| Field | Value |
| --- | --- |
| Repository | `BaijieLi/pit-ne-job-explorer` |
| Branch | `main` |
| Main file path | `app/streamlit_app.py` |
| App URL | choose an available name such as `pit-ne-job-explorer` |

No secrets are required. The deployed app reads `data/source_registry.json` and
fetches public Greenhouse, Lever, Breezy, and Ashby postings at runtime.

## Runtime Behavior

The app loads data in this order:

1. Local generated output at `outputs/classified_jobs.csv`, when present.
2. Live public ATS sources from `data/source_registry.json`.
3. Synthetic fallback data from `data/examples/synthetic_job_postings.csv`.

Generated CSV snapshots are intentionally excluded from Git because live job
postings expire and should be refreshed.

## Local Deployment Check

From the repository root:

```bash
streamlit run app/streamlit_app.py
```

The app should show a caption describing whether it loaded local output, live
ATS data, or the synthetic fallback dataset.
