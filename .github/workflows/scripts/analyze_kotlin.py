#!/usr/bin/env python3
"""Kotlin test result analyzer for corn-flakes-detection.

Parses Gradle kotlin.test JUnit XML reports from ``build/test-results/``.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _report_utils import cli_main, find_xml_reports  # noqa: E402

LANGUAGE = "Kotlin"
FRAMEWORK = "kotlin.test"


def find_reports(artifacts_dir: Path) -> list[Path]:
    """Find Kotlin Gradle test report XML files."""
    # Gradle puts results in build/test-results/test/
    for d in artifacts_dir.rglob("test-results"):
        xmls = sorted(d.rglob("*.xml"))
        if xmls:
            return xmls
    # Fallback
    return find_xml_reports(artifacts_dir)


if __name__ == "__main__":
    cli_main(LANGUAGE, FRAMEWORK, find_reports)
