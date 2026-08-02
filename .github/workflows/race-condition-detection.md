---
description: |
  Daily race-condition flakiness detection workflow. Analyzes recent test artifacts across
  multiple GitHub Actions runs to surface tests that fail intermittently due to concurrency
  bugs (data races, deadlocks, concurrent modification, timing/ordering issues) and opens or
  updates a dedicated issue per affected test.

on:
  # Run on weekdays only (avoid weekend noise). Hour chosen at random.
  schedule:
    - cron: "0 7 * * 1-5"
  # Allow manual runs for ad-hoc investigation.
  workflow_dispatch:

timeout-minutes: 45
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

steps:
  - name: Validate auth token
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    run: |
      gh run list --repo "${GITHUB_REPOSITORY}" --workflow=test.yml --limit 1 >/dev/null \
        || { echo "::error::Unable to list test workflow runs with GH_TOKEN. Check GITHUB_TOKEN validity and actions:read permission."; exit 1; }

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
      # Save run metadata for the agent. headSha lets the agent group runs by commit
      # so it can spot the SAME test passing on one run and failing on another at the
      # same SHA — the hallmark of a race condition.
      gh run list --workflow=test.yml --limit 30 --json databaseId,conclusion,createdAt,name,headSha,headBranch > ./artifacts/runs.json
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
    title-prefix: "[race condition] "
    labels: [race-condition, flaky-test, automated]
    allowed-labels: [race-condition, flaky-test, automated]
    close-older-issues: false
    max: 30
  update-issue:
    status:
    target: "*"
    max: 30
  noop:
---

# Daily Race Condition Flakiness Detection 🧵🏁

You are an AI agent that detects **race-condition–induced flaky tests** from GitHub Actions
workflow runs and files a focused issue per affected test.

## What is a race-condition flaky test?

A race-condition flaky test is one whose result is **non-deterministic because of concurrency**,
not because of a stable logic bug. Treat a test as a race-condition suspect when **either** of
these holds:

1. **Same-commit non-determinism** — the *same* test (same class + name) **passes in one run and
   fails in another run that shares the same `headSha`**. If the code is identical and the result
   flips, timing/scheduling is the most likely cause.
2. **Concurrency failure signature** — the failure message/stack trace contains a known
   race/concurrency indicator (see the signature list below), regardless of how many runs you have.

Plain deterministic failures (assertion mismatches, compile errors, missing files, the test fails
the same way on every run at a SHA) are **out of scope** — ignore them. This workflow is *only*
about concurrency-related flakiness.

## Available Tools

### GitHub CLI (gh)

The `gh` CLI **IS authenticated** via `GH_TOKEN` for **read operations** on this repository. Use
`gh` (NOT `curl`) for `gh run list` and `gh run view`. For **write operations** (creating/updating
issues), use the safe-output tools — never `gh` and never the GitHub MCP write tools directly.

**IMPORTANT**: Do NOT use `gh run download` — artifacts are pre-downloaded in the `steps:` block.

**⚠️ EFFICIENCY RULES — READ BEFORE STARTING**:
- **NEVER** use `grep`, `cat`, `head`, `tail`, or `awk` to manually parse XML report files. The
  per-language analyzers have **already been run for you** in the `steps:` block; just `cat` the
  resulting markdown in `./reports/`.
- Do **NOT** run `python3` (or `python`, `node`, `go`, `perl`, `awk`, `sed`) — these interpreters
  are **blocked by the sandbox** and fail with `Permission denied`. All XML parsing is done ahead
  of time.
- If a report file is missing for a language/run, that language produced no artifacts for that run
  — skip it. Do NOT fall back to manual XML parsing.

## Pre-Downloaded Inputs 📥

Everything you need is already on disk before you start:

- `./artifacts/runs.json` — JSON array of recent test run metadata: `databaseId`, `conclusion`,
  `createdAt`, `name`, `headSha`, `headBranch`. **`headSha` is critical** — it lets you group runs
  by commit to detect same-commit non-determinism.
- `./reports/<language>_<run_id>.md` — **pre-generated** standardised markdown analysis, one per
  language per run. This is what you read.
- `./reports/analyze.log` — log of which reports were generated and any analyzer errors.

Supported language prefixes: `java`, `python`, `typescript`, `golang`, `csharp`, `rust`, `cpp`,
`c`, `swift`, `kotlin`, `php`, `ruby`, `elixir`, `dart`.

All reports share the same format: `## Test Summary` (metrics), `## Failed Tests` (per-class
headers `### \`classname\`` with `#### N. \`test_name\``, plus **Type:**, **Time:**, and
**Message:** blocks), and `## Quick Reference`.

## Race / Concurrency Signatures 🔎

When scanning a failure's **Type** and **Message** blocks, treat any of the following (case-
insensitive) as a concurrency signature. The list is grouped by ecosystem but match across all
languages:

- **Generic**: `race condition`, `data race`, `deadlock`, `livelock`, `thread`, `concurrent`,
  `concurrency`, `mutex`, `semaphore`, `atomic`, `lock`, `synchroniz`, `non-deterministic`,
  `timing`, `timeout` *(only when paired with concurrency context)`, `interrupted`, `scheduler`.
- **Go**: `WARNING: DATA RACE`, `race detected`, `fatal error: concurrent map read and map write`,
  `concurrent map writes`, `concurrent map iteration and map write`.
- **Java / Kotlin**: `ConcurrentModificationException`, `java.util.concurrent`, `Deadlock`,
  `InterruptedException`, `thread interrupted`, `Lock`, `synchronized`.
- **C# / .NET**: `ThreadAbortException`, `SemaphoreFullException`, `deadlock`, `Interlocked`,
  `lock contention`, `Task was canceled`.
- **C / C++**: `ThreadSanitizer`, `data race`, `WARNING: ThreadSanitizer`, `race on`, `pthread`,
  `std::mutex`, `lock-order-inversion`.
- **Rust**: `data race`, `PoisonError`, `deadlock`, `Mutex`, `RwLock`, `would block`.
- **Python**: `RuntimeError: dictionary changed size during iteration`, `deadlock`, `asyncio`,
  `Lock`, `Event`, `threading`, `concurrent.futures`.
- **Ruby**: `ThreadError`, `deadlock`, `Mutex`, `fatal: No live threads left`.
- **PHP / Elixir / Dart / Swift / TypeScript**: `deadlock`, `mutex`, `race`, `async`, `await`,
  timing-sensitive timeouts, `concurrent`.

A signature match OR same-commit non-determinism is sufficient to classify a test as a
race-condition suspect.

## Step-by-Step Process

> **⏱️ Time Budget**: The per-language reports are pre-generated — just `cat` them. Do not attempt
> to run analyzers or parse XML yourself.

### 1. Load metadata and reports 📊

```bash
cat ./artifacts/runs.json
ls ./reports/
cat ./reports/analyze.log
```

Build an index of every report file: `./reports/<language>_<run_id>.md`. Map each `run_id` back to
its `headSha` using `runs.json`.

### 2. Read each report and collect failures 🧾

For each `./reports/<language>_<run_id>.md` with a `## Failed Tests` section, extract for every
failed test: language, `test_class` (from `### \`...\``), `test_name` (from `#### N. \`...\``),
`failure_type` (**Type:**), `failure_message` (**Message:**), and the run's `headSha`.

If a report shows `✅ All tests passed!`, record each of its passing tests too — you need the
pass/fail history per `headSha` to detect same-commit non-determinism.

### 3. Classify race-condition suspects 🧵

A test is a **race-condition suspect** if EITHER:

- **Same-commit non-determinism**: across the runs that share one `headSha`, the test both passed
  and failed; OR
- **Signature match**: its `failure_type` or `failure_message` matches any concurrency signature
  from the list above.

Exclude tests whose failures are deterministic at every SHA and carry no concurrency signature.

For each suspect, capture: language, fully-qualified test name (`<class>.<name>`), the evidence
(which it is — flip-flop SHA and/or which signature matched), representative failure message, and
the list of affected run IDs / SHAs.

### 4. File or update one issue per suspect 🗂️

Process each race-condition suspect:

1. **Search existing issues** (read-only, via `gh api` / the GitHub read tools) with title prefix
   `[race condition]` to see whether this test already has an issue.
2. **No existing issue** → emit a `create-issue` safe output. Title (the `[race condition] `
   prefix is added automatically): `<Language> race-condition flaky test: <Class>.<name>`.
   Include labels `["race-condition", "flaky-test", "automated"]`.
3. **Existing open issue** → emit an `update-issue` safe output refreshing the body with the latest
   evidence (newest affected runs/SHAs).
4. If any step fails, note it and continue with the remaining suspects.

**Issue body must include**:
- **Classification**: which trigger fired (same-commit non-determinism, signature match, or both).
- **Evidence**: the conflicting run IDs + `headSha` (for flip-flops) and/or the exact concurrency
  signature(s) matched, with the representative failure message in a fenced code block.
- **Suspected cause**: a short concurrency-focused hypothesis (shared mutable state, missing
  synchronisation, ordering assumption, await/sleep timing, resource contention, etc.).
- **Remediation instruction for the Copilot coding agent**: tell it to title its PR
  `[Corn Flakes] {language-name} fix race condition: {super brief description of the fix}` where
  language-name matches the test's language (Java, Python, TypeScript, Go, C#, Rust, C++, C, Swift,
  Kotlin, PHP, Ruby, Elixir, Dart).

Do NOT add any "generated by" / "automatically generated" footer — the system appends attribution
automatically.

### 5. Update cache memory 🧠

Store in `cache-memory`: today's date and the list of race-condition suspect tests (with their
issue numbers) so future runs can track recurrence and trends.

## Safe Outputs

- **Suspects found**: `create-issue` per newly-detected suspect, `update-issue` for suspects that
  already have an open issue.
- **No suspects / no artifacts**: emit `noop` with a one-line explanation (e.g. "No
  race-condition flakiness detected across the last 30 runs" or "No test artifacts available").

## Error Handling

On missing artifacts, rate limits, or parse errors: note the problem, continue with available
data, and log which items failed. Never abort the whole run because one report is unreadable.

## Cleanup

After completing the analysis, remove temporary files:

```bash
rm -rf ./artifacts ./reports
```
