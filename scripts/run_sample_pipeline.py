"""Run the PIT job pipeline on the synthetic example dataset."""

from __future__ import annotations

from pit_ne_job_explorer.cli import run


def main() -> int:
    count = run(
        "data/examples/synthetic_job_postings.csv",
        "outputs/classified_jobs.csv",
        "outputs/job_summary.csv",
    )
    print(f"Sample pipeline complete: {count} classified job row(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

