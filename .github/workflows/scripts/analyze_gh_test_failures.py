#!/usr/bin/env python3
"""
GitHub Actions Test Failure Analyzer

Analyzes GitHub Actions workflow runs, downloads test report artifacts,
and generates a markdown report of failed tests.

Can be used in three modes:
1. Remote analysis: Fetches artifacts from GitHub API
2. Local analysis: Analyzes pre-downloaded artifact directories
3. Auto-detect: Uses GITHUB_* environment variables in Actions context

Usage:
    # Auto-detect in GitHub Actions (uses GITHUB_REPOSITORY and GITHUB_RUN_ID)
    python analyze_gh_test_failures.py --local-artifacts ./test-results
    
    # Remote analysis
    python analyze_gh_test_failures.py <owner/repo> [--token TOKEN] [--run-id RUN_ID] [--artifact-pattern PATTERN]
    
    # Local analysis (artifacts already downloaded)
    python analyze_gh_test_failures.py --local-artifacts /path/to/artifacts

Examples:
    # In GitHub Actions workflow (after downloading artifacts)
    python analyze_gh_test_failures.py --local-artifacts ./test-results --output report.md
    
    # Analyze specific repo/run remotely
    python analyze_gh_test_failures.py mbianchidev/corn-test --run-id 12345678
    
    # Auto-detect repo from environment
    python analyze_gh_test_failures.py --artifact-pattern "surefire"
"""

import argparse
import os
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import json
import re
import urllib.request
import urllib.error


@dataclass
class TestFailure:
    """Represents a single test failure."""
    test_class: str
    test_name: str
    failure_message: str
    failure_type: str
    stack_trace: str
    time_elapsed: float = 0.0


@dataclass
class TestSuiteResult:
    """Represents results from a test suite."""
    name: str
    tests: int
    failures: int
    errors: int
    skipped: int
    time: float
    test_failures: list[TestFailure] = field(default_factory=list)


@dataclass
class WorkflowRunInfo:
    """Information about a workflow run."""
    id: int
    name: str
    head_branch: str
    head_sha: str
    status: str
    conclusion: str
    created_at: str
    html_url: str


import subprocess
import shutil


def gh_cli_available() -> bool:
    """Check if gh CLI is available."""
    return shutil.which("gh") is not None


class GitHubAPI:
    """Simple GitHub API client using urllib or gh CLI."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None, use_gh_cli: bool = True):
        self.use_gh_cli = use_gh_cli and gh_cli_available()
        self.token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        
        if self.use_gh_cli:
            print("Using GitHub CLI for API requests and artifact downloads.")
        elif not self.token:
            print("Warning: No GitHub token provided. API rate limits will be strict.")
            print("Set GITHUB_TOKEN or GH_TOKEN environment variable, or use --token flag.")
    
    def _make_request(self, endpoint: str, accept: str = "application/vnd.github+json") -> bytes:
        """Make a request to the GitHub API."""
        if self.use_gh_cli:
            return self._gh_cli_request(endpoint)
        
        url = f"{self.BASE_URL}{endpoint}" if endpoint.startswith("/") else endpoint
        
        headers = {
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        request = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8', errors='replace')
            raise Exception(f"GitHub API error {e.code}: {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Network error: {e.reason}")
    
    def _gh_cli_request(self, endpoint: str) -> bytes:
        """Make a request using the gh CLI."""
        try:
            result = subprocess.run(
                ["gh", "api", endpoint],
                capture_output=True,
                timeout=60,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"gh CLI error: {e.stderr.decode('utf-8', errors='replace')}")
        except subprocess.TimeoutExpired:
            raise Exception("gh CLI request timed out")
    
    def _get_json(self, endpoint: str) -> dict:
        """Get JSON response from GitHub API."""
        data = self._make_request(endpoint)
        return json.loads(data.decode('utf-8'))
    
    def get_workflow_runs(self, owner: str, repo: str, status: str = "completed", per_page: int = 10) -> list[dict]:
        """Get recent workflow runs for a repository."""
        endpoint = f"/repos/{owner}/{repo}/actions/runs?status={status}&per_page={per_page}"
        response = self._get_json(endpoint)
        return response.get("workflow_runs", [])
    
    def get_workflow_run(self, owner: str, repo: str, run_id: int) -> dict:
        """Get a specific workflow run."""
        endpoint = f"/repos/{owner}/{repo}/actions/runs/{run_id}"
        return self._get_json(endpoint)
    
    def get_artifacts(self, owner: str, repo: str, run_id: int) -> list[dict]:
        """Get artifacts for a workflow run."""
        endpoint = f"/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
        response = self._get_json(endpoint)
        return response.get("artifacts", [])
    
    def download_artifact(self, owner: str, repo: str, artifact_id: int, dest_path: Path, artifact_name: str = "") -> Path:
        """Download an artifact zip file."""
        if self.use_gh_cli:
            return self._download_artifact_gh_cli(owner, repo, artifact_name or str(artifact_id), dest_path)
        
        endpoint = f"/repos/{owner}/{repo}/actions/artifacts/{artifact_id}/zip"
        
        # GitHub redirects to a signed URL for artifact download
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        request = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                content = response.read()
                dest_path.write_bytes(content)
                return dest_path
        except urllib.error.HTTPError as e:
            raise Exception(f"Failed to download artifact: {e.code} {e.reason}")
    
    def _download_artifact_gh_cli(self, owner: str, repo: str, artifact_name: str, dest_path: Path) -> Path:
        """Download artifact using gh CLI."""
        try:
            # gh run download downloads to current directory, so we work in dest_path parent
            dest_dir = dest_path.parent
            result = subprocess.run(
                ["gh", "run", "download", "-R", f"{owner}/{repo}", "-n", artifact_name, "-D", str(dest_dir / artifact_name)],
                capture_output=True,
                timeout=120,
                check=True,
            )
            # gh downloads to a folder, we need to zip it for consistency
            extracted_dir = dest_dir / artifact_name
            if extracted_dir.is_dir():
                # Create a zip from the extracted content
                import shutil
                shutil.make_archive(str(dest_path.with_suffix('')), 'zip', extracted_dir)
                return dest_path
            return dest_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"gh CLI download error: {e.stderr.decode('utf-8', errors='replace')}")


class TestReportParser:
    """Parser for various test report formats."""
    
    @staticmethod
    def parse_surefire_xml(xml_path: Path) -> Optional[TestSuiteResult]:
        """Parse a Surefire/JUnit XML test report."""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Handle both <testsuite> and <testsuites> root elements
            if root.tag == "testsuites":
                testsuites = root.findall("testsuite")
            else:
                testsuites = [root] if root.tag == "testsuite" else []
            
            all_failures: list[TestFailure] = []
            total_tests = 0
            total_failures = 0
            total_errors = 0
            total_skipped = 0
            total_time = 0.0
            suite_name = ""
            
            for testsuite in testsuites:
                suite_name = testsuite.get("name", "Unknown")
                total_tests += int(testsuite.get("tests", 0))
                total_failures += int(testsuite.get("failures", 0))
                total_errors += int(testsuite.get("errors", 0))
                total_skipped += int(testsuite.get("skipped", 0))
                total_time += float(testsuite.get("time", 0))
                
                for testcase in testsuite.findall("testcase"):
                    test_name = testcase.get("name", "Unknown")
                    test_class = testcase.get("classname", suite_name)
                    time_elapsed = float(testcase.get("time", 0))
                    
                    # Check for failures
                    failure = testcase.find("failure")
                    if failure is not None:
                        all_failures.append(TestFailure(
                            test_class=test_class,
                            test_name=test_name,
                            failure_message=failure.get("message", "No message"),
                            failure_type=failure.get("type", "Unknown"),
                            stack_trace=failure.text or "",
                            time_elapsed=time_elapsed,
                        ))
                    
                    # Check for errors
                    error = testcase.find("error")
                    if error is not None:
                        all_failures.append(TestFailure(
                            test_class=test_class,
                            test_name=test_name,
                            failure_message=error.get("message", "No message"),
                            failure_type=error.get("type", "Error"),
                            stack_trace=error.text or "",
                            time_elapsed=time_elapsed,
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
        except ET.ParseError as e:
            print(f"Warning: Failed to parse XML {xml_path}: {e}")
            return None
        except Exception as e:
            print(f"Warning: Error processing {xml_path}: {e}")
            return None
    
    @staticmethod
    def parse_surefire_txt(txt_path: Path) -> Optional[TestSuiteResult]:
        """Parse a Surefire plain text test report."""
        try:
            content = txt_path.read_text(encoding='utf-8', errors='replace')
            
            # Extract test set name
            name_match = re.search(r"Test set:\s+(.+)", content)
            suite_name = name_match.group(1).strip() if name_match else txt_path.stem
            
            # Extract summary line
            summary_match = re.search(
                r"Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+),\s*Skipped:\s*(\d+)",
                content
            )
            
            if not summary_match:
                return None
            
            tests = int(summary_match.group(1))
            failures = int(summary_match.group(2))
            errors = int(summary_match.group(3))
            skipped = int(summary_match.group(4))
            
            # If no failures, return early
            if failures == 0 and errors == 0:
                return TestSuiteResult(
                    name=suite_name,
                    tests=tests,
                    failures=failures,
                    errors=errors,
                    skipped=skipped,
                    time=0.0,
                    test_failures=[],
                )
            
            # Parse failures from text - look for FAILURE! markers
            failure_pattern = re.compile(
                r"([\w.]+)\s+Time elapsed:\s*([\d.]+)\s*s\s*<<<\s*FAILURE!\s*\n"
                r"(org\.\w+\.\w+):\s*(.+?)(?=\n\s+at|\n\n|\Z)",
                re.MULTILINE | re.DOTALL
            )
            
            test_failures: list[TestFailure] = []
            for match in failure_pattern.finditer(content):
                test_full_name = match.group(1)
                time_elapsed = float(match.group(2))
                failure_type = match.group(3)
                failure_message = match.group(4).strip()
                
                # Split class and method name
                if "." in test_full_name:
                    parts = test_full_name.rsplit(".", 1)
                    test_class = parts[0]
                    test_name = parts[1] if len(parts) > 1 else test_full_name
                else:
                    test_class = suite_name
                    test_name = test_full_name
                
                test_failures.append(TestFailure(
                    test_class=test_class,
                    test_name=test_name,
                    failure_message=failure_message,
                    failure_type=failure_type,
                    stack_trace="",  # Full stack trace not easily extractable from txt
                    time_elapsed=time_elapsed,
                ))
            
            return TestSuiteResult(
                name=suite_name,
                tests=tests,
                failures=failures,
                errors=errors,
                skipped=skipped,
                time=0.0,
                test_failures=test_failures,
            )
        except Exception as e:
            print(f"Warning: Error processing {txt_path}: {e}")
            return None


class TestFailureAnalyzer:
    """Main analyzer that orchestrates fetching and parsing test reports."""
    
    def __init__(self, github_api: GitHubAPI):
        self.api = github_api
        self.parser = TestReportParser()
    
    def find_test_artifacts(self, artifacts: list[dict], pattern: str = "") -> list[dict]:
        """Filter artifacts that likely contain test reports."""
        test_artifact_patterns = [
            "test", "surefire", "junit", "report", "coverage", "results"
        ]
        
        matching = []
        for artifact in artifacts:
            name = artifact.get("name", "").lower()
            
            # If pattern specified, use it
            if pattern:
                if pattern.lower() in name:
                    matching.append(artifact)
            else:
                # Otherwise use common patterns
                if any(p in name for p in test_artifact_patterns):
                    matching.append(artifact)
        
        return matching
    
    def parse_test_reports_in_dir(self, report_dir: Path) -> list[TestSuiteResult]:
        """Parse test reports directly from a directory (no extraction needed)."""
        results: list[TestSuiteResult] = []
        
        # Find and parse all XML test reports
        for xml_file in report_dir.rglob("*.xml"):
            # Skip non-test files
            if not any(x in xml_file.name.lower() for x in ["test", "surefire", "junit"]):
                try:
                    content = xml_file.read_text(encoding='utf-8', errors='replace')[:500]
                    if "<testsuite" not in content and "<testsuites" not in content:
                        continue
                except:
                    continue
            
            result = self.parser.parse_surefire_xml(xml_file)
            if result:
                results.append(result)
        
        # Also parse TXT reports
        for txt_file in report_dir.rglob("*.txt"):
            result = self.parser.parse_surefire_txt(txt_file)
            if result and result.test_failures:
                existing_names = {(f.test_class, f.test_name) for r in results for f in r.test_failures}
                new_failures = [f for f in result.test_failures 
                               if (f.test_class, f.test_name) not in existing_names]
                if new_failures:
                    result.test_failures = new_failures
                    results.append(result)
        
        return results
    
    def extract_and_parse_artifact(self, zip_path: Path, extract_dir: Path) -> list[TestSuiteResult]:
        """Extract artifact zip and parse test reports."""
        results: list[TestSuiteResult] = []
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_dir)
        except zipfile.BadZipFile:
            print(f"Warning: {zip_path} is not a valid zip file")
            return results
        
        return self.parse_test_reports_in_dir(extract_dir)
    
    def analyze_run(self, owner: str, repo: str, run_id: int, artifact_pattern: str = "") -> tuple[WorkflowRunInfo, list[TestSuiteResult]]:
        """Analyze a specific workflow run."""
        # Get run info
        run_data = self.api.get_workflow_run(owner, repo, run_id)
        run_info = WorkflowRunInfo(
            id=run_data["id"],
            name=run_data.get("name", "Unknown"),
            head_branch=run_data.get("head_branch", "Unknown"),
            head_sha=run_data.get("head_sha", "")[:7],
            status=run_data.get("status", "Unknown"),
            conclusion=run_data.get("conclusion", "Unknown"),
            created_at=run_data.get("created_at", ""),
            html_url=run_data.get("html_url", ""),
        )
        
        # Get artifacts
        artifacts = self.api.get_artifacts(owner, repo, run_id)
        test_artifacts = self.find_test_artifacts(artifacts, artifact_pattern)
        
        if not test_artifacts:
            print(f"No test artifacts found for run {run_id}")
            if artifacts:
                print(f"Available artifacts: {[a.get('name') for a in artifacts]}")
            return run_info, []
        
        print(f"Found {len(test_artifacts)} test artifact(s): {[a.get('name') for a in test_artifacts]}")
        
        all_results: list[TestSuiteResult] = []
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            for artifact in test_artifacts:
                artifact_id = artifact["id"]
                artifact_name = artifact.get("name", f"artifact_{artifact_id}")
                
                print(f"Downloading artifact: {artifact_name}...")
                zip_path = temp_path / f"{artifact_name}.zip"
                extract_dir = temp_path / artifact_name
                extract_dir.mkdir(exist_ok=True)
                
                try:
                    self.api.download_artifact(owner, repo, artifact_id, zip_path, artifact_name)
                    # Check if gh CLI downloaded directly to folder
                    if extract_dir.exists() and any(extract_dir.iterdir()):
                        results = self.parse_test_reports_in_dir(extract_dir)
                    elif zip_path.exists():
                        results = self.extract_and_parse_artifact(zip_path, extract_dir)
                    else:
                        print(f"Warning: No files found for artifact {artifact_name}")
                        results = []
                    all_results.extend(results)
                except Exception as e:
                    print(f"Warning: Failed to process artifact {artifact_name}: {e}")
        
        return run_info, all_results
    
    def find_failed_run(self, owner: str, repo: str) -> Optional[int]:
        """Find the most recent failed workflow run."""
        # First check for failed runs
        runs = self.api.get_workflow_runs(owner, repo, status="completed", per_page=20)
        
        for run in runs:
            if run.get("conclusion") == "failure":
                return run["id"]
        
        # If no failed runs, return the most recent completed run
        if runs:
            print("No failed runs found. Using most recent completed run.")
            return runs[0]["id"]
        
        return None


def generate_markdown_report(
    repo: str,
    run_info: WorkflowRunInfo,
    results: list[TestSuiteResult],
    output_path: Path
) -> None:
    """Generate a markdown report of test failures."""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Count totals
    total_tests = sum(r.tests for r in results)
    total_failures = sum(r.failures for r in results)
    total_errors = sum(r.errors for r in results)
    total_skipped = sum(r.skipped for r in results)
    all_failures = [f for r in results for f in r.test_failures]
    
    lines = [
        f"# Test Failure Report",
        f"",
        f"**Repository:** `{repo}`  ",
        f"**Generated:** {now}  ",
        f"",
        f"## Workflow Run Information",
        f"",
        f"| Property | Value |",
        f"|----------|-------|",
        f"| Run ID | [{run_info.id}]({run_info.html_url}) |",
        f"| Workflow | {run_info.name} |",
        f"| Branch | `{run_info.head_branch}` |",
        f"| Commit | `{run_info.head_sha}` |",
        f"| Status | {run_info.status} |",
        f"| Conclusion | **{run_info.conclusion}** |",
        f"| Created | {run_info.created_at} |",
        f"",
        f"## Test Summary",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total Tests | {total_tests} |",
        f"| Passed | {total_tests - total_failures - total_errors - total_skipped} |",
        f"| Failed | **{total_failures}** |",
        f"| Errors | {total_errors} |",
        f"| Skipped | {total_skipped} |",
        f"",
    ]
    
    if not all_failures:
        lines.extend([
            f"## Result",
            f"",
            f"✅ **All tests passed!** No failures detected.",
            f"",
        ])
    else:
        lines.extend([
            f"## Failed Tests ({len(all_failures)} failures)",
            f"",
        ])
        
        # Group failures by class
        failures_by_class: dict[str, list[TestFailure]] = {}
        for failure in all_failures:
            if failure.test_class not in failures_by_class:
                failures_by_class[failure.test_class] = []
            failures_by_class[failure.test_class].append(failure)
        
        for test_class, failures in failures_by_class.items():
            lines.extend([
                f"### `{test_class}`",
                f"",
            ])
            
            for i, failure in enumerate(failures, 1):
                lines.extend([
                    f"#### {i}. `{failure.test_name}`",
                    f"",
                    f"**Type:** `{failure.failure_type}`  ",
                    f"**Time:** {failure.time_elapsed:.3f}s  ",
                    f"",
                    f"**Message:**",
                    f"```",
                    f"{failure.failure_message}",
                    f"```",
                    f"",
                ])
                
                if failure.stack_trace:
                    # Truncate very long stack traces
                    stack_lines = failure.stack_trace.strip().split('\n')
                    if len(stack_lines) > 15:
                        stack_display = '\n'.join(stack_lines[:15]) + f"\n... ({len(stack_lines) - 15} more lines)"
                    else:
                        stack_display = failure.stack_trace.strip()
                    
                    lines.extend([
                        f"<details>",
                        f"<summary>Stack Trace</summary>",
                        f"",
                        f"```",
                        f"{stack_display}",
                        f"```",
                        f"",
                        f"</details>",
                        f"",
                    ])
        
        # Add quick reference table
        lines.extend([
            f"## Quick Reference",
            f"",
            f"| # | Test Class | Test Method | Error Type |",
            f"|---|------------|-------------|------------|",
        ])
        
        for i, failure in enumerate(all_failures, 1):
            short_class = failure.test_class.split('.')[-1]
            short_type = failure.failure_type.split('.')[-1]
            lines.append(f"| {i} | `{short_class}` | `{failure.test_name}` | `{short_type}` |")
        
        lines.append("")
    
    # Write to file
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"\n✅ Report generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze GitHub Actions test failures from workflow artifacts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect from GitHub Actions environment
  %(prog)s
  
  # Analyze specific repository
  %(prog)s owner/repo
  %(prog)s owner/repo --run-id 12345678
  %(prog)s owner/repo --artifact-pattern surefire
  
  # Analyze local artifact directory (downloaded in workflow)
  %(prog)s --local-artifacts ./test-results
  
  # Use with explicit token
  %(prog)s owner/repo --token ghp_xxxx --output results.md
        """
    )
    
    parser.add_argument(
        "repo",
        nargs="?",
        default=None,
        help="Repository in 'owner/repo' format (auto-detected from GITHUB_REPOSITORY if omitted)"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (or set GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--run-id",
        type=int,
        help="Specific workflow run ID to analyze (auto-detected from GITHUB_RUN_ID if omitted)"
    )
    parser.add_argument(
        "--artifact-pattern",
        default="",
        help="Pattern to match artifact names (default: auto-detect test artifacts)"
    )
    parser.add_argument(
        "--local-artifacts",
        help="Path to local artifacts directory (skip download, analyze local files)"
    )
    parser.add_argument(
        "--output",
        default="test-failure-report.md",
        help="Output markdown file path (default: test-failure-report.md)"
    )
    
    args = parser.parse_args()
    
    # Auto-detect from GitHub Actions environment
    repo_full = args.repo or os.environ.get("GITHUB_REPOSITORY")
    run_id = args.run_id or (int(os.environ.get("GITHUB_RUN_ID", 0)) or None)
    
    # Handle local artifacts mode
    if args.local_artifacts:
        local_path = Path(args.local_artifacts)
        if not local_path.exists():
            print(f"Error: Local artifacts path does not exist: {local_path}")
            sys.exit(1)
        
        print(f"Analyzing local artifacts at: {local_path}")
        
        # Create a minimal API just for run info if needed
        api = GitHubAPI(token=args.token) if repo_full and run_id else None
        analyzer = TestFailureAnalyzer(api) if api else TestFailureAnalyzer(GitHubAPI(token=args.token, use_gh_cli=False))
        
        # Parse local directory
        results = analyzer.parse_test_reports_in_dir(local_path)
        
        # Create run info from environment or defaults
        if repo_full and run_id and api:
            try:
                owner, repo = repo_full.split("/", 1)
                run_data = api.get_workflow_run(owner, repo, run_id)
                run_info = WorkflowRunInfo(
                    id=run_data["id"],
                    name=run_data.get("name", "Unknown"),
                    head_branch=run_data.get("head_branch", os.environ.get("GITHUB_REF_NAME", "Unknown")),
                    head_sha=run_data.get("head_sha", os.environ.get("GITHUB_SHA", ""))[:7],
                    status=run_data.get("status", "Unknown"),
                    conclusion=run_data.get("conclusion", "Unknown"),
                    created_at=run_data.get("created_at", ""),
                    html_url=run_data.get("html_url", ""),
                )
            except Exception as e:
                print(f"Warning: Could not fetch run info: {e}")
                run_info = WorkflowRunInfo(
                    id=run_id or 0,
                    name=os.environ.get("GITHUB_WORKFLOW", "Unknown"),
                    head_branch=os.environ.get("GITHUB_REF_NAME", "Unknown"),
                    head_sha=os.environ.get("GITHUB_SHA", "")[:7] if os.environ.get("GITHUB_SHA") else "",
                    status="completed",
                    conclusion="failure",
                    created_at=datetime.now().isoformat(),
                    html_url=f"https://github.com/{repo_full}/actions/runs/{run_id}" if repo_full and run_id else "",
                )
        else:
            run_info = WorkflowRunInfo(
                id=run_id or 0,
                name=os.environ.get("GITHUB_WORKFLOW", "Local Analysis"),
                head_branch=os.environ.get("GITHUB_REF_NAME", "local"),
                head_sha=os.environ.get("GITHUB_SHA", "")[:7] if os.environ.get("GITHUB_SHA") else "local",
                status="completed",
                conclusion="failure",
                created_at=datetime.now().isoformat(),
                html_url="",
            )
        
        # Generate report
        output_path = Path(args.output)
        generate_markdown_report(repo_full or "local/repo", run_info, results, output_path)
        
        # Print summary
        all_failures = [f for r in results for f in r.test_failures]
        if all_failures:
            print(f"\n📊 Summary: {len(all_failures)} test failure(s) found")
            for f in all_failures[:5]:
                print(f"   ❌ {f.test_class}.{f.test_name}")
            if len(all_failures) > 5:
                print(f"   ... and {len(all_failures) - 5} more")
        else:
            print("\n✅ No test failures found!")
        return
    
    # Remote analysis mode - require repo
    if not repo_full:
        print("Error: Repository must be provided via argument or GITHUB_REPOSITORY environment variable")
        sys.exit(1)
    
    if "/" not in repo_full:
        print(f"Error: Repository must be in 'owner/repo' format, got: {repo_full}")
        sys.exit(1)
    
    owner, repo = repo_full.split("/", 1)
    
    # Initialize
    api = GitHubAPI(token=args.token)
    analyzer = TestFailureAnalyzer(api)
    
    # Find run to analyze
    if not run_id:
        print(f"Finding most recent failed run for {repo_full}...")
        run_id = analyzer.find_failed_run(owner, repo)
        if not run_id:
            print("No workflow runs found for this repository.")
            sys.exit(1)
    
    print(f"Analyzing workflow run: {run_id}")
    
    # Analyze
    try:
        run_info, results = analyzer.analyze_run(owner, repo, run_id, args.artifact_pattern)
    except Exception as e:
        print(f"Error analyzing run: {e}")
        sys.exit(1)
    
    # Generate report
    output_path = Path(args.output)
    generate_markdown_report(repo_full, run_info, results, output_path)
    
    # Print summary
    all_failures = [f for r in results for f in r.test_failures]
    if all_failures:
        print(f"\n📊 Summary: {len(all_failures)} test failure(s) found")
        for f in all_failures[:5]:  # Show first 5
            print(f"   ❌ {f.test_class}.{f.test_name}")
        if len(all_failures) > 5:
            print(f"   ... and {len(all_failures) - 5} more")
    else:
        print("\n✅ No test failures found!")


if __name__ == "__main__":
    main()
