#!/usr/bin/env python3
"""
Shared utilities for per-language test result analyzers.

Provides:
- JUnit XML parsing (handles <testsuites> and <testsuite> roots)
- Swift text output parsing
- Standardized markdown report generation
- Common CLI argument handling

All per-language analyzer scripts import from this module to ensure
a consistent output format across languages.
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# Data classes — shared across all analyzers
# ---------------------------------------------------------------------------

@dataclass
class TestFailure:
    """Represents a single test failure or error."""
    test_class: str
    test_name: str
    failure_message: str
    failure_type: str
    stack_trace: str = ""
    time_elapsed: float = 0.0


@dataclass
class TestSuiteResult:
    """Aggregated results from one or more test suites in a report file."""
    name: str
    tests: int = 0
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    time: float = 0.0
    test_failures: list[TestFailure] = field(default_factory=list)


# ---------------------------------------------------------------------------
# JUnit XML parser — works for all frameworks that emit JUnit XML
# ---------------------------------------------------------------------------

def parse_junit_xml(xml_path: Path) -> Optional[TestSuiteResult]:
    """Parse a JUnit/Surefire/xUnit XML test report.

    Handles both ``<testsuites>`` (wrapper) and ``<testsuite>`` root elements,
    which covers Maven Surefire, pytest --junitxml, jest-junit, gotestsum,
    cargo2junit, CTest --output-junit, PHPUnit, RSpec, ExUnit and Dart.
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Warning: Could not parse {xml_path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Warning: Error reading {xml_path}: {e}", file=sys.stderr)
        return None

    if root.tag == "testsuites":
        suites = root.findall("testsuite")
    elif root.tag == "testsuite":
        suites = [root]
    else:
        return None

    all_failures: list[TestFailure] = []
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_time = 0.0
    suite_name = Path(xml_path).stem

    for suite in suites:
        suite_name = suite.get("name", suite_name)
        total_tests += int(suite.get("tests", 0))
        total_failures += int(suite.get("failures", 0))
        total_errors += int(suite.get("errors", 0))
        total_skipped += int(suite.get("skipped", 0))
        total_time += float(suite.get("time", 0))

        for testcase in suite.findall("testcase"):
            tc_name = testcase.get("name", "unknown")
            tc_class = testcase.get("classname", suite_name)
            tc_time = float(testcase.get("time", 0))

            failure = testcase.find("failure")
            if failure is not None:
                all_failures.append(TestFailure(
                    test_class=tc_class,
                    test_name=tc_name,
                    failure_message=failure.get("message", failure.text or "No message"),
                    failure_type=failure.get("type", "Failure"),
                    stack_trace=failure.text or "",
                    time_elapsed=tc_time,
                ))

            error = testcase.find("error")
            if error is not None:
                all_failures.append(TestFailure(
                    test_class=tc_class,
                    test_name=tc_name,
                    failure_message=error.get("message", error.text or "No message"),
                    failure_type=error.get("type", "Error"),
                    stack_trace=error.text or "",
                    time_elapsed=tc_time,
                ))

    if total_tests == 0 and not all_failures:
        return None

    return TestSuiteResult(
        name=suite_name,
        tests=total_tests,
        failures=total_failures,
        errors=total_errors,
        skipped=total_skipped,
        time=total_time,
        test_failures=all_failures,
    )


# ---------------------------------------------------------------------------
# Swift text output parser
# ---------------------------------------------------------------------------

_SWIFT_TESTCASE = re.compile(
    r"Test Case\s+['\"]?-\[(\S+)\s+(\S+)\]['\"]?\s+(passed|failed)\s+\((\d+\.\d+)\s+seconds\)"
)
_SWIFT_SUMMARY = re.compile(
    r"Executed\s+(\d+)\s+tests?,\s+with\s+(\d+)\s+failures?\s+\((\d+)\s+unexpected\)"
)
_SWIFT_FAILURE_MSG = re.compile(
    r"(.*?\.swift:\d+):\s*error:\s*-\[(\S+)\s+(\S+)\]\s*:\s*(.*)"
)
# Swift Testing framework markers (◇, ✔, ✘)
_SWIFT_TESTING_PASS = re.compile(r"[✔✓]\s+Test\s+(\S+)\s+passed\s+after\s+(\d+\.\d+)\s+seconds")
_SWIFT_TESTING_FAIL = re.compile(r"[✘✗]\s+Test\s+(\S+)\s+failed\s+after\s+(\d+\.\d+)\s+seconds")
_SWIFT_TESTING_ERR = re.compile(r"\s+[▷▶]\s+(.*)")


def parse_swift_text(txt_path: Path) -> Optional[TestSuiteResult]:
    """Parse Swift ``swift test`` text output into a TestSuiteResult."""
    try:
        content = txt_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"Warning: Could not read {txt_path}: {e}", file=sys.stderr)
        return None

    failures: list[TestFailure] = []
    total_tests = 0
    total_failures_count = 0
    total_time = 0.0

    # Collect failure messages indexed by (class, method)
    failure_messages: dict[tuple[str, str], str] = {}
    for m in _SWIFT_FAILURE_MSG.finditer(content):
        cls, method, msg = m.group(2), m.group(3), m.group(4)
        failure_messages[(cls, method)] = msg

    # XCTest-style output
    for m in _SWIFT_TESTCASE.finditer(content):
        cls, method, status, elapsed = m.group(1), m.group(2), m.group(3), float(m.group(4))
        total_tests += 1
        total_time += elapsed
        if status == "failed":
            total_failures_count += 1
            msg = failure_messages.get((cls, method), "Test failed")
            failures.append(TestFailure(
                test_class=cls,
                test_name=method,
                failure_message=msg,
                failure_type="XCTAssertionFailure",
                time_elapsed=elapsed,
            ))

    # Swift Testing framework style (✔/✘)
    if total_tests == 0:
        current_fail: Optional[str] = None
        for line in content.splitlines():
            pm = _SWIFT_TESTING_PASS.search(line)
            if pm:
                total_tests += 1
                total_time += float(pm.group(2))
                current_fail = None
                continue
            fm = _SWIFT_TESTING_FAIL.search(line)
            if fm:
                total_tests += 1
                total_failures_count += 1
                elapsed = float(fm.group(2))
                total_time += elapsed
                test_name = fm.group(1)
                current_fail = test_name
                failures.append(TestFailure(
                    test_class="SwiftTests",
                    test_name=test_name,
                    failure_message="",
                    failure_type="TestFailure",
                    time_elapsed=elapsed,
                ))
                continue
            if current_fail:
                em = _SWIFT_TESTING_ERR.search(line)
                if em and failures:
                    failures[-1].failure_message = em.group(1).strip()
                    current_fail = None

    # Try summary line as a fallback for totals
    for m in _SWIFT_SUMMARY.finditer(content):
        summary_tests = int(m.group(1))
        summary_failures = int(m.group(2))
        if summary_tests > total_tests:
            total_tests = summary_tests
        if summary_failures > total_failures_count:
            total_failures_count = summary_failures

    if total_tests == 0:
        return None

    return TestSuiteResult(
        name=txt_path.stem,
        tests=total_tests,
        failures=total_failures_count,
        errors=0,
        skipped=0,
        time=total_time,
        test_failures=failures,
    )


# ---------------------------------------------------------------------------
# Markdown report generator — identical output format for every language
# ---------------------------------------------------------------------------

def generate_markdown_report(
    language: str,
    framework: str,
    results: list[TestSuiteResult],
    output_path: Optional[Path] = None,
) -> str:
    """Generate a standardised markdown test-failure report.

    The format matches ``analyze_gh_test_failures.py`` so the agentic
    workflow's prompt can parse it with the same extraction rules.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_tests = sum(r.tests for r in results)
    total_failures = sum(r.failures for r in results)
    total_errors = sum(r.errors for r in results)
    total_skipped = sum(r.skipped for r in results)
    all_failures = [f for r in results for f in r.test_failures]

    lines: list[str] = [
        f"# Test Failure Report — {language} ({framework})",
        "",
        f"**Generated:** {now}  ",
        "",
        "## Test Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total Tests | {total_tests} |",
        f"| Passed | {total_tests - total_failures - total_errors - total_skipped} |",
        f"| Failed | **{total_failures}** |",
        f"| Errors | {total_errors} |",
        f"| Skipped | {total_skipped} |",
        "",
    ]

    if not all_failures:
        lines += [
            "## Result",
            "",
            "✅ **All tests passed!** No failures detected.",
            "",
        ]
    else:
        lines += [
            f"## Failed Tests ({len(all_failures)} failures)",
            "",
        ]

        # Group by class
        by_class: dict[str, list[TestFailure]] = {}
        for f in all_failures:
            by_class.setdefault(f.test_class, []).append(f)

        for test_class, class_failures in by_class.items():
            lines += [f"### `{test_class}`", ""]
            for i, f in enumerate(class_failures, 1):
                lines += [
                    f"#### {i}. `{f.test_name}`",
                    "",
                    f"**Type:** `{f.failure_type}`  ",
                    f"**Time:** {f.time_elapsed:.3f}s  ",
                    "",
                    "**Message:**",
                    "```",
                    f.failure_message,
                    "```",
                    "",
                ]
                if f.stack_trace:
                    trace_lines = f.stack_trace.strip().splitlines()
                    if len(trace_lines) > 15:
                        trace = "\n".join(trace_lines[:15]) + f"\n... ({len(trace_lines) - 15} more lines)"
                    else:
                        trace = f.stack_trace.strip()
                    lines += [
                        "<details>",
                        "<summary>Stack Trace</summary>",
                        "",
                        "```",
                        trace,
                        "```",
                        "",
                        "</details>",
                        "",
                    ]

        # Quick reference table
        lines += [
            "## Quick Reference",
            "",
            "| # | Test Class | Test Method | Error Type |",
            "|---|------------|-------------|------------|",
        ]
        for i, f in enumerate(all_failures, 1):
            short_class = f.test_class.rsplit(".", 1)[-1]
            short_type = f.failure_type.rsplit(".", 1)[-1]
            lines.append(f"| {i} | `{short_class}` | `{f.test_name}` | `{short_type}` |")
        lines.append("")

    report = "\n".join(lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"✅ Report generated: {output_path}")

    return report


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def find_xml_reports(base_dir: Path, pattern: str = "*.xml") -> list[Path]:
    """Recursively find XML files matching *pattern* under *base_dir*."""
    if not base_dir.exists():
        return []
    return sorted(base_dir.rglob(pattern))


def find_test_xml_reports(base_dir: Path) -> list[Path]:
    """Find XML files that look like JUnit test reports."""
    candidates = find_xml_reports(base_dir)
    results: list[Path] = []
    for p in candidates:
        # Quick heuristic: check if it contains <testsuite
        try:
            head = p.read_text(encoding="utf-8", errors="replace")[:500]
            if "<testsuite" in head or "<testsuites" in head:
                results.append(p)
        except Exception:
            continue
    return results


# ---------------------------------------------------------------------------
# CLI main — shared entry point for per-language scripts
# ---------------------------------------------------------------------------

ReportFinderFn = Callable[[Path], list[Path]]


def cli_main(
    language: str,
    framework: str,
    find_reports: ReportFinderFn,
    *,
    parse_fn: Optional[Callable[[Path], Optional[TestSuiteResult]]] = None,
) -> None:
    """Common CLI handler used by all per-language analyzer scripts.

    Parameters
    ----------
    language:
        Human-readable language name (e.g. "Java").
    framework:
        Framework name (e.g. "JUnit 5").
    find_reports:
        Callable that, given a base directory ``Path``, returns the list of
        report files for this language.
    parse_fn:
        Optional custom parser. Defaults to ``parse_junit_xml``.
    """
    parser = argparse.ArgumentParser(
        description=f"Analyze {language} ({framework}) test results"
    )
    parser.add_argument(
        "artifacts_dir",
        help="Path to the artifacts directory for this language",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output markdown file path (default: stdout)",
    )
    args = parser.parse_args()

    artifacts = Path(args.artifacts_dir)
    if not artifacts.exists():
        print(f"Error: artifacts directory does not exist: {artifacts}", file=sys.stderr)
        sys.exit(1)

    report_files = find_reports(artifacts)
    if not report_files:
        print(f"No {language} test report files found in {artifacts}", file=sys.stderr)
        # Still generate an empty report so the agent has a consistent file
        report = generate_markdown_report(language, framework, [])
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"✅ Empty report generated: {args.output}")
        else:
            print(report)
        return

    parse = parse_fn or parse_junit_xml
    results: list[TestSuiteResult] = []
    for rf in report_files:
        r = parse(rf)
        if r:
            results.append(r)

    output_path = Path(args.output) if args.output else None
    report = generate_markdown_report(language, framework, results, output_path)

    if not args.output:
        print(report)

    # Print summary to stderr for agent visibility
    all_f = [f for r in results for f in r.test_failures]
    total = sum(r.tests for r in results)
    if all_f:
        print(f"\n📊 {language}: {len(all_f)} failure(s) out of {total} tests", file=sys.stderr)
        for f in all_f[:5]:
            print(f"   ❌ {f.test_class}.{f.test_name}", file=sys.stderr)
        if len(all_f) > 5:
            print(f"   ... and {len(all_f) - 5} more", file=sys.stderr)
    else:
        print(f"\n✅ {language}: All {total} tests passed!", file=sys.stderr)
