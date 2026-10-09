from pit_ne_job_explorer.normalization import (
    deduplicate_records,
    infer_domain,
    infer_experience_level,
    infer_location_type,
    normalize_record,
)


def test_normalize_record_maps_aliases_and_infers_fields():
    record = normalize_record(
        {
            "job_title": "Senior Privacy Engineer",
            "company": "Digital Rights Center",
            "location": "Remote",
            "url": "https://example.org/job",
            "summary": "Build privacy tools for civil rights programs.",
            "source": "Example Board",
        }
    )

    assert record["title"] == "Senior Privacy Engineer"
    assert record["employer"] == "Digital Rights Center"
    assert record["job_url"] == "https://example.org/job"
    assert record["location_type"] == "Remote"
    assert record["experience_level"] == "Senior"
    assert record["domain"] == "Privacy"
    assert record["posting_id"]


def test_inference_helpers():
    assert infer_location_type("Hybrid Boston") == "Hybrid"
    assert infer_experience_level("Policy Fellow") == "Entry"
    assert infer_domain("Public health data analyst") == "Data Science"


def test_deduplicate_records_prefers_url_key():
    records = [
        {"title": "A", "employer": "Org", "location": "Remote", "job_url": "x"},
        {"title": "A copy", "employer": "Org", "location": "Remote", "job_url": "x"},
        {"title": "B", "employer": "Org", "location": "Remote", "job_url": "y"},
    ]

    unique = deduplicate_records(records)

    assert len(unique) == 2
    assert unique[0]["title"] == "A"

