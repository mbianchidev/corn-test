#!/usr/bin/env python3
"""Java test result analyzer for corn-flakes-detection.

Parses Maven Surefire JUnit XML reports from ``target/surefire-reports/``.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _report_utils import cli_main, find_xml_reports  # noqa: E402

LANGUAGE = "Java"
FRAMEWORK = "JUnit 5"


def find_reports(artifacts_dir: Path) -> list[Path]:
    """Find Java Surefire XML test reports."""
    # Standard Surefire location
    for d in artifacts_dir.rglob("surefire-reports"):
        xmls = sorted(d.glob("TEST-*.xml"))
        if xmls:
            return xmls
    # Fallback: any XML containing test results
    return find_xml_reports(artifacts_dir, "TEST-*.xml") or find_xml_reports(artifacts_dir)


if __name__ == "__main__":
    cli_main(LANGUAGE, FRAMEWORK, find_reports)
