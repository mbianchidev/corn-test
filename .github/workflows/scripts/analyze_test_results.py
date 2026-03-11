#!/usr/bin/env python3
"""
Multi-framework test result analyzer.

Dispatches to framework-specific parsers to produce unified JUnit XML analysis.
Supports: JUnit (Java/Kotlin), pytest, unittest, Jest, Playwright, Go testing,
xUnit.net, Cargo test, Google Test, Unity (C), Swift Testing, PHPUnit, RSpec,
ExUnit, Dart test.

Usage:
    python analyze_test_results.py <language> <reports_dir>
    python analyze_test_results.py --all <root_dir>
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestResult:
    """A single test case result."""
    name: str
    classname: str
    time: float = 0.0
    status: str = "passed"  # passed, failed, error, skipped
    message: str = ""


@dataclass
class SuiteResult:
    """Results from a test suite."""
    name: str
    framework: str
    language: str
    tests: int = 0
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    time: float = 0.0
    test_results: list = field(default_factory=list)


def parse_junit_xml(xml_path: str, framework: str, language: str) -> SuiteResult:
    """Parse a standard JUnit XML report file."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Warning: Could not parse {xml_path}: {e}", file=sys.stderr)
        return SuiteResult(name=Path(xml_path).stem, framework=framework, language=language)

    # Handle both <testsuites> and <testsuite> root elements
    if root.tag == "testsuites":
        suites = root.findall("testsuite")
    elif root.tag == "testsuite":
        suites = [root]
    else:
        return SuiteResult(name=Path(xml_path).stem, framework=framework, language=language)

    all_results = []
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_time = 0.0

    for suite in suites:
        total_tests += int(suite.get("tests", 0))
        total_failures += int(suite.get("failures", 0))
        total_errors += int(suite.get("errors", 0))
        total_skipped += int(suite.get("skipped", 0))
        total_time += float(suite.get("time", 0))

        for testcase in suite.findall("testcase"):
            result = TestResult(
                name=testcase.get("name", "unknown"),
                classname=testcase.get("classname", "unknown"),
                time=float(testcase.get("time", 0)),
            )

            failure = testcase.find("failure")
            error = testcase.find("error")
            skipped_el = testcase.find("skipped")

            if failure is not None:
                result.status = "failed"
                result.message = failure.get("message", failure.text or "")
            elif error is not None:
                result.status = "error"
                result.message = error.get("message", error.text or "")
            elif skipped_el is not None:
                result.status = "skipped"

            all_results.append(result)

    return SuiteResult(
        name=Path(xml_path).stem,
        framework=framework,
        language=language,
        tests=total_tests,
        failures=total_failures,
        errors=total_errors,
        skipped=total_skipped,
        time=total_time,
        test_results=all_results,
    )


# --- Framework-specific analyzers ---

FRAMEWORK_MAP = {
    "java": {"frameworks": ["junit"], "pattern": "TEST-*.xml", "subdir": "surefire-reports"},
    "python": {"frameworks": ["pytest", "pyunit"], "pattern": "*-results.xml", "subdir": "reports"},
    "typescript": {"frameworks": ["jest", "playwright"], "pattern": "*-results.xml", "subdir": "reports"},
    "golang": {"frameworks": ["go-testing"], "pattern": "*-results.xml", "subdir": "reports"},
    "csharp": {"frameworks": ["xunit"], "pattern": "*-results.xml", "subdir": "reports"},
    "rust": {"frameworks": ["cargo-test"], "pattern": "*-results.xml", "subdir": "reports"},
    "cpp": {"frameworks": ["gtest"], "pattern": "*-results.xml", "subdir": "reports"},
    "c": {"frameworks": ["unity"], "pattern": "*-results.xml", "subdir": "reports"},
    "swift": {"frameworks": ["swift-testing"], "pattern": "*.txt", "subdir": "reports"},
    "kotlin": {"frameworks": ["kotlin-test"], "pattern": "*.xml", "subdir": "build/test-results"},
    "php": {"frameworks": ["phpunit"], "pattern": "*-results.xml", "subdir": "reports"},
    "ruby": {"frameworks": ["rspec"], "pattern": "*-results.xml", "subdir": "reports"},
    "elixir": {"frameworks": ["exunit"], "pattern": "*-results.xml", "subdir": "reports"},
    "dart": {"frameworks": ["dart-test"], "pattern": "*-results.xml", "subdir": "reports"},
}


def find_report_files(base_dir: str, language: str) -> list[str]:
    """Find test report files for a given language."""
    config = FRAMEWORK_MAP.get(language, {})
    pattern = config.get("pattern", "*.xml")
    subdir = config.get("subdir", "reports")

    report_dir = Path(base_dir) / subdir
    if not report_dir.exists():
        report_dir = Path(base_dir)

    return sorted(str(p) for p in report_dir.glob(pattern))


def analyze_language(language: str, reports_dir: str) -> list[SuiteResult]:
    """Analyze test reports for a specific language."""
    config = FRAMEWORK_MAP.get(language)
    if not config:
        print(f"Unsupported language: {language}", file=sys.stderr)
        return []

    report_files = find_report_files(reports_dir, language)
    if not report_files:
        print(f"No report files found for {language} in {reports_dir}", file=sys.stderr)
        return []

    results = []
    for report_file in report_files:
        framework = config["frameworks"][0]
        # Try to detect specific framework from filename
        for fw in config["frameworks"]:
            if fw in Path(report_file).stem.lower():
                framework = fw
                break
        results.append(parse_junit_xml(report_file, framework, language))

    return results


def generate_markdown_report(all_results: list[SuiteResult]) -> str:
    """Generate a markdown summary report."""
    lines = ["# Test Results Summary\n"]

    for result in all_results:
        passed = result.tests - result.failures - result.errors - result.skipped
        lines.append(f"## {result.language.title()} — {result.framework}")
        lines.append(f"- **Tests**: {result.tests}")
        lines.append(f"- **Passed**: {passed}")
        lines.append(f"- **Failed**: {result.failures}")
        lines.append(f"- **Errors**: {result.errors}")
        lines.append(f"- **Skipped**: {result.skipped}")
        lines.append(f"- **Time**: {result.time:.3f}s")
        lines.append("")

        failed_tests = [t for t in result.test_results if t.status in ("failed", "error")]
        if failed_tests:
            lines.append("### Failed Tests")
            for t in failed_tests:
                lines.append(f"- `{t.classname}.{t.name}` — {t.message[:200]}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Multi-framework test result analyzer")
    parser.add_argument("language", nargs="?", help="Language to analyze")
    parser.add_argument("reports_dir", nargs="?", help="Reports directory")
    parser.add_argument("--all", metavar="ROOT_DIR", help="Analyze all languages from root directory")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    all_results = []

    if args.all:
        root = Path(args.all)
        for lang in FRAMEWORK_MAP:
            lang_dir = root / lang
            if lang_dir.exists():
                all_results.extend(analyze_language(lang, str(lang_dir)))
    elif args.language and args.reports_dir:
        all_results = analyze_language(args.language, args.reports_dir)
    else:
        parser.print_help()
        sys.exit(1)

    report = generate_markdown_report(all_results)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
