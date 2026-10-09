"""Rule-based Public Interest Technology job classification."""

from __future__ import annotations

import re
from typing import Iterable, Mapping

from .normalization import clean_text


KEYWORD_GROUPS: dict[str, tuple[str, ...]] = {
    "public_interest": (
        "accessibility",
        "accountability",
        "civil rights",
        "civic",
        "community",
        "digital rights",
        "equity",
        "fairness",
        "human rights",
        "public health",
        "public service",
        "public-sector",
        "transparency",
    ),
    "technology": (
        "ai",
        "analytics",
        "cybersecurity",
        "data",
        "digital",
        "machine learning",
        "platform",
        "privacy",
        "software",
        "technology",
    ),
    "governance": (
        "compliance",
        "ethics",
        "governance",
        "policy",
        "regulation",
        "research",
        "safety",
    ),
}

COMMERCIAL_ONLY_TERMS = (
    "customer acquisition",
    "market share",
    "revenue growth",
    "sales pipeline",
    "conversion funnel",
)


def _contains_phrase(text: str, phrase: str) -> bool:
    pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None


def matched_keywords(record: Mapping[str, object]) -> dict[str, list[str]]:
    """Return matched keyword groups for one posting."""

    haystack = " ".join(
        clean_text(record.get(field)).lower()
        for field in ("title", "employer", "description", "sector", "domain")
    )
    matches: dict[str, list[str]] = {}
    for group, keywords in KEYWORD_GROUPS.items():
        group_matches = [keyword for keyword in keywords if _contains_phrase(haystack, keyword)]
        if group_matches:
            matches[group] = group_matches
    negative = [term for term in COMMERCIAL_ONLY_TERMS if _contains_phrase(haystack, term)]
    if negative:
        matches["commercial_only"] = negative
    return matches


def score_record(record: Mapping[str, object]) -> tuple[float, list[str]]:
    """Return a PIT relevance score and matched keywords."""

    matches = matched_keywords(record)
    score = 0.0
    if "public_interest" in matches:
        score += 2.0
    if "technology" in matches:
        score += 1.5
    if "governance" in matches:
        score += 1.5

    sector = clean_text(record.get("sector")).lower()
    if sector in {"government", "nonprofit", "academia"}:
        score += 0.75

    if "commercial_only" in matches:
        score -= min(2.0, len(matches["commercial_only"]) * 0.75)

    flat_matches = [
        keyword
        for group in ("public_interest", "technology", "governance", "commercial_only")
        for keyword in matches.get(group, [])
    ]
    return round(max(score, 0.0), 2), flat_matches


def classify_record(record: Mapping[str, object]) -> dict[str, object]:
    """Add PIT classification fields to one normalized posting."""

    score, keywords = score_record(record)
    has_public_interest = any(
        keyword in keywords for keyword in KEYWORD_GROUPS["public_interest"]
    )
    has_technical_or_governance = any(
        keyword in keywords
        for keyword in (*KEYWORD_GROUPS["technology"], *KEYWORD_GROUPS["governance"])
    )
    if score >= 4.0 and has_public_interest and has_technical_or_governance:
        label = "PIT"
    elif score >= 2.5:
        label = "REVIEW"
    else:
        label = "NON_PIT"

    output = dict(record)
    output["pit_score"] = score
    output["pit_label"] = label
    output["matched_keywords"] = "|".join(sorted(set(keywords)))
    return output


def classify_records(
    records: Iterable[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Classify many normalized postings."""

    return [classify_record(record) for record in records]
