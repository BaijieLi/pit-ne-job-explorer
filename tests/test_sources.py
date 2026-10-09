from pit_ne_job_explorer.sources import (
    parse_greenhouse_posting,
    parse_lever_posting,
    strip_html,
)


def test_parse_lever_posting_preserves_apply_link_and_categories():
    source = {"name": "Civitech", "sector": "Private"}
    posting = {
        "id": "abc",
        "text": "Data Acquisition Specialist",
        "hostedUrl": "https://jobs.lever.co/civitech/abc",
        "createdAt": 1760000000000,
        "descriptionPlain": "Build civic data tools for public participation.",
        "categories": {
            "location": "Austin, TX or Remote",
            "commitment": "Full-time",
            "team": "Data",
        },
    }

    row = parse_lever_posting(source, posting)

    assert row["title"] == "Data Acquisition Specialist"
    assert row["job_url"] == "https://jobs.lever.co/civitech/abc"
    assert row["domain"] == "Data"
    assert row["sector"] == "Private"
    assert row["location_type"] == ""
    assert row["date_posted"] == "2025-10-09"


def test_parse_greenhouse_posting_strips_html_and_keeps_source_url():
    source = {"name": "Code for America", "sector": "Nonprofit"}
    posting = {
        "id": 123,
        "title": "AI Governance Lead",
        "absolute_url": "https://job-boards.greenhouse.io/codeforamerica/jobs/123",
        "updated_at": "2026-10-02T22:04:29-04:00",
        "location": {"name": "Remote (in the U.S.)"},
        "content": "&lt;p&gt;Responsible AI &amp;amp; policy for public services.&lt;/p&gt;",
        "departments": [{"name": "Technology"}],
    }

    row = parse_greenhouse_posting(source, posting)

    assert row["employer"] == "Code for America"
    assert row["job_url"].endswith("/123")
    assert row["description"] == "Responsible AI & policy for public services."
    assert row["domain"] == "Technology"


def test_strip_html_normalizes_entities_and_spacing():
    assert strip_html("&lt;p&gt;Digital&nbsp;rights&lt;/p&gt;") == "Digital rights"
