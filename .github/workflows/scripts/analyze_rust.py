#!/usr/bin/env python3
"""Rust test result analyzer for corn-flakes-detection.

Parses cargo2junit JUnit XML reports from ``reports/``.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _report_utils import cli_main, find_xml_reports  # noqa: E402

LANGUAGE = "Rust"
FRAMEWORK = "cargo test"


def find_reports(artifacts_dir: Path) -> list[Path]:
    """Find Rust test report XML files."""
    reports = find_xml_reports(artifacts_dir, "rust-test-results.xml")
    if reports:
        return reports
    reports = find_xml_reports(artifacts_dir, "*-results.xml")
    if reports:
        return reports
    return find_xml_reports(artifacts_dir)


if __name__ == "__main__":
    cli_main(LANGUAGE, FRAMEWORK, find_reports)
