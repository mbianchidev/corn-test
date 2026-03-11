#!/usr/bin/env python3
"""Python test result analyzer for corn-flakes-detection.

Parses pytest and unittest JUnit XML reports from ``reports/``.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _report_utils import cli_main, find_xml_reports  # noqa: E402

LANGUAGE = "Python"
FRAMEWORK = "pytest + unittest"


def find_reports(artifacts_dir: Path) -> list[Path]:
    """Find Python test report XML files."""
    # Look for pytest-results.xml, pyunit-results.xml
    reports = find_xml_reports(artifacts_dir, "*-results.xml")
    if reports:
        return reports
    # Fallback
    return find_xml_reports(artifacts_dir)


if __name__ == "__main__":
    cli_main(LANGUAGE, FRAMEWORK, find_reports)
