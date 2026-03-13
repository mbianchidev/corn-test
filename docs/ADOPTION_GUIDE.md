# 🌽 Corn Flakes Detection — Adoption Guide

> **Automated flaky test detection using GitHub Agentic Workflows (gh-aw)**

This guide explains how to adopt the **corn-flakes-detection** agentic workflow in your own repository. The workflow runs on a daily schedule, analyzes your test artifacts, detects flaky tests, creates and manages GitHub Issues for each flaky test, and assigns Copilot Coding Agent to fix them.

> [!NOTE]
> **Multi-language support.** This workflow supports any project that produces **JUnit XML** test reports. See the [Supported Languages](#supported-languages--test-frameworks) section for framework-specific setup guidance.

---

## Table of Contents

- [Supported Languages & Test Frameworks](#supported-languages--test-frameworks)
- [Prerequisites](#prerequisites)
- [Step 1 — Install the gh-aw CLI](#step-1--install-the-gh-aw-cli)
- [Step 2 — Create the Copilot Setup Steps Workflow](#step-2--create-the-copilot-setup-steps-workflow)
- [Step 3 — Add the Test Workflow](#step-3--add-the-test-workflow)
- [Step 4 — Add the Python Analyzer Script](#step-4--add-the-python-analyzer-script)
- [Step 5 — Create the Agentic Workflow Definition](#step-5--create-the-agentic-workflow-definition)
- [Step 6 — Compile the Agentic Workflow](#step-6--compile-the-agentic-workflow)
- [Step 7 — Configure Repository Tokens & Permissions](#step-7--configure-repository-tokens--permissions)
- [Step 8 — Commit and Enable](#step-8--commit-and-enable)
- [File Structure Reference](#file-structure-reference)
- [Token & Permissions Reference](#token--permissions-reference)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

---

## Supported Languages & Test Frameworks

The workflow analyzes **JUnit XML** test reports. Any language/framework producing this format is supported. Below are the tested configurations with example test workflow snippets.

| Language | Framework(s) | Build Tool | Report Output |
|----------|-------------|------------|---------------|
| **Java** | JUnit 5 | Maven (Surefire) | `target/surefire-reports/TEST-*.xml` |
| **Kotlin** | kotlin.test | Gradle | `build/test-results/**/*.xml` |
| **Python** | pytest, unittest | pip | `--junitxml=reports/results.xml` |
| **TypeScript** | Jest, Playwright | npm | `jest-junit` / `--reporter=junit` |
| **Go** | built-in testing | gotestsum | `--junitfile reports/results.xml` |
| **C#** | xUnit.net | dotnet | `--logger "junit;LogFilePath=..."` |
| **Rust** | cargo test | cargo2junit | pipe JSON to `cargo2junit` |
| **C++** | Google Test (gTest) | CMake / CTest | `ctest --output-junit` |
| **C** | Unity | CMake / CTest | `ctest --output-junit` |
| **Swift** | XCTest | Swift Package Manager | Text output (parsed by analyzer) |
| **PHP** | PHPUnit | Composer | `--log-junit reports/results.xml` |
| **Ruby** | RSpec | Bundler | `rspec_junit_formatter` |
| **Elixir** | ExUnit | Mix | `junit_formatter` |
| **Dart** | dart test | pub | `junitreport:tojunit` |

---

## Prerequisites

Before you begin, ensure you have:

| Requirement | Details |
|---|---|
| **GitHub repository** | Public or private, with GitHub Actions enabled |
| **Test project** | Using one of the [supported frameworks](#supported-languages--test-frameworks) that produces JUnit XML reports |
| **GitHub Copilot** | A [GitHub Copilot](https://github.com/features/copilot) subscription (Business or Enterprise) for the Copilot Coding Agent integration |
| **Fine-grained PAT** | A personal access token with `contents`, `pull-requests`, and `issues` read/write permissions (see [Step 7](#step-7--configure-repository-tokens--permissions)) |
| **gh CLI** | The [GitHub CLI](https://cli.github.com/) installed locally |
| **gh-aw extension** | The [GitHub Agentic Workflows](https://gh.io/gh-aw) CLI extension installed (see Step 1) |

---

## Step 1 — Install the gh-aw CLI

Install the `gh-aw` CLI extension, which compiles agentic workflow definitions (`.md` files) into GitHub Actions workflows (`.lock.yml` files).

```bash
# Install the gh-aw extension
gh ext install github/gh-aw

# Verify installation
gh aw version
```

> 📖 **Docs**: [gh-aw Installation](https://gh.io/gh-aw)

---

## Step 2 — Create the Copilot Setup Steps Workflow

This workflow configures the environment for GitHub Copilot Agent with the gh-aw MCP server. It must be present for the agentic workflow to function.

Create `.github/workflows/copilot-setup-steps.yml`:

```yaml
name: "Copilot Setup Steps"

on:
  workflow_dispatch:
  push:
    paths:
      - .github/workflows/copilot-setup-steps.yml

jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Install gh-aw extension
        run: |
          curl -fsSL https://raw.githubusercontent.com/githubnext/gh-aw/refs/heads/main/install-gh-aw.sh | bash
      - name: Verify gh-aw installation
        run: gh aw version
```

> [!NOTE]
> The job **must** be named `copilot-setup-steps` — this name is required by GitHub Copilot Agent.

---

## Step 3 — Add the Test Workflow

You need a GitHub Actions workflow that runs your tests and uploads JUnit XML reports as artifacts. Create `.github/workflows/test.yml` with a job for each language in your project.

> [!IMPORTANT]
> - Each language job should upload artifacts named `test-results-<language>` (e.g., `test-results-java`, `test-results-python`)
> - Add a `collect-results` job that merges all individual artifacts into a single `test-results` artifact
> - Use `continue-on-error: true` on test steps so artifacts are uploaded even when tests fail

Below are example job configurations for each supported language. Use only the ones relevant to your project.

<details>
<summary><strong>Java (JUnit 5 / Maven)</strong></summary>

```yaml
test-java:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: java
  steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-java@v4
    with:
      java-version: '11'
      distribution: 'temurin'
      cache: 'maven'
      cache-dependency-path: java/pom.xml
  - run: mvn clean compile
  - run: mvn test
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-java
      path: java/target/surefire-reports/**/*
```
</details>

<details>
<summary><strong>Python (pytest + unittest)</strong></summary>

```yaml
test-python:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: python
  steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: '3.11'
  - run: pip install -r requirements.txt
  - run: python -m pytest --junitxml=reports/pytest-results.xml -v
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-python
      path: python/reports/*.xml
```
</details>

<details>
<summary><strong>TypeScript (Jest + Playwright)</strong></summary>

```yaml
test-typescript:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: typescript
  steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-node@v4
    with:
      node-version: '20'
      cache: 'npm'
      cache-dependency-path: typescript/package-lock.json
  - run: npm ci
  - run: npx jest --ci --reporters=default --reporters=jest-junit
    continue-on-error: true
    env:
      JEST_JUNIT_OUTPUT_DIR: reports
  - run: npx playwright install --with-deps chromium
  - run: npx playwright test --reporter=junit
    continue-on-error: true
    env:
      PLAYWRIGHT_JUNIT_OUTPUT_NAME: reports/playwright-results.xml
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-typescript
      path: typescript/reports/*.xml
```
</details>

<details>
<summary><strong>Go (built-in testing)</strong></summary>

```yaml
test-golang:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: golang
  steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-go@v5
    with:
      go-version: '1.22'
  - run: go install gotest.tools/gotestsum@latest
  - run: gotestsum --junitfile reports/go-test-results.xml -- -v ./...
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-golang
      path: golang/reports/*.xml
```
</details>

<details>
<summary><strong>C# (xUnit.net)</strong></summary>

```yaml
test-csharp:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: csharp
  steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-dotnet@v4
    with:
      dotnet-version: '8.0'
  - run: dotnet restore
  - run: dotnet test --logger "junit;LogFilePath=reports/xunit-results.xml" --no-restore
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-csharp
      path: csharp/**/reports/*.xml
```
</details>

<details>
<summary><strong>Rust (cargo test)</strong></summary>

```yaml
test-rust:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: rust
  steps:
  - uses: actions/checkout@v4
  - uses: dtolnay/rust-toolchain@stable
  - run: cargo install cargo2junit
  - run: cargo test -- -Z unstable-options --format json 2>&1 | cargo2junit > reports/rust-test-results.xml
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-rust
      path: rust/reports/*.xml
```
</details>

<details>
<summary><strong>C++ (Google Test)</strong></summary>

```yaml
test-cpp:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: cpp
  steps:
  - uses: actions/checkout@v4
  - run: sudo apt-get update && sudo apt-get install -y cmake libgtest-dev
  - run: mkdir -p build && cd build && cmake .. && make
  - run: mkdir -p reports && cd build && ctest --output-junit ../reports/gtest-results.xml --output-on-failure
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-cpp
      path: cpp/reports/*.xml
```
</details>

<details>
<summary><strong>C (Unity)</strong></summary>

```yaml
test-c:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: c
  steps:
  - uses: actions/checkout@v4
  - run: sudo apt-get update && sudo apt-get install -y cmake ruby
  - run: mkdir -p build && cd build && cmake .. && make
  - run: mkdir -p reports && cd build && ctest --output-junit ../reports/unity-results.xml --output-on-failure
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-c
      path: c/reports/*.xml
```
</details>

<details>
<summary><strong>Swift (XCTest)</strong></summary>

```yaml
test-swift:
  runs-on: macos-latest
  defaults:
    run:
      working-directory: swift
  steps:
  - uses: actions/checkout@v4
  - run: swift build
  - run: swift test 2>&1 | tee reports/swift-test-output.txt
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-swift
      path: swift/reports/*
```
</details>

<details>
<summary><strong>Kotlin (kotlin.test / Gradle)</strong></summary>

```yaml
test-kotlin:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: kotlin
  steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-java@v4
    with:
      java-version: '17'
      distribution: 'temurin'
  - uses: gradle/actions/setup-gradle@v4
  - run: ./gradlew test
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-kotlin
      path: kotlin/build/test-results/**/*.xml
```
</details>

<details>
<summary><strong>PHP (PHPUnit)</strong></summary>

```yaml
test-php:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: php
  steps:
  - uses: actions/checkout@v4
  - uses: shivammathur/setup-php@v2
    with:
      php-version: '8.3'
      tools: composer
  - run: composer install --no-interaction
  - run: vendor/bin/phpunit --log-junit reports/phpunit-results.xml
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-php
      path: php/reports/*.xml
```
</details>

<details>
<summary><strong>Ruby (RSpec)</strong></summary>

```yaml
test-ruby:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: ruby
  steps:
  - uses: actions/checkout@v4
  - uses: ruby/setup-ruby@v1
    with:
      ruby-version: '3.3'
      bundler-cache: true
      working-directory: ruby
  - run: bundle exec rspec --format RspecJunitFormatter --out reports/rspec-results.xml --format documentation
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-ruby
      path: ruby/reports/*.xml
```
</details>

<details>
<summary><strong>Elixir (ExUnit)</strong></summary>

```yaml
test-elixir:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: elixir
  steps:
  - uses: actions/checkout@v4
  - uses: erlef/setup-beam@v1
    with:
      elixir-version: '1.16'
      otp-version: '26'
  - run: mix deps.get
  - run: mix test --formatter JUnitFormatter
    continue-on-error: true
    env:
      JUNIT_OUTPUT_DIR: reports
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-elixir
      path: elixir/reports/*.xml
```
</details>

<details>
<summary><strong>Dart (dart test)</strong></summary>

```yaml
test-dart:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: dart
  steps:
  - uses: actions/checkout@v4
  - uses: dart-lang/setup-dart@v1
    with:
      sdk: '3.3.0'
  - run: dart pub get
  - run: |
      mkdir -p reports
      dart test --reporter json | dart run junitreport:tojunit > reports/dart-test-results.xml
    continue-on-error: true
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: test-results-dart
      path: dart/reports/*.xml
```
</details>

<details>
<summary><strong>Collect Results (required — merges all language artifacts)</strong></summary>

```yaml
collect-results:
  needs: [test-java, test-python, ...]  # List all your language jobs
  if: always()
  runs-on: ubuntu-latest
  steps:
  - uses: actions/download-artifact@v4
    with:
      pattern: test-results-*
      path: all-test-results
      merge-multiple: false
  - uses: actions/upload-artifact@v4
    with:
      name: test-results
      path: all-test-results/
      retention-days: 30
```
</details>

> [!IMPORTANT]
> The final merged artifact **must** be named `test-results` — the agentic workflow downloads artifacts by this name.

---

## Step 4 — Add the Python Analyzer Script

The agentic workflow uses Python scripts to parse JUnit/Surefire XML test reports into structured markdown. Copy the scripts from this repository:

```
.github/workflows/scripts/analyze_gh_test_failures.py    # Original Java-focused analyzer
.github/workflows/scripts/analyze_test_results.py        # Multi-language analyzer
```

Place them at the same paths in your repository:

```bash
mkdir -p .github/workflows/scripts
# Copy both analyzer scripts into .github/workflows/scripts/
```

These scripts support:
- Parsing JUnit XML reports from all supported languages/frameworks
- Generating markdown summaries of test failures
- Local artifact analysis mode (used by the agentic workflow)
- Multi-language auto-detection when analyzing from a root directory

---

## Step 5 — Create the Agentic Workflow Definition

This is the core file that defines the AI agent's behavior. Create `.github/workflows/corn-flakes-detection.md`:

The file has two parts:
1. **YAML Frontmatter** (between `---` markers) — configures triggers, permissions, tools, and safe outputs
2. **Markdown Body** — the agent's prompt/instructions

### Frontmatter Structure

```yaml
---
description: |
  Daily flaky test detection workflow that analyzes test artifacts, creates issues
  for flaky tests, and generates a daily status issue with metrics and recommendations.

on:
  schedule: daily

timeout-minutes: 30
strict: false

permissions:
  actions: read
  contents: read
  attestations: read
  pull-requests: read
  issues: read
  discussions: read

steps:
  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.11'

  - name: Prepare artifacts directory
    run: mkdir -p ./artifacts ./reports

  - name: Download test artifacts from recent runs
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    run: |
      gh run list --workflow=test.yml --limit 20 --json databaseId,conclusion,createdAt,name,headSha,headBranch > ./artifacts/runs.json
      for RUN_ID in $(python3 -c "import json,sys; [print(r['databaseId']) for r in json.load(sys.stdin)]" < ./artifacts/runs.json); do
        mkdir -p ./artifacts/$RUN_ID
        gh run download "$RUN_ID" -n test-results -D ./artifacts/$RUN_ID 2>>./artifacts/download.log || echo "No test-results artifact for run $RUN_ID" >> ./artifacts/download.log
      done

env:
  GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

network: {}

tools:
  github:
    toolsets: [default, actions]
  bash:
    - "python .github/workflows/scripts/analyze_gh_test_failures.py:*"
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
    close-older-issues: false
    max: 51
  close-issue:
    required-title-prefix: "[corn flakes detection] "
    target: "*"
    max: 60
  update-issue:
    target: "*"
    max: 50
  assign-to-agent:
    name: "copilot"
    target: "*"
    max: 50
    ignore-if-error: true
  noop:
---
```

### Key Frontmatter Fields Explained

| Field | Purpose |
|---|---|
| `on: schedule: daily` | Runs once per day (gh-aw picks a scattered cron time) |
| `strict: false` | **Required** when using `${{ secrets.GITHUB_TOKEN }}` in `env:` blocks |
| `permissions` | Read-only permissions for the workflow steps (write permissions for issues are handled by safe outputs) |
| `steps` | Pre-agent setup steps — downloads test artifacts before the AI agent starts |
| `network: {}` | Disables external network access for the agent (security best practice) |
| `tools` | Restricts which tools the agent can use — only specific bash commands are allowed |
| `cache-memory: true` | Enables persistent memory across runs so the agent can track trends |
| `safe-outputs` | Defines what write actions the agent is allowed to perform (issue creation, updates, closing, assignment) |

### Markdown Body (Agent Prompt)

After the closing `---`, write the agent's instructions in Markdown. The prompt should describe:

1. What the agent should do (analyze test artifacts, detect flaky tests)
2. How to use the available tools (bash commands, Python script, GitHub CLI)
3. Step-by-step process for analysis
4. How to create/update/close issues
5. How to generate the daily summary
6. Error handling guidelines

You can copy the full prompt from this repository's `.github/workflows/corn-flakes-detection.md` as a starting point and customize it for your needs.

> 📖 **Docs**: [Agentic Workflow Definition Reference](https://gh.io/gh-aw)

---

## Step 6 — Compile the Agentic Workflow

After creating the `.md` file, compile it to generate the `.lock.yml` GitHub Actions workflow file:

```bash
gh aw compile corn-flakes-detection
```

This produces:
- `.github/workflows/corn-flakes-detection.lock.yml` — the actual GitHub Actions workflow (auto-generated, do NOT edit manually)
- `.github/aw/actions-lock.json` — action version pinning

> [!WARNING]
> **Always recompile** after editing the `.md` file. Both the `.md` and `.lock.yml` files must be committed together.

> 📖 **Docs**: [Compiling Workflows](https://gh.io/gh-aw)

---

## Step 7 — Configure Repository Tokens & Permissions

### Required: `GITHUB_TOKEN` (Automatic)

The built-in `GITHUB_TOKEN` is used automatically and needs these permissions:

| Permission | Level | Used For |
|---|---|---|
| `actions` | `read` | Listing workflow runs, downloading artifacts |
| `contents` | `read` | Reading repository files |
| `attestations` | `read` | Reading attestation data |
| `pull-requests` | `read` | Reading pull request metadata |
| `issues` | `read` | Reading issue data (write handled by safe outputs) |
| `discussions` | `read` | Reading discussion data |

> [!NOTE]
> The workflow declares read-only permissions. Write operations (creating issues, closing issues, updating issues) are handled through **safe outputs**, which use a separate privileged token managed by gh-aw.

### Required: `COPILOT_GITHUB_TOKEN`

The `COPILOT_GITHUB_TOKEN` secret is required for the Copilot Coding Agent to run. This is validated during the workflow's activation job.

- **How to set it**: Go to **Settings → Secrets and variables → Actions → New repository secret**
- **Value**: A GitHub token (classic or fine-grained) with permissions for Copilot

> 📖 **Docs**: [Engine Configuration — GitHub Copilot](https://gh.io/gh-aw) (see the Engines → GitHub Copilot section)

### Required: `GH_AW_AGENT_TOKEN` (for issue management and agent assignment)

The `GH_AW_AGENT_TOKEN` is **required** for the full extent of the flaky test detector's features, including updating issues, creating pull requests, and assigning Copilot Coding Agent to flaky test issues. The default `GITHUB_TOKEN` is insufficient for these operations.

- **How to set it**: Go to **Settings → Secrets and variables → Actions → New repository secret**
- **Name**: `GH_AW_AGENT_TOKEN`
- **Value**: A fine-grained PAT with the following permissions:

| Permission | Level | Used For |
|---|---|---|
| `contents` | Read and write | Reading repository files and creating branches/PRs for fixes |
| `pull-requests` | Read and write | Creating and managing pull requests for flaky test fixes |
| `issues` | Read and write | Creating, updating, closing issues and assigning the Copilot agent |
| `metadata` | Read | Repository metadata access (automatically granted with any fine-grained PAT) |

The `assign-to-agent` safe output uses an explicit token configured via the `github-token` field:

```
CORN_GH_AW_ASSIGN_ISSUES_TOKEN
```

> [!WARNING]
> Without `GH_AW_AGENT_TOKEN`, the workflow will still run but with **degraded functionality** — the agent will not be able to assign Copilot to flaky test issues or create pull requests for fixes. The workflow uses `ignore-if-error: true` on `assign-to-agent` to avoid hard failures, but you will miss out on automatic fix attempts.

### Repository Settings

Ensure the following repository settings are configured:

1. **Actions permissions**: Go to **Settings → Actions → General** and ensure "Allow all actions and reusable workflows" is selected (or at minimum allow `github/gh-aw` actions)
2. **Workflow permissions**: Under **Settings → Actions → General → Workflow permissions**, ensure the `GITHUB_TOKEN` has at least read permissions for the required scopes
3. **Issues**: Ensure Issues are enabled on the repository (**Settings → General → Features → Issues**)

---

## Step 8 — Commit and Enable

Commit all the files to your repository:

```bash
git add \
  .github/workflows/copilot-setup-steps.yml \
  .github/workflows/test.yml \
  .github/workflows/corn-flakes-detection.md \
  .github/workflows/corn-flakes-detection.lock.yml \
  .github/workflows/scripts/analyze_gh_test_failures.py \
  .github/aw/actions-lock.json

git commit -m "feat: add corn-flakes-detection agentic workflow"
git push
```

The workflow will:
1. Run on the daily schedule (cron time assigned during compile)
2. Download test artifacts from recent `test.yml` runs
3. Have the Copilot agent analyze flaky tests and create/manage issues
4. Assign Copilot Coding Agent to fix flaky tests (requires `GH_AW_AGENT_TOKEN`)

You can also trigger it manually via **Actions → Daily Flaky Test Repo Status 🔍 → Run workflow**.

---

## File Structure Reference

After setup, your repository should have these files:

```
your-repo/
├── .github/
│   ├── aw/
│   │   └── actions-lock.json               # Auto-generated action version pins
│   └── workflows/
│       ├── copilot-setup-steps.yml          # Copilot Agent environment setup
│       ├── test.yml                         # Your test workflow (uploads artifacts)
│       ├── corn-flakes-detection.md         # Agentic workflow definition (you edit this)
│       ├── corn-flakes-detection.lock.yml   # Compiled workflow (auto-generated, do NOT edit)
│       ├── agentics-maintenance.yml         # Auto-generated maintenance workflow (if applicable)
│       └── scripts/
│           ├── analyze_gh_test_failures.py  # JUnit XML test report parser
│           └── analyze_test_results.py      # Multi-framework report analyzer
├── <language>/                              # Your project source and tests
│   ├── <build-config>                       # e.g., pom.xml, package.json, go.mod, etc.
│   ├── <source-code>/
│   ├── <tests>/
│   └── reports/                             # Test reports (generated at runtime)
└── ...
```

---

## Token & Permissions Reference

| Token / Secret | Required? | How to Create | Permissions Needed |
|---|---|---|---|
| `GITHUB_TOKEN` | ✅ Automatic | Built-in, no setup needed | `actions: read`, `contents: read`, `issues: read`, `pull-requests: read` |
| `COPILOT_GITHUB_TOKEN` | ✅ Yes | Repository secret | Copilot access — see [engine docs](https://gh.io/gh-aw) |
| `GH_AW_AGENT_TOKEN` | ✅ Yes | Repository secret (fine-grained PAT) | `contents: read/write`, `pull-requests: read/write`, `issues: read/write`, `metadata: read` (auto-granted) |
| `CORN_GH_AW_ASSIGN_ISSUES_TOKEN` | ✅ Yes | Repository secret (PAT) | Same as `GH_AW_AGENT_TOKEN` — explicitly configured for the `assign-to-agent` safe output via `github-token` field |

---

## Customization

### Changing the Schedule

Edit the `on:` section in the frontmatter of your `.md` file:

```yaml
on:
  schedule: daily       # Once per day (default)
  # schedule: hourly    # Every hour
  # schedule: weekly    # Once per week
```

Then recompile: `gh aw compile corn-flakes-detection`

### Adjusting Safe Output Limits

The `max` field on each safe output controls how many times the agent can call that action per run:

```yaml
safe-outputs:
  create-issue:
    max: 51         # Increase if you have more than 50 flaky tests
  close-issue:
    max: 60
  update-issue:
    max: 50
```

### Customizing Labels

Change the `labels` on `create-issue` to match your project's labeling convention:

```yaml
safe-outputs:
  create-issue:
    title-prefix: "[corn flakes detection] "
    labels: [flaky-test, automated, ci]    # Your custom labels
```

### Changing the Title Prefix

The `title-prefix` ensures all issues created by this workflow are easily identifiable and can be managed (closed, updated) by the agent:

```yaml
safe-outputs:
  create-issue:
    title-prefix: "[your-prefix] "
  close-issue:
    required-title-prefix: "[your-prefix] "
```

> [!WARNING]
> The `title-prefix` in `create-issue` and `required-title-prefix` in `close-issue` **must match** — otherwise the agent won't be able to close its own issues.

---

## Troubleshooting

### Workflow fails at "Validate COPILOT_GITHUB_TOKEN secret"

**Cause**: The `COPILOT_GITHUB_TOKEN` secret is not set.

**Fix**: Add the secret in **Settings → Secrets and variables → Actions → New repository secret**.

### Agent cannot assign Copilot to issues (FORBIDDEN error)

**Cause**: The `GH_AW_AGENT_TOKEN` secret is missing or has insufficient permissions. The default `GITHUB_TOKEN` lacks permissions for the `replaceActorsForAssignable` GraphQL mutation.

**Fix**: Create a fine-grained PAT with `contents: read/write`, `pull-requests: read/write`, and `issues: read/write` permissions, then add it as the `GH_AW_AGENT_TOKEN` repository secret (see [Step 7](#step-7--configure-repository-tokens--permissions)). The workflow uses `ignore-if-error: true` so this won't cause a hard failure, but features will be degraded.

### No test artifacts found

**Cause**: The test workflow either hasn't run yet or isn't uploading artifacts with the name `test-results`.

**Fix**: Ensure your test workflow:
1. Uses `actions/upload-artifact@v4` to upload per-language results (e.g., `test-results-java`, `test-results-python`)
2. Includes a `collect-results` job that merges all per-language artifacts into a single `test-results` artifact
3. Uploads JUnit XML reports in the correct language-specific paths (see [Step 3](#step-3--add-the-test-workflow))
4. Has `continue-on-error: true` on the test step so artifacts are uploaded on failure

### Compilation fails with "strict mode" error

**Cause**: Using `${{ secrets.GITHUB_TOKEN }}` in `env:` blocks with `strict: true` (the default).

**Fix**: Add `strict: false` to the frontmatter of your `.md` file.

---

## Supported Report Formats

> [!NOTE]
> The corn-flakes-detection workflow supports **any project** that produces **JUnit XML** test reports. The following languages and frameworks have been tested and have example configurations in this repository:
>
> | Language | Framework | Report Mechanism |
> |----------|-----------|-----------------|
> | Java | JUnit 5 | Maven Surefire (`target/surefire-reports/TEST-*.xml`) |
> | Kotlin | kotlin.test | Gradle (`build/test-results/**/*.xml`) |
> | Python | pytest / unittest | `--junitxml` flag |
> | TypeScript | Jest / Playwright | `jest-junit` reporter / `--reporter=junit` |
> | Go | built-in testing | `gotestsum --junitfile` |
> | C# | xUnit.net | `--logger "junit"` |
> | Rust | cargo test | `cargo2junit` pipe |
> | C++ | Google Test | `ctest --output-junit` |
> | C | Unity | `ctest --output-junit` |
> | Swift | XCTest | Text output (parsed by analyzer) |
> | PHP | PHPUnit | `--log-junit` flag |
> | Ruby | RSpec | `rspec_junit_formatter` |
> | Elixir | ExUnit | `junit_formatter` |
> | Dart | dart test | `junitreport:tojunit` |
>
> If your language/framework produces JUnit XML, it should work — configure the test workflow to upload the XML as an artifact named `test-results`.

---

## Resources

- **GitHub Agentic Workflows (gh-aw)**: [https://gh.io/gh-aw](https://gh.io/gh-aw)
- **gh-aw Overview**: [https://github.github.com/gh-aw/introduction/overview/](https://github.github.com/gh-aw/introduction/overview/)
- **Safe Outputs Reference**: [https://gh.io/gh-aw](https://gh.io/gh-aw) (see Reference → Safe Outputs)
- **Engine Configuration (Copilot)**: [https://gh.io/gh-aw](https://gh.io/gh-aw) (see Reference → Engines → GitHub Copilot)
- **Assign-to-Agent Reference**: [https://gh.io/gh-aw](https://gh.io/gh-aw) (see Reference → Safe Outputs → assign-to-agent)
- **gh CLI**: [https://cli.github.com/](https://cli.github.com/)
- **This repository (corn-test)**: [https://github.com/mbianchidev/corn-test](https://github.com/mbianchidev/corn-test)
