# 🌽 Corn Flakes Detection — Adoption Guide

> **Automated flaky test detection using GitHub Agentic Workflows (gh-aw)**

This guide explains how to adopt the **corn-flakes-detection** agentic workflow in your own repository. The workflow runs on a daily schedule, analyzes your test artifacts, detects flaky tests, creates and manages GitHub Issues for each flaky test, and optionally assigns Copilot Coding Agent to fix them.

> [!IMPORTANT]
> **Java-only support.** This workflow currently works **only for Java projects** that use **Maven Surefire** to produce JUnit XML test reports (`target/surefire-reports/`).
> Support for additional languages and test frameworks is planned — more to come soon.

---

## Table of Contents

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

## Prerequisites

Before you begin, ensure you have:

| Requirement | Details |
|---|---|
| **GitHub repository** | Public or private, with GitHub Actions enabled |
| **Java + Maven project** | Uses `maven-surefire-plugin` to produce JUnit XML reports in `target/surefire-reports/` |
| **GitHub Copilot** | A [GitHub Copilot](https://github.com/features/copilot) subscription (Business or Enterprise) for the Copilot Coding Agent integration |
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

You need a GitHub Actions workflow that runs your Java tests and uploads the Surefire reports as artifacts. Create `.github/workflows/test.yml`:

```yaml
name: Run Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: "0 6,12 * * *"  # Run twice daily to generate data for flaky detection

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up JDK 11
      uses: actions/setup-java@v4
      with:
        java-version: '11'
        distribution: 'temurin'
        cache: 'maven'

    - name: Build with Maven
      run: mvn clean compile

    - name: Run tests
      id: run_tests
      run: mvn test
      continue-on-error: true

    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: |
          target/surefire-reports/**/*
          target/*.log
        retention-days: 30
```

> [!IMPORTANT]
> The artifact **must** be named `test-results` — the agentic workflow downloads artifacts by this name.
> The `continue-on-error: true` on the test step ensures artifacts are uploaded even when tests fail.

---

## Step 4 — Add the Python Analyzer Script

The agentic workflow uses a Python script to parse JUnit/Surefire XML test reports into structured markdown. Copy the script from this repository:

```
.github/workflows/scripts/analyze_gh_test_failures.py
```

Place it at the same path in your repository:

```bash
mkdir -p .github/workflows/scripts
# Copy analyze_gh_test_failures.py into .github/workflows/scripts/
```

This script supports:
- Parsing Surefire XML reports (`TEST-*.xml`)
- Generating markdown summaries of test failures
- Local artifact analysis mode (used by the agentic workflow)

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

> 📖 **Docs**: [Engine Configuration — GitHub Copilot](https://github.github.com/gh-aw/reference/engines/#github-copilot-default)

### Optional: `GH_AW_AGENT_TOKEN` (for `assign-to-agent`)

The `assign-to-agent` safe output uses a token fallback chain:

```
GH_AW_ASSIGN_ISSUES_TOKEN → GH_AW_AGENT_TOKEN → GH_AW_GITHUB_TOKEN → GITHUB_TOKEN
```

If you want the agent to **assign Copilot Coding Agent to flaky test issues**, you need a PAT with elevated permissions because the default `GITHUB_TOKEN` is insufficient for the `replaceActorsForAssignable` GraphQL mutation.

| Token | Scope | Purpose |
|---|---|---|
| `GH_AW_AGENT_TOKEN` | `repo` (classic) or `issues: write` (fine-grained) | Assigning the Copilot agent to issues |

> [!TIP]
> The workflow uses `ignore-if-error: true` on `assign-to-agent`, so the workflow will not fail if this token is missing — it will just skip the assignment step. You can set this up later.

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
4. Optionally assign Copilot Coding Agent to fix flaky tests

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
│           └── analyze_gh_test_failures.py  # Test report parser script
├── pom.xml                                  # Maven configuration
└── src/
    ├── main/java/...                        # Your Java source code
    └── test/java/...                        # Your Java tests (JUnit 5 / Surefire)
```

---

## Token & Permissions Reference

| Token / Secret | Required? | How to Create | Permissions Needed |
|---|---|---|---|
| `GITHUB_TOKEN` | ✅ Automatic | Built-in, no setup needed | `actions: read`, `contents: read`, `issues: read`, `pull-requests: read` |
| `COPILOT_GITHUB_TOKEN` | ✅ Yes | Repository secret | Copilot access — see [engine docs](https://github.github.com/gh-aw/reference/engines/#github-copilot-default) |
| `GH_AW_AGENT_TOKEN` | ❌ Optional | Repository secret (PAT) | `repo` scope (classic) or `issues: write` (fine-grained) — needed for `assign-to-agent` |
| `GH_AW_ASSIGN_ISSUES_TOKEN` | ❌ Optional | Repository secret (PAT) | Write access to issues — alternative to `GH_AW_AGENT_TOKEN` for assignment |

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

**Cause**: The `GITHUB_TOKEN` lacks permissions for the `replaceActorsForAssignable` GraphQL mutation.

**Fix**: Create a PAT with `repo` scope and add it as `GH_AW_AGENT_TOKEN` secret. The workflow uses `ignore-if-error: true` so this won't block the rest of the workflow.

### No test artifacts found

**Cause**: The test workflow either hasn't run yet or isn't uploading artifacts with the name `test-results`.

**Fix**: Ensure your test workflow:
1. Uses `actions/upload-artifact@v4` with `name: test-results`
2. Uploads Surefire XML reports from `target/surefire-reports/`
3. Has `continue-on-error: true` on the test step so artifacts are uploaded on failure

### Compilation fails with "strict mode" error

**Cause**: Using `${{ secrets.GITHUB_TOKEN }}` in `env:` blocks with `strict: true` (the default).

**Fix**: Add `strict: false` to the frontmatter of your `.md` file.

---

## Current Limitations

> [!CAUTION]
> **Java only.** This workflow currently supports **only Java projects** with the following stack:
> - **Build tool**: Maven (with `maven-surefire-plugin`)
> - **Test framework**: JUnit 5 (or any framework producing Surefire-compatible XML reports)
> - **Report format**: JUnit XML (`target/surefire-reports/TEST-*.xml`)
>
> It does **not** yet support:
> - Gradle projects
> - JavaScript/TypeScript (Jest, Mocha, Vitest)
> - Python (pytest, unittest)
> - Go (gotestsum)
> - Other languages or test frameworks
>
> **More language support is coming soon.** Check the repository for updates.

---

## Resources

- **GitHub Agentic Workflows (gh-aw)**: [https://gh.io/gh-aw](https://gh.io/gh-aw)
- **gh-aw Overview**: [https://github.github.com/gh-aw/introduction/overview/](https://github.github.com/gh-aw/introduction/overview/)
- **Safe Outputs Reference**: [https://github.github.com/gh-aw/reference/safe-outputs/](https://github.github.com/gh-aw/reference/safe-outputs/)
- **Engine Configuration (Copilot)**: [https://github.github.com/gh-aw/reference/engines/#github-copilot-default](https://github.github.com/gh-aw/reference/engines/#github-copilot-default)
- **Assign-to-Agent Reference**: [https://github.github.com/gh-aw/reference/safe-outputs/#assign-to-agent-assign-to-agent](https://github.github.com/gh-aw/reference/safe-outputs/#assign-to-agent-assign-to-agent)
- **gh CLI**: [https://cli.github.com/](https://cli.github.com/)
- **This repository (corn-test)**: [https://github.com/mbianchidev/corn-test](https://github.com/mbianchidev/corn-test)
