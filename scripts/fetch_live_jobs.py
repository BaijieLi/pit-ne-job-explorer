"""Fetch real public ATS postings and run the PIT classifier."""

from __future__ import annotations

import argparse
from pathlib import Path

from pit_ne_job_explorer.cli import run, write_csv
from pit_ne_job_explorer.sources import (
    SOURCE_FIELDS,
    collect_jobs_with_errors,
    load_source_registry,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch real public job postings from configured ATS boards."
    )
    parser.add_argument(
        "--sources",
        default="data/source_registry.json",
        help="JSON registry of public ATS sources.",
    )
    parser.add_argument(
        "--raw-output",
        default="outputs/live_raw_jobs.csv",
        help="Raw normalized source rows before classification.",
    )
    parser.add_argument(
        "--jobs-output",
        default="outputs/classified_jobs.csv",
        help="Classified job-board output for the Streamlit explorer.",
    )
    parser.add_argument(
        "--summary-output",
        default="outputs/job_summary.csv",
        help="Summary metric output CSV.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    sources = load_source_registry(args.sources)
    rows, errors = collect_jobs_with_errors(sources)
    for error in errors:
        print(f"Warning: {error}")
    if not rows:
        raise SystemExit("No postings were fetched from the configured sources.")
    write_csv(args.raw_output, rows, SOURCE_FIELDS)
    count = run(args.raw_output, args.jobs_output, args.summary_output)
    successful_sources = len(sources) - len(errors)
    print(
        f"Fetched {len(rows)} public posting(s) from "
        f"{successful_sources}/{len(sources)} source(s)."
    )
    print(f"Wrote {count} classified job row(s) to {Path(args.jobs_output)}")
    print(f"Wrote summary metrics to {Path(args.summary_output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
