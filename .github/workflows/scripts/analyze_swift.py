#!/usr/bin/env python3
"""Swift test result analyzer for corn-flakes-detection.

Parses Swift Testing / XCTest text output from ``reports/``.
Swift does not produce JUnit XML by default, so this script parses
the plain-text output captured by ``swift test 2>&1 | tee reports/swift-test-output.txt``.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _report_utils import cli_main, parse_swift_text  # noqa: E402

LANGUAGE = "Swift"
FRAMEWORK = "Swift Testing"


def find_reports(artifacts_dir: Path) -> list[Path]:
    """Find Swift test output files."""
    # Look for text output files first
    txts = sorted(artifacts_dir.rglob("*.txt"))
    if txts:
        return txts
    # Some setups may produce XML
    xmls = sorted(artifacts_dir.rglob("*.xml"))
    return xmls


if __name__ == "__main__":
    cli_main(LANGUAGE, FRAMEWORK, find_reports, parse_fn=parse_swift_text)
