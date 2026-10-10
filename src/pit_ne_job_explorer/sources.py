"""Public ATS source adapters for real job-board postings."""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from html import unescape
from pathlib import Path
from typing import Iterable, Mapping


SOURCE_FIELDS = (
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
)

USER_AGENT = "pit-ne-job-explorer/0.1 (+https://github.com/BaijieLi/pit-ne-job-explorer)"


class SourceFetchError(RuntimeError):
    """Raised when a configured source cannot be fetched."""


def load_source_registry(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)


def fetch_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except Exception as exc:  # pragma: no cover - exercised only with live network
        raise SourceFetchError(f"Could not fetch {url}: {exc}") from exc


def strip_html(value: object) -> str:
    text = unescape(unescape(str(value or "")))
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def _iso_date_from_millis(value: object) -> str:
    if not value:
        return ""
    try:
        seconds = int(value) / 1000
    except (TypeError, ValueError):
        return ""
    return datetime.fromtimestamp(seconds, tz=UTC).date().isoformat()


def _join_names(items: Iterable[Mapping[str, object]], field: str = "name") -> str:
    return "; ".join(
        str(item.get(field, "")).strip()
        for item in items
        if str(item.get(field, "")).strip()
    )


def parse_lever_posting(source: Mapping[str, str], posting: Mapping[str, object]) -> dict[str, str]:
    categories = posting.get("categories") or {}
    if not isinstance(categories, Mapping):
        categories = {}

    description = " ".join(
        str(part)
        for part in (
            posting.get("openingPlain"),
            posting.get("descriptionPlain"),
            posting.get("additionalPlain"),
        )
        if part
    )

    return {
        "title": str(posting.get("text", "") or ""),
        "employer": source["name"],
        "location": str(categories.get("location", "") or ""),
        "country": str(posting.get("country", "") or ""),
        "source": f"Lever: {source['name']}",
        "job_url": str(posting.get("hostedUrl") or posting.get("applyUrl") or ""),
        "description": description,
        "date_posted": _iso_date_from_millis(posting.get("createdAt")),
        "location_type": "",
        "experience_level": str(posting.get("level", "") or ""),
        "sector": str(source.get("sector", "") or ""),
        "domain": str(categories.get("team", "") or categories.get("department", "") or ""),
    }


def parse_greenhouse_posting(
    source: Mapping[str, str], posting: Mapping[str, object]
) -> dict[str, str]:
    location = posting.get("location") or {}
    if not isinstance(location, Mapping):
        location = {}
    departments = posting.get("departments") or []
    offices = posting.get("offices") or []

    return {
        "title": str(posting.get("title", "") or ""),
        "employer": source["name"],
        "location": str(location.get("name", "") or ""),
        "country": "",
        "source": f"Greenhouse: {source['name']}",
        "job_url": str(posting.get("absolute_url", "") or ""),
        "description": strip_html(posting.get("content", "")),
        "date_posted": str(posting.get("first_published") or posting.get("updated_at") or ""),
        "location_type": "",
        "experience_level": "",
        "sector": str(source.get("sector", "") or ""),
        "domain": _join_names(departments) or _join_names(offices),
    }


def parse_breezy_posting(source: Mapping[str, str], posting: Mapping[str, object]) -> dict[str, str]:
    location = posting.get("location") or {}
    if not isinstance(location, Mapping):
        location = {}
    location_name = str(location.get("name", "") or "")
    country = location.get("country") or {}
    if not isinstance(country, Mapping):
        country = {}

    description_parts = [
        posting.get("description"),
        posting.get("summary"),
        posting.get("department"),
    ]
    description = " ".join(strip_html(part) for part in description_parts if part)
    is_remote = location.get("is_remote") is True

    return {
        "title": str(posting.get("name", "") or ""),
        "employer": str((posting.get("company") or {}).get("name") or source["name"]),
        "location": location_name,
        "country": str(country.get("name", "") or ""),
        "source": f"Breezy: {source['name']}",
        "job_url": str(posting.get("url", "") or source.get("source_url", "")),
        "description": description,
        "date_posted": str(posting.get("published_date", "") or ""),
        "location_type": "Remote" if is_remote else "",
        "experience_level": "",
        "sector": str(source.get("sector", "") or ""),
        "domain": str(posting.get("department", "") or ""),
    }


def fetch_lever_source(source: Mapping[str, str]) -> list[dict[str, str]]:
    site = urllib.parse.quote(source["site"])
    url = f"https://api.lever.co/v0/postings/{site}?mode=json"
    payload = fetch_json(url)
    if not isinstance(payload, list):
        raise SourceFetchError(f"Lever source {source['name']} returned non-list JSON")
    return [parse_lever_posting(source, posting) for posting in payload]


def fetch_greenhouse_source(source: Mapping[str, str]) -> list[dict[str, str]]:
    token = urllib.parse.quote(source["board_token"])
    url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
    payload = fetch_json(url)
    if not isinstance(payload, Mapping) or not isinstance(payload.get("jobs"), list):
        raise SourceFetchError(f"Greenhouse source {source['name']} returned unexpected JSON")
    return [parse_greenhouse_posting(source, posting) for posting in payload["jobs"]]


def fetch_breezy_source(source: Mapping[str, str]) -> list[dict[str, str]]:
    subdomain = urllib.parse.quote(source["subdomain"])
    url = f"https://{subdomain}.breezy.hr/json"
    payload = fetch_json(url)
    if not isinstance(payload, list):
        raise SourceFetchError(f"Breezy source {source['name']} returned non-list JSON")
    return [parse_breezy_posting(source, posting) for posting in payload]


def fetch_source(source: Mapping[str, str]) -> list[dict[str, str]]:
    provider = source.get("provider")
    if provider == "lever":
        return fetch_lever_source(source)
    if provider == "greenhouse":
        return fetch_greenhouse_source(source)
    if provider == "breezy":
        return fetch_breezy_source(source)
    raise SourceFetchError(f"Unsupported provider for {source.get('name')}: {provider}")


def collect_jobs(sources: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in sources:
        rows.extend(fetch_source(source))
    return rows


def collect_jobs_with_errors(
    sources: Iterable[Mapping[str, str]],
) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    errors: list[str] = []
    for source in sources:
        try:
            rows.extend(fetch_source(source))
        except SourceFetchError as exc:
            errors.append(str(exc))
    return rows, errors
