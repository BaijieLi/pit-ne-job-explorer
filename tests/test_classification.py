from pit_ne_job_explorer.classification import classify_record, score_record


def test_classify_pit_role():
    row = classify_record(
        {
            "title": "AI Policy Fellow",
            "sector": "Nonprofit",
            "domain": "Policy",
            "description": "Research AI governance, equity, accountability, and public service.",
        }
    )

    assert row["pit_label"] == "PIT"
    assert row["pit_score"] >= 4
    assert "equity" in row["matched_keywords"]


def test_classify_commercial_role_as_non_pit():
    row = classify_record(
        {
            "title": "Growth Marketing Manager",
            "sector": "Private",
            "domain": "General",
            "description": "Own customer acquisition, revenue growth, and market share.",
        }
    )

    assert row["pit_label"] == "NON_PIT"


def test_score_returns_keywords():
    score, keywords = score_record(
        {
            "title": "Accessibility Researcher",
            "sector": "Academia",
            "description": "Accessibility research for digital public services.",
        }
    )

    assert score > 0
    assert "accessibility" in keywords


def test_short_keywords_do_not_match_inside_words():
    row = classify_record(
        {
            "title": "Growth Marketing Manager",
            "sector": "Private",
            "domain": "General",
            "description": "Support retail campaigns and market share reporting.",
        }
    )

    assert "ai" not in row["matched_keywords"].split("|")
