"""Normalize raw job postings into a public-safe canonical schema."""

from __future__ import annotations

import hashlib
import re
from typing import Iterable, Mapping

from .schema import CANONICAL_FIELDS


FIELD_ALIASES = {
    "company": "employer",
    "organization": "employer",
    "org": "employer",
    "job_title": "title",
    "role": "title",
    "url": "job_url",
    "link": "job_url",
    "posting_url": "job_url",
    "job_link": "job_url",
    "desc": "description",
    "summary": "description",
    "posted": "date_posted",
    "level": "experience_level",
    "work_type": "location_type",
    "employment_location_type": "location_type",
    "industry_cluster": "domain",
}

LOCATION_TYPES = {
    "remote": "Remote",
    "hybrid": "Hybrid",
    "in person": "In-Person",
    "in-person": "In-Person",
    "onsite": "In-Person",
    "on-site": "In-Person",
}

EXPERIENCE_PATTERNS = (
    ("Executive", ("chief", "vp", "vice president", "executive")),
    ("Director", ("director", "head of")),
    ("Senior", ("senior", "sr.", "lead", "principal", "manager")),
    ("Entry", ("fellow", "intern", "assistant", "associate", "entry")),
)

DOMAIN_PATTERNS = (
    ("Privacy", ("privacy", "digital rights", "data protection")),
    ("Policy", ("policy", "governance", "regulation", "compliance")),
    ("Research", ("research", "study", "evaluate", "analysis")),
    ("Developer", ("software", "engineer", "developer", "platform")),
    ("Data Science", ("data", "machine learning", "ai", "analytics")),
    ("Design", ("ux", "design", "accessibility", "user research")),
    ("Security", ("cybersecurity", "security", "threat")),
    ("Advocacy", ("advocacy", "civil rights", "community")),
)

SECTOR_PATTERNS = (
    ("Government", ("government", "public sector", "city", "state", "department")),
    ("Nonprofit", ("nonprofit", "non-profit", "foundation", "civil society")),
    ("Academia", ("university", "institute", "lab", "research center")),
    ("Private", ("startup", "company", "enterprise", "platform", "studio")),
)


def _to_snake_case(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"[^A-Za-z0-9]+", "_", value)
    return value.strip("_").lower()


def canonical_field_name(field_name: str) -> str:
    """Return the canonical field name for an input column."""

    snake = _to_snake_case(field_name)
    return FIELD_ALIASES.get(snake, snake)


def clean_text(value: object) -> str:
    """Normalize a raw text value."""

    return re.sub(r"\s+", " ", str(value or "")).strip()


def infer_location_type(*texts: object) -> str:
    haystack = " ".join(clean_text(text).lower() for text in texts)
    for pattern, label in LOCATION_TYPES.items():
        if pattern in haystack:
            return label
    return "Unknown"


def infer_experience_level(*texts: object) -> str:
    haystack = " ".join(clean_text(text).lower() for text in texts)
    for label, patterns in EXPERIENCE_PATTERNS:
        if any(pattern in haystack for pattern in patterns):
            return label
    return "Mid" if haystack else "Unknown"


def infer_sector(*texts: object) -> str:
    haystack = " ".join(clean_text(text).lower() for text in texts)
    for label, patterns in SECTOR_PATTERNS:
        if any(pattern in haystack for pattern in patterns):
            return label
    return "Unknown"


def infer_domain(*texts: object) -> str:
    haystack = " ".join(clean_text(text).lower() for text in texts)
    for label, patterns in DOMAIN_PATTERNS:
        if any(pattern in haystack for pattern in patterns):
            return label
    return "General"


def infer_country(location: object, country: object = "") -> str:
    explicit = clean_text(country)
    if explicit:
        return explicit
    location_text = clean_text(location).lower()
    if any(token in location_text for token in ("united states", "usa", " us ")):
        return "United States"
    if any(state in location_text for state in (" ma", " ny", " dc", " ca", " wa", " il")):
        return "United States"
    return "Unknown"


def posting_id(record: Mapping[str, object]) -> str:
    """Create a stable posting identifier from durable fields."""

    key = "|".join(
        clean_text(record.get(field)).lower()
        for field in ("title", "employer", "location", "job_url")
    )
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def normalize_record(record: Mapping[str, object]) -> dict[str, object]:
    """Normalize one raw job posting."""

    flattened: dict[str, object] = {}
    for key, value in record.items():
        flattened[canonical_field_name(key)] = value

    title = clean_text(flattened.get("title"))
    employer = clean_text(flattened.get("employer"))
    location = clean_text(flattened.get("location"))
    description = clean_text(flattened.get("description"))
    sector = clean_text(flattened.get("sector")) or infer_sector(
        employer, description, flattened.get("source")
    )
    domain = clean_text(flattened.get("domain")) or infer_domain(title, description)
    location_type = clean_text(flattened.get("location_type")) or infer_location_type(
        location, description
    )
    experience_level = clean_text(
        flattened.get("experience_level")
    ) or infer_experience_level(title, description)

    normalized = {field: "" for field in CANONICAL_FIELDS}
    normalized.update(
        {
            "title": title,
            "employer": employer,
            "location": location,
            "country": infer_country(location, flattened.get("country")),
            "source": clean_text(flattened.get("source")),
            "job_url": clean_text(flattened.get("job_url")),
            "description": description,
            "date_posted": clean_text(flattened.get("date_posted")),
            "location_type": location_type,
            "experience_level": experience_level,
            "sector": sector,
            "domain": domain,
        }
    )
    normalized["posting_id"] = clean_text(flattened.get("posting_id")) or posting_id(
        normalized
    )
    return normalized


def normalize_records(records: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    """Normalize many raw job postings."""

    return [normalize_record(record) for record in records]


def deduplicate_records(
    records: Iterable[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Remove duplicate postings while preserving input order."""

    unique: list[dict[str, object]] = []
    seen: set[str] = set()
    for record in records:
        url = clean_text(record.get("job_url")).lower()
        key = url or "|".join(
            clean_text(record.get(field)).lower()
            for field in ("title", "employer", "location")
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(dict(record))
    return unique

