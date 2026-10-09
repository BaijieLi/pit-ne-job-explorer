"""Aggregate classified PIT job postings for dashboard summaries."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping


SUMMARY_FIELDNAMES = ("section", "name", "value", "percent")


def _percent(count: int, total: int) -> str:
    if total == 0:
        return ""
    return f"{count / total:.2%}"


def _counter_rows(section: str, counter: Counter[str], total: int) -> list[dict[str, object]]:
    return [
        {
            "section": section,
            "name": name or "Unknown",
            "value": count,
            "percent": _percent(count, total),
        }
        for name, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def summarize_records(records: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    """Create CSV-friendly summary rows from classified postings."""

    rows = list(records)
    total = len(rows)
    summary: list[dict[str, object]] = [
        {"section": "summary", "name": "record_count", "value": total, "percent": ""},
        {
            "section": "summary",
            "name": "pit_count",
            "value": sum(1 for row in rows if row.get("pit_label") == "PIT"),
            "percent": _percent(
                sum(1 for row in rows if row.get("pit_label") == "PIT"), total
            ),
        },
    ]

    for field in (
        "pit_label",
        "domain",
        "sector",
        "experience_level",
        "location_type",
    ):
        summary.extend(
            _counter_rows(
                field,
                Counter(str(row.get(field, "") or "Unknown") for row in rows),
                total,
            )
        )
    return summary

