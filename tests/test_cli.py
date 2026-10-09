import csv

from pit_ne_job_explorer.cli import run


def test_run_writes_classified_jobs_and_summary(tmp_path):
    input_path = tmp_path / "jobs.csv"
    jobs_output = tmp_path / "classified.csv"
    summary_output = tmp_path / "summary.csv"
    input_path.write_text(
        "title,employer,location,source,job_url,description,sector\n"
        "AI Policy Fellow,Civic Lab,Remote,Example,x,"
        "AI governance and equity for public service,Nonprofit\n",
        encoding="utf-8",
    )

    count = run(input_path, jobs_output, summary_output)

    assert count == 1
    with jobs_output.open(newline="", encoding="utf-8") as file:
        jobs = list(csv.DictReader(file))
    with summary_output.open(newline="", encoding="utf-8") as file:
        summary = list(csv.DictReader(file))

    assert jobs[0]["pit_label"] == "PIT"
    assert any(row["section"] == "summary" for row in summary)

