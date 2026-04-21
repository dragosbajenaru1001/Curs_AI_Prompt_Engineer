from app.pipeline import BugReportPipeline


def run_code():
    pipeline = BugReportPipeline()
    with open("data/bug_report.txt", "r") as f:
        bug_report = f.read()
    result = pipeline.run(bugs=bug_report)

    print(result["email_status"])
    