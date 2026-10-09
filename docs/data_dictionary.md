# Data Dictionary

| Field | Description |
| --- | --- |
| posting_id | Stable identifier generated from title, employer, location, and URL. |
| title | Job title. |
| employer | Hiring organization. |
| location | Free-text location from the source posting. |
| country | Country inferred or provided by the source. |
| source | Source board, newsletter, or collection method. |
| job_url | Link to the original posting. |
| description | Short job description or excerpt used for classification. |
| date_posted | Posting date when available. |
| location_type | `Remote`, `Hybrid`, `In-Person`, or `Unknown`. |
| experience_level | `Entry`, `Mid`, `Senior`, `Director`, `Executive`, or `Unknown`. |
| sector | `Government`, `Nonprofit`, `Private`, `Academia`, or `Unknown`. |
| domain | Primary job domain such as `Policy`, `Privacy`, `Research`, `Developer`, or `Data Science`. |
| pit_score | Rule-based score used to classify PIT relevance. |
| pit_label | `PIT`, `REVIEW`, or `NON_PIT`. |
| matched_keywords | Pipe-delimited keywords that contributed to the PIT score. |

Live-source adapters preserve the employer-hosted ATS posting URL in `job_url`
so the Streamlit explorer can render a direct application link.
