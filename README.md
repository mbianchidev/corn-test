# 🌽 corn-test

**Corn: the flakes detection agentic workflow**

A multi-language flaky test detection system powered by [GitHub Agentic Workflows (gh-aw)](https://gh.io/gh-aw). This repository contains sample applications with intentionally flaky tests across **14 programming languages**, used to validate and demonstrate automated flaky test detection, triage, and remediation via AI agents.

---

## How It Works

1. **Test workflows** run across all language projects on a schedule (and on push/PR)
2. Each language job uploads JUnit XML test reports as artifacts
3. The **corn-flakes-detection** agentic workflow analyzes test artifacts daily
4. An AI agent detects flaky tests, creates/manages GitHub Issues, and assigns [Copilot Coding Agent](https://github.com/features/copilot) to fix them

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  test.yml   │────▶│  Test Artifacts  │────▶│  corn-flakes-       │
│ (14 langs)  │     │  (JUnit XML)     │     │  detection agent    │
└─────────────┘     └──────────────────┘     └────────┬────────────┘
                                                       │
                                          ┌────────────▼────────────┐
                                          │  GitHub Issues          │
                                          │  + Copilot Agent Fixes  │
                                          └─────────────────────────┘
```

---

## Supported Languages & Frameworks

| Language | Folder | Test Framework(s) | Report Format |
|----------|--------|-------------------|---------------|
| **Java** | `java/` | JUnit 5 (Maven Surefire) | JUnit XML |
| **Python** | `python/` | pytest + unittest | JUnit XML |
| **TypeScript** | `typescript/` | Jest + Playwright | JUnit XML |
| **Go** | `golang/` | built-in testing (gotestsum) | JUnit XML |
| **C#** | `csharp/` | xUnit.net | JUnit XML |
| **Rust** | `rust/` | cargo test (cargo2junit) | JUnit XML |
| **C++** | `cpp/` | Google Test (gTest) | CTest JUnit XML |
| **C** | `c/` | Unity (CTest) | CTest JUnit XML |
| **Swift** | `swift/` | Swift Testing (XCTest) | Text output |
| **Kotlin** | `kotlin/` | kotlin.test (Gradle) | JUnit XML |
| **PHP** | `php/` | PHPUnit | JUnit XML |
| **Ruby** | `ruby/` | RSpec | JUnit XML |
| **Elixir** | `elixir/` | ExUnit | JUnit XML |
| **Dart** | `dart/` | dart test | JUnit XML |

---

## Project Structure

Each language folder follows the same pattern — a `MathOperations` class (deterministic) and a `RandomMathOperations` class (intentionally flaky):

```
corn-test/
├── java/                    # Java (JUnit 5 / Maven)
├── python/                  # Python (pytest + unittest)
├── typescript/              # TypeScript (Jest + Playwright)
├── golang/                  # Go (built-in testing)
├── csharp/                  # C# (xUnit.net / .NET)
├── rust/                    # Rust (cargo test)
├── cpp/                     # C++ (Google Test / CMake)
├── c/                       # C (Unity / CMake)
├── swift/                   # Swift (XCTest / SPM)
├── kotlin/                  # Kotlin (kotlin.test / Gradle)
├── php/                     # PHP (PHPUnit / Composer)
├── ruby/                    # Ruby (RSpec / Bundler)
├── elixir/                  # Elixir (ExUnit / Mix)
├── dart/                    # Dart (dart test)
├── docs/
│   └── ADOPTION_GUIDE.md    # How to adopt corn-flakes-detection in your repo
└── .github/
    └── workflows/
        ├── test.yml                         # Multi-language test runner
        ├── corn-flakes-detection.md         # Agentic workflow definition
        ├── corn-flakes-detection.lock.yml   # Compiled workflow (auto-generated)
        └── scripts/
            ├── analyze_gh_test_failures.py  # JUnit XML test report analyzer
            └── analyze_test_results.py      # Multi-framework report analyzer
```

---

## The Flaky Test Pattern

Every language project implements the same two classes:

### MathOperations (Deterministic)
Reliable mathematical operations that always produce consistent results:
- `add`, `subtract`, `multiply`, `divide` (with zero-check)
- `power`, `factorial`, `derivative` (polynomial)
- `pi` (first 40 decimals), `gcd` (Euclidean algorithm)

### RandomMathOperations (Intentionally Flaky)
Functions designed to produce intermittent test failures:

| Function | Behavior | Flakiness |
|----------|----------|-----------|
| `generateRandomOddNumber()` | Returns odd number 1–99 | ✅ Reliable |
| `generateRandomEvenNumber()` | Returns even number 0–100 | ⚠️ **5% chance of returning odd** (intentional flaw) |
| `generateRandomPrimeCandidate()` | Returns prime from list 2–97 | ✅ Reliable |

Each language's test suite runs the flaky tests **20 times per execution** to amplify the detection signal.

---

## Running Tests Locally

Each language folder is self-contained. Navigate to the folder and use the language's standard tooling:

```bash
# Java
cd java && mvn test

# Python
cd python && pip install -r requirements.txt && python -m pytest -v

# TypeScript
cd typescript && npm ci && npm test

# Go
cd golang && go test -v ./...

# C# 
cd csharp && dotnet test

# Rust
cd rust && cargo test

# C++ 
cd cpp && mkdir -p build && cd build && cmake .. && make && ctest

# C
cd c && mkdir -p build && cd build && cmake .. && make && ctest

# Swift
cd swift && swift test

# Kotlin
cd kotlin && ./gradlew test

# PHP
cd php && composer install && vendor/bin/phpunit

# Ruby
cd ruby && bundle install && bundle exec rspec

# Elixir
cd elixir && mix deps.get && mix test

# Dart
cd dart && dart pub get && dart test
```

---

## CI/CD Pipeline

The `.github/workflows/test.yml` runs **14 parallel jobs** (one per language), then a `collect-results` job merges all artifacts into a single `test-results` artifact consumed by the flake detection workflow.

All test jobs use `continue-on-error: true` to ensure artifacts are always uploaded, even when flaky tests fail.

---

## Adopting Corn-Flakes Detection

Want to add automated flaky test detection to your own repository? See the **[Adoption Guide](docs/ADOPTION_GUIDE.md)** for step-by-step instructions covering:

- Setting up the test workflow for your language
- Installing and configuring the agentic workflow
- Token and permission configuration
- Customization options

---

## Purpose

This project is designed for:
- 🔍 **Flake detection** — automatically identify tests that pass and fail intermittently
- 🤖 **AI-powered remediation** — Copilot Coding Agent is assigned to fix detected flaky tests
- 📊 **Reliability metrics** — track test stability across multiple languages and frameworks
- 🔄 **CI/CD resilience** — validate retry strategies and failure handling
- 📚 **Reference implementation** — example of multi-language test infrastructure with agentic workflows
