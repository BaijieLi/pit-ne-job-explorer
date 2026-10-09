from pit_ne_job_explorer.analysis import summarize_records


def test_summarize_records_counts_labels_and_categories():
    rows = summarize_records(
        [
            {
                "pit_label": "PIT",
                "domain": "Policy",
                "sector": "Government",
                "experience_level": "Entry",
                "location_type": "Remote",
            },
            {
                "pit_label": "NON_PIT",
                "domain": "General",
                "sector": "Private",
                "experience_level": "Mid",
                "location_type": "In-Person",
            },
        ]
    )

    by_key = {(row["section"], row["name"]): row for row in rows}
    assert by_key[("summary", "record_count")]["value"] == 2
    assert by_key[("summary", "pit_count")]["percent"] == "50.00%"
    assert by_key[("pit_label", "PIT")]["value"] == 1
    assert by_key[("sector", "Government")]["percent"] == "50.00%"

