---
description: |
  Daily flaky test detection workflow that analyzes test artifacts, creates issues for flaky tests,
  and generates a daily status discussion with metrics and recommendations.

on:
  schedule: daily

timeout-minutes: 75
strict: false

engine:
  id: copilot
  model: claude-sonnet-4.5

permissions:
  actions: read
  contents: read
  attestations: read
  pull-requests: read
  issues: read
  discussions: read

steps:
  - name: Validate auth token
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    run: |
      gh run list --repo "${GITHUB_REPOSITORY}" --workflow=test.yml --limit 1 >/dev/null \
        || { echo "::error::Unable to list test workflow runs with GH_TOKEN. Check GITHUB_TOKEN validity and actions:read permission."; exit 1; }

  - name: Validate GH AW assign-to-agent token
    env:
      GH_TOKEN: ${{ secrets.CORN_GH_AW_ASSIGN_ISSUES_TOKEN }}
    run: |
      if [ -z "${GH_TOKEN:-}" ]; then
        echo "::warning::CORN_GH_AW_ASSIGN_ISSUES_TOKEN is not configured. assign-to-agent output will be skipped if needed."
        exit 0
      fi

      gh api "repos/${GITHUB_REPOSITORY}/issues?per_page=1" >/dev/null \
        || echo "::warning::CORN_GH_AW_ASSIGN_ISSUES_TOKEN is invalid or lacks issue access. assign-to-agent output may be skipped."

  - name: Set up Python
    uses: actions/setup-python@v6
    with:
      python-version: '3.11'
  
  - name: Prepare artifacts directory
    run: mkdir -p ./artifacts ./reports

  - name: Download test artifacts from recent runs
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    run: |
      # Save run metadata for the agent
      gh run list --workflow=test.yml --limit 20 --json databaseId,conclusion,createdAt,name,headSha,headBranch > ./artifacts/runs.json
      # Download test-results artifact for each run
      for RUN_ID in $(python3 -c "import json,sys; [print(r['databaseId']) for r in json.load(sys.stdin)]" < ./artifacts/runs.json); do
        mkdir -p ./artifacts/$RUN_ID
        gh run download "$RUN_ID" -n test-results -D ./artifacts/$RUN_ID 2>>./artifacts/download.log || echo "No test-results artifact for run $RUN_ID" >> ./artifacts/download.log
      done

  - name: Generate per-language analyzer reports
    # Runs the Python analyzers here on the GitHub Actions runner (NOT inside the
    # agent sandbox, which denies python3 execution). The agent then only READS
    # the pre-generated markdown reports under ./reports/, so it never needs
    # python3 itself.
    run: |
      SCRIPTS_DIR=".github/workflows/scripts"
      mkdir -p ./reports
      : > ./reports/analyze.log
      shopt -s nullglob
      for run_dir in ./artifacts/*/; do
        run_id=$(basename "$run_dir")
        for lang_dir in "$run_dir"test-results-*/; do
          [ -d "$lang_dir" ] || continue
          lang=$(basename "$lang_dir")
          lang=${lang#test-results-}
          case "$lang" in
            python) script="analyze_python_tests.py" ;;
            *) script="analyze_${lang}.py" ;;
          esac
          script_path="$SCRIPTS_DIR/$script"
          if [ ! -f "$script_path" ]; then
            echo "No analyzer for language '$lang' (run $run_id), skipping" >> ./reports/analyze.log
            continue
          fi
          out="./reports/${lang}_${run_id}.md"
          if python3 "$script_path" "$lang_dir" -o "$out" >> ./reports/analyze.log 2>&1; then
            echo "OK: $lang run $run_id -> $out" >> ./reports/analyze.log
          else
            echo "FAILED: $lang run $run_id (analyzer error)" >> ./reports/analyze.log
          fi
        done
      done
      echo "Generated reports:" && ls -1 ./reports || true

env:
  GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

network: {}

tools:
  github:
    toolsets: [default, actions]
  bash:
    - "gh run list:*"
    - "gh run view:*"
    - "gh api:*"
    - "cat:*"
    - "ls:*"
    - "mkdir:*"
    - "rm:*"
  cache-memory: true

safe-outputs:
  create-issue:
    title-prefix: "[corn flakes detection] "
    labels: [flaky-test, automated]
    allowed-labels: [flaky-test, automated, daily-summary]
    close-older-issues: false
    max: 51  # 50 for flaky test issues + 1 for daily summary issue
  close-issue:
    required-title-prefix: "[corn flakes detection] "
    target: "*"
    max: 60
  update-issue:
    status:
    target: "*"
    max: 50
    # Use a PAT so that re-opening a closed issue emits an `issues: reopened`
    # event. Actions performed with the default GITHUB_TOKEN do not trigger
    # further workflow runs, which would prevent reopened-issue-handler from
    # running and re-opening linked PRs / re-assigning Copilot.
    github-token: ${{ secrets.CORN_GH_AW_ASSIGN_ISSUES_TOKEN }}
  assign-to-agent:
    name: "copilot"
    target: "*"
    max: 50
    ignore-if-error: true
    github-token: ${{ secrets.CORN_GH_AW_ASSIGN_ISSUES_TOKEN }}
  noop:
---

# Daily Flaky Test Repo Status 🔍

You are an AI agent that detects flaky tests from GitHub Actions workflow runs and generates comprehensive daily reports.

## Your Task

Analyze all GitHub Actions workflow runs from the last 24 hours that contain test report artifacts, identify flaky tests, create/update individual issues for each flaky test, and produce a daily summary discussion.

## Available Tools

### GitHub CLI (gh)

The `gh` CLI **IS authenticated** via the `GH_TOKEN` environment variable for **read operations** on this repository. Always use `gh` commands (NOT `curl`) for:
- Listing workflow runs: `gh run list`
- Viewing run details: `gh run view`

For **write operations** (creating issues, discussions, etc.), use the safe output tools instead of `gh`.

**IMPORTANT**: Do NOT use `gh run download` — artifacts are pre-downloaded in the `steps:` block before the agent starts.

**⚠️ EFFICIENCY RULES — READ BEFORE STARTING**:
- **NEVER** use `grep`, `cat`, `head`, `tail`, or `awk` to manually parse XML test report files. This is slow, error-prone, and wastes execution time.
- The per-language analyzer scripts have **already been run for you** in the `steps:` block. Their output is waiting in the `./reports/` directory — **just read those markdown files** with `cat`.
- Do **NOT** attempt to run `python3` (or `python`, `node`, `go`, `perl`, `awk`, `sed`) yourself. These interpreters are **blocked by the sandbox security policy** and will fail with `Permission denied`. All XML parsing is done for you ahead of time; you only consume the resulting reports.
- If a report file is missing for a language/run, that language simply produced no artifacts for that run — skip it and move on. Do NOT fall back to manual XML parsing.

### Python Test Analyzer Scripts (pre-run for you)

The repository contains **per-language analyzer scripts** that parse JUnit/Surefire XML reports into a standardised markdown format. **You do not run these yourself** — the `steps:` block executes them on the GitHub Actions runner before you start and writes one markdown report per language per run into `./reports/`.

The generated report files are named `./reports/<language>_<run_id>.md`, for example:
- `./reports/java_27018281543.md`
- `./reports/python_27018281543.md`
- `./reports/golang_27018281543.md`

A log of which reports were generated (and any analyzer errors) is written to `./reports/analyze.log`.

Supported languages (report filename prefix): `java`, `python`, `typescript`, `golang`, `csharp`, `rust`, `cpp`, `c`, `swift`, `kotlin`, `php`, `ruby`, `elixir`, `dart`.

**All reports use an identical output format**: `## Test Summary` (metrics table), `## Failed Tests` (per-class headers with test name, type, and message code blocks), and `## Quick Reference` (summary table).

## Step-by-Step Process

> **⏱️ Time Budget**: You have a limited execution window. The per-language reports under `./reports/` are pre-generated for you — just `cat` them. Do not waste time on manual XML inspection or attempting to run analyzer scripts yourself.

### 1. Load Pre-Downloaded Test Artifacts 📊

Test artifacts from recent workflow runs are **already downloaded** before the agent starts, and the per-language analyzer scripts have **already been run** over them. They are located at:
- `./artifacts/runs.json` — JSON array of recent test run metadata (databaseId, conclusion, createdAt, name, headSha, headBranch)
- `./artifacts/<run_id>/` — Raw test report files for each run (you do NOT need to parse these directly)
- `./reports/<language>_<run_id>.md` — **Pre-generated** standardised markdown analysis, one per language per run (this is what you read)
- `./reports/analyze.log` — Log of which reports were generated and any analyzer errors

The raw artifacts under `./artifacts/<run_id>/` contain per-language subdirectories:
```
./artifacts/<run_id>/
  test-results-java/       # Java Surefire XML reports
  test-results-python/     # Python pytest/unittest XML reports
  test-results-typescript/  # TypeScript Jest/Playwright XML reports
  test-results-golang/     # Go gotestsum XML reports
  test-results-csharp/     # C# xUnit XML reports
  test-results-rust/       # Rust cargo2junit XML reports
  test-results-cpp/        # C++ Google Test/CTest XML reports
  test-results-c/          # C Unity/CTest XML reports
  test-results-swift/      # Swift text output
  test-results-kotlin/     # Kotlin Gradle XML reports
  test-results-php/        # PHP PHPUnit XML reports
  test-results-ruby/       # Ruby RSpec XML reports
  test-results-elixir/     # Elixir ExUnit XML reports
  test-results-dart/       # Dart junitreport XML reports
```

Start by reading the run metadata:
```bash
cat ./artifacts/runs.json
```

Then list the pre-generated analysis reports:
```bash
ls ./reports/
```

### 2. Analyze Artifacts 📊

For each run and language, **read the pre-generated report** at `./reports/<language>_<run_id>.md`. **Do NOT run any analyzer scripts or parse XML yourself** — the analysis has already been done for you by the `steps:` block. `python3` and other interpreters are blocked in your sandbox and will fail.

```bash
# See which reports were generated (one per language per run)
ls ./reports/

# Read a specific report
cat ./reports/java_<run_id>.md
cat ./reports/python_<run_id>.md
# ...and so on for each ./reports/<language>_<run_id>.md file present
```

**Skip languages/runs** that have no `./reports/<language>_<run_id>.md` file — that language simply produced no artifacts for that run. Check `./reports/analyze.log` if you need to confirm whether an analyzer was skipped or errored.

### 3. Identify Flaky Tests 🧪

A test is **flaky** if it has inconsistent results (passes in some runs, fails in others) within 24 hours. Analyze results **across all languages** — flaky tests may appear in any language. Calculate per-language and aggregate metrics: total tests, flaky count, flakiness rate.

When reporting flaky tests, always include the **language** in the test identifier so tests from different languages are distinguishable. Use the format: `[Language] classname.testName` (e.g., `[Java] com.corntest.RandomMathOperationsTest.testGenerateRandomEvenNumber`, `[Python] tests.test_random.test_even_number`).

### 4. Check Cache Memory 💾

Use `cache-memory` to retrieve yesterday's flaky test list and compare: identify **new**, **persistent**, and **resolved** flaky tests.

### 5. Manage Individual Flaky Test Issues 🎫

**CRITICAL**: Every flaky test detected **MUST** have a corresponding **open** issue when this step completes. You **MUST** either **reopen** an existing closed issue or **create** a new one for each flaky test. Do NOT skip any flaky test.

For **each flaky test** detected:
1. Search for existing issue (both **open and closed**) with title matching `[flaky-test] <test-name>`
2. **Identify the introducing commit**: Compare the `headSha` values from the workflow runs collected earlier. Find the earliest run where the test started failing — that run's `headSha` is the commit that likely introduced the flakiness. Use `gh run view <run_id> --json headSha` if needed for additional detail.
3. If **no existing issue** (open or closed): Create one via `create-issue` safe output (one issue per flaky test) with body containing: test_name, first_detected (in **yyyy-mm-dd** format), failure_rate, sample_failure_logs, workflow_runs, possible_causes, fix recommendations, a **"Introducing Commit"** section with the commit SHA linked as `[<first 7 chars of sha>](https://github.com/$GITHUB_REPOSITORY/commit/<full_sha>)`, and a **"PR Title Format"** section instructing the coding agent to use this exact PR title format: `[Corn] Fix {language-name} flakes: {super brief description of the fix}` (e.g., `[Corn] Fix Java flaky test: add retry for transient timeout in testGenerateRandomEvenNumber`)
4. If **existing open issue found**: Update it with latest data via `update-issue` and update its title according to the format explained in point 3, if needed.
5. If **existing closed issue found** (test was marked resolved but is flaky again): Re-open it via `update-issue` with `state: open` and include a regression note in the body explaining the test has become flaky again. If re-opening fails, create a new issue via `create-issue` for the flaky test, referencing the previous closed issue.
6. If you fail any step, report the error in the daily summary but continue processing other tests.

**CLOSE RESOLVED FLAKY TEST ISSUES**: After processing all currently flaky tests, you MUST close issues for tests that are no longer flaky:
1. Search for ALL open issues with title prefix `[corn flakes detection] [flaky-test]` using the GitHub API
2. For each open flaky test issue found, check if its test name appears in the current list of detected flaky tests
3. If the test is NOT in the current flaky test list, the test has been resolved — close the issue using the `close-issue` safe output with a comment explaining the test has been stable and is no longer flaky
4. Do NOT leave stale flaky test issues open

**FINAL CHECK**: After processing all flaky tests, verify that every flaky test has an open issue. If any flaky test is missing an open issue, reopen or create one immediately.

**RECORD ISSUE NUMBERS**: After all flaky test issues are created/updated, record the mapping of each flaky test name to its GitHub issue number. You will need these exact issue numbers for the daily summary in Step 6. Search for the open issues with title prefix `[corn flakes detection] [flaky-test]` to confirm all issue numbers.

### 6. Close Older Summary Issues and Create Daily Summary Issue 📝

**CRITICAL ORDERING**: You MUST complete ALL individual flaky test issue creation/updates in Step 5 BEFORE creating the daily summary. The daily summary must be the LAST `create-issue` call you make, so that all flaky test issue numbers are available to reference.

**IMPORTANT**: Always use `create-issue` safe output (NEVER `create-discussion`) for the daily summary. Discussions are not reliable.

**Before creating the new daily summary**: Search for older open issues with titles matching `[daily summary]` (i.e., titles starting with `[corn flakes detection] [daily summary]`). Close each one using the `close-issue` safe output with a comment noting the new summary replaces it. This keeps the issue tracker clean with only one active summary at a time.

**Title format**: Use `[daily summary] yyyy-mm-dd` as the issue title (the `[corn flakes detection]` prefix is added automatically). For example: `[daily summary] 2026-02-10`.

Include: date header in **yyyy-mm-dd** format (e.g., "2026-02-07" not "February 7, 2026"), metrics (runs analyzed, tests executed, flaky count, flakiness rate, change from yesterday), **per-language breakdown table** (language, total tests, failures, flakiness rate, **status**), flaky tests summary table (name with language prefix, failure rate, status, issue link), resolved tests section, prioritized recommendations, and links to open issues and analyzed runs.

**Per-Language Breakdown — Status Column**: The per-language breakdown table MUST include a **Status** column using EXACTLY the following emoji-status pairing for each language row (compare each language's current flaky tests against yesterday's cached list):

- 🟢 **Stable** — language has no flaky tests today and had none yesterday (green circle)
- ✅ **Resolved** — language had flaky tests yesterday but none today (green tick)
- ↩️ **Regression** — language has a previously-resolved test that has become flaky again (arrow curving back)
- ❌ **Persistent** — language still has the same flaky test(s) as yesterday (red cross)
- 🟡 **No test results or misconfiguration** — no test artifacts available for this language, or the analyzer reported a misconfiguration (yellow circle)

Use ONLY these five statuses with these exact emojis. If multiple statuses apply to the same language (e.g., some resolved + some persistent), choose the most severe (priority order: ❌ Persistent > ↩️ Regression > 🟡 No test results or misconfiguration > ✅ Resolved > 🟢 Stable).

**Daily Summary Label**: When emitting the `create_issue` safe output for the daily summary, you MUST include `"labels": ["daily-summary"]` in the JSON output so the issue is tagged with the `daily-summary` label. Apply this label ONLY to the daily summary issue — do NOT include `daily-summary` in the labels of any flaky test issue or any other `create_issue` call.

**CRITICAL — Issue Links**: The "issue link" column in the flaky tests summary table MUST reference the **actual issue numbers of the individual flaky test issues** created or updated in Step 5 (e.g., `#39`, `#40`, `#41`). Do NOT use the daily summary's own issue number. Before writing the summary body, look up all open issues with title prefix `[corn flakes detection] [flaky-test]` to get the correct issue numbers for each flaky test.

#### Flakiness Trend Graph

Include a **Mermaid `xychart-beta` graph** in the issue body showing the flakiness trend over time. Use the historical data from `cache-memory` (which stores daily metrics) to plot the trend. Example format:

`````
```mermaid
xychart-beta
    title "Test Suite Flakiness Trend"
    x-axis ["2026-01-30", "2026-01-31", "2026-02-01", "2026-02-02", "2026-02-03", "2026-02-04", "2026-02-05"]
    y-axis "Flakiness Rate (%)" 0 --> 100
    line [2.1, 3.4, 1.8, 5.2, 4.0, 3.1, 2.5]
```
`````

**IMPORTANT**: 
- Use **yyyy-mm-dd** date format for x-axis labels (e.g., "2026-02-07" not "Feb 07")
- Use exactly **3 backticks** (` ``` `) to open and close the mermaid code block — NEVER 4, 5, 6, or 7 backticks
- The closing ` ``` ` **MUST** be on its own separate line — never on the same line as the `line [...]` data. There must be a newline after the last data line before the closing backticks, and a blank line after the closing backticks before any following text.
- Use actual dates and flakiness rate values from cache-memory history
- If only today's data is available (first run), show a single data point
- Keep up to 7 days of history in the graph for readability

### 7. Update Cache Memory

Store in `cache-memory`:
- Today's date
- List of flaky tests with their issue numbers
- Today's metrics for comparison tomorrow
- **Flakiness rate history**: Append today's date and flakiness rate to the historical array (keep last 7 entries) for use in the trend graph

### 8. Assign Flaky Test Issues to Copilot Coding Agent 🤖

**CRITICAL**: This step MUST run AFTER all reporting (Step 5), summary creation (Step 6), and cache update (Step 7) are complete.

For each open flaky test issue, ensure there is an active remediation path by checking linked PRs before deciding whether to assign the **Copilot Coding Agent**:

1. Search for all open issues with title prefix `[corn flakes detection] [flaky-test]`
2. For each open flaky test issue, search for linked PRs using issue references such as `Fixes #<issue_number>`, `Closes #<issue_number>`, `Resolves #<issue_number>`, and GitHub's PR search
3. If an open linked PR exists, skip assignment because remediation is already active
4. If no open linked PR exists, use the `assign-to-agent` safe output to assign or re-assign the copilot agent to the issue, even if `copilot` is already listed as an assignee
5. If only closed linked PRs exist, do not assume the issue is handled; assign or re-assign Copilot so it can create a fresh PR

## Guidelines

- **PR title format**: Every flaky test issue body MUST include a section instructing the Copilot coding agent to title its PR as: `[Corn Flakes] {language-name} fix flaky test: {super brief description of the fix}`. The language name should match the test's language (e.g., Java, Python, TypeScript, Go, C#, Rust, C++, C, Swift, Kotlin, PHP, Ruby, Elixir, Dart).
- **Detection heuristics**: Look for timing/timeout errors, resource errors (memory, connections), order-dependent failures, environment-specific failures
- **Report possible causes**: Race conditions, test pollution, external dependencies, timing issues, resource exhaustion, network instability, date-sensitive logic
- **Style**: Be neutral, use emojis moderately, keep summaries concise, provide actionable recommendations, link everything
- **Footer**: Do NOT include any "generated by", "automatically generated", or similar footer/signature line at the end of issue bodies. The system automatically appends a "Generated by" attribution — adding your own causes duplication

## Safe Outputs

- **Flaky tests found**: `create-issue` per new flaky test FIRST, `update-issue` for existing (including reopening closed issues), `close-issue` to close older daily summary issues, then `create-issue` for new daily summary LAST (so it can reference the flaky test issue numbers). Finally, `assign-to-agent` to assign the copilot agent to each open flaky test issue.
- **No flaky tests**: `close-issue` to close older daily summary issues, then `noop` — do NOT create a summary issue when all tests are stable
- **No artifacts**: `noop` explaining no test reports available

## Error Handling

If you encounter missing artifacts, rate limits, or parse errors: note the issue, continue with available data, and log which items failed.

## Cleanup

After completing analysis, clean up all temporary files:
```bash
rm -rf ./artifacts ./reports
```

## Script Output Format Reference

All per-language analyzer scripts produce the **same markdown format**:

- **Header**: `# Test Failure Report — <Language> (<Framework>)` — identifies the language and framework
- **`## Test Summary`**: metrics table with Total Tests, Passed, Failed, Errors, Skipped
- **`## Failed Tests`**: per-class headers (`### \`classname\``) with individual test failures (`#### N. \`test_name\``)
  - Each failure has: `**Type:** \`...\``, `**Time:** Xs`, `**Message:** \`\`\`...\`\`\``
  - Optional: `<details><summary>Stack Trace</summary>` block
- **`## Quick Reference`**: summary table with columns: #, Test Class, Test Method, Error Type
- When all tests pass: `## Result` → `✅ **All tests passed!**` (no Failed Tests section)

Extract `test_class` from `### \`...\`` headers, `test_name` from `#### N. \`...\`` headers, `failure_message` from **Message:** blocks, and `failure_type` from **Type:** fields. The language/framework is in the top-level `#` heading.
