"""Command-line pipeline for PIT job posting classification."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .analysis import SUMMARY_FIELDNAMES, summarize_records
from .classification import classify_records
from .normalization import deduplicate_records, normalize_records
from .schema import CANONICAL_FIELDS


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv(
    path: str | Path, rows: list[dict[str, object]], fieldnames: tuple[str, ...]
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(
    input_path: str | Path,
    jobs_output_path: str | Path,
    summary_output_path: str | Path,
) -> int:
    """Normalize, deduplicate, classify, and summarize job postings."""

    raw_records = read_csv(input_path)
    normalized = normalize_records(raw_records)
    unique = deduplicate_records(normalized)
    classified = classify_records(unique)
    summary = summarize_records(classified)
    write_csv(jobs_output_path, classified, CANONICAL_FIELDS)
    write_csv(summary_output_path, summary, SUMMARY_FIELDNAMES)
    return len(classified)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Classify and summarize Public Interest Technology job postings."
    )
    parser.add_argument("input", help="Raw job posting CSV.")
    parser.add_argument(
        "--jobs-output",
        default="outputs/classified_jobs.csv",
        help="Classified job output CSV.",
    )
    parser.add_argument(
        "--summary-output",
        default="outputs/job_summary.csv",
        help="Summary metric output CSV.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    count = run(args.input, args.jobs_output, args.summary_output)
    print(f"Wrote {count} classified job row(s) to {args.jobs_output}")
    print(f"Wrote summary metrics to {args.summary_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

