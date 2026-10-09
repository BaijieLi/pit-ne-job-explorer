"""Canonical schema for PIT job postings."""

from __future__ import annotations

CANONICAL_FIELDS = (
    "posting_id",
    "title",
    "employer",
    "location",
    "country",
    "source",
    "job_url",
    "description",
    "date_posted",
    "location_type",
    "experience_level",
    "sector",
    "domain",
    "pit_score",
    "pit_label",
    "matched_keywords",
)

RAW_TEXT_FIELDS = ("title", "employer", "location", "description", "source")

