# MCP Server Capabilities Matrix

**Comprehensive Reference for DIP-SMC-PSO Debugging**

This matrix documents all available MCP servers, their capabilities, use cases, and integration patterns for systematic debugging.

## Server Overview

| Server | Category | Status | Priority | Installation |
|--------|----------|--------|----------|--------------|
| **ruff** | Code Quality | ✅ Active | Critical | `pip install ruff` |
| **vulture** | Code Quality | ✅ Active | High | `pip install vulture` |
| **playwright** | Browser Testing | ✅ Active | High | `npm install -g @modelcontextprotocol/server-playwright` |
| **pytest-mcp** | Testing | ✅ Active | Critical | Built-in with pytest |
| **git-mcp** | Version Control | ✅ Active | Critical | Built-in with git |
| **filesystem** | File Operations | ✅ Active | Critical | Built-in |
| **sequential-thinking** | Analysis | ✅ Active | Medium | MCP standard |
| **numpy-mcp** | Numerical Computing | ✅ Active | High | Custom (.mcp_servers/numpy-mcp) |
| **github** | Issue Management | ✅ Active | Medium | `gh` CLI or MCP |
| **sqlite-mcp** | Data Analysis | ⚠️ Optional | Low | `pip install sqlite-mcp` |
| **pandas-mcp** | Data Analysis | ✅ Active | Medium | Custom (.mcp_servers/pandas-mcp-server) |

## Detailed Capabilities

### 1. RUFF - Code Quality Linting

**Purpose:** PEP 8 compliance, style enforcement, auto-fixes

**Capabilities:**
- ✅ Detect 800+ Python linting rules
- ✅ Auto-fix safe issues (F401, F541, F841, etc.)
- ✅ JSON/text/grouped output formats
- ✅ Configurable rule selection
- ✅ Fast (10-100x faster than flake8)

**Use Cases:**
- Code quality analysis workflow
- Pre-commit hooks
- CI/CD pipeline validation
- Migration from flake8/pylint

**Commands:**
```bash
# Analysis
ruff check src/ tests/ --statistics
ruff check src/ tests/ --output-format=json

# Auto-fix
ruff check src/ tests/ --fix
ruff check src/ tests/ --fix --unsafe-fixes

# Specific rules
ruff check src/ --select E,F,W  # Errors, pyflakes, warnings
```

**Integration Points:**
- Phase 1 & 2 of Complete Debugging Workflow
- Code Quality Analysis Workflow
- Pre-commit validation

---

### 2. VULTURE - Dead Code Detection

**Purpose:** Find unused code (functions, variables, imports, classes)

**Capabilities:**
- ✅ Detect unused variables, functions, classes
- ✅ Confidence scoring (0-100%)
- ✅ Whitelist support for false positives
- ✅ Configurable minimum confidence threshold
- ✅ Reports line numbers and file paths

**Use Cases:**
- Dead code cleanup
- Dependency optimization
- Code coverage improvement
- Refactoring preparation

**Commands:**
```bash
# Standard scan
vulture src/ tests/ --min-confidence 80

# High confidence only
vulture src/ tests/ --min-confidence 90

# Production code only (avoid test false positives)
vulture src/ --min-confidence 80
```

**Common False Positives:**
- Pytest fixture parameters
- Context manager protocol vars (`__exit__`)
- Abstract method parameters
- Protocol stubs

**Integration Points:**
- Phase 1 of Complete Debugging Workflow
- Code Quality Analysis Workflow
- Refactoring workflows

---

### 3. Playwright - Browser Automation

**Purpose:** Automate browser testing, capture screenshots, UI validation

**Capabilities:**
- ✅ Cross-browser testing (Chromium, Firefox, WebKit)
- ✅ Screenshot capture (full page, specific elements)
- ✅ UI interaction (clicks, typing, navigation)
- ✅ Performance measurement (load times, metrics)
- ✅ Network request monitoring
- ✅ Console error detection
- ✅ Mobile/tablet viewport emulation

**Use Cases:**
- Streamlit dashboard testing
- Visual regression testing
- UI/UX validation
- Performance monitoring
- End-to-end workflow testing

**Commands:**
```bash
# Install browsers
npx playwright install

# Run Playwright MCP server
npx @modelcontextprotocol/server-playwright
```

**Integration Points:**
- Streamlit Testing Workflow
- Pre-deployment validation
- Visual regression testing
- Performance analysis

**Example Usage:**
```plaintext
/test-browser
"Screenshot Streamlit dashboard at localhost:8501"
"Test classical SMC simulation workflow"
"Measure dashboard load time"
```

---

### 4. Pytest-MCP - Test Execution

**Purpose:** Run tests, collect coverage, analyze failures

**Capabilities:**
- ✅ Execute test suites with filtering
- ✅ Collect code coverage (line, branch)
- ✅ Generate HTML/XML/JSON reports
- ✅ Parallel test execution
- ✅ Fixture management
- ✅ Benchmark integration (pytest-benchmark)
- ✅ Property-based testing (Hypothesis)

**Use Cases:**
- Test debugging workflow
- Coverage analysis
- Regression testing
- Performance benchmarking
- CI/CD validation

**Commands:**
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Run specific tests
pytest tests/test_controllers/ -k "test_classical_smc"

# Run with benchmarks
pytest tests/test_benchmarks/ --benchmark-only
```

**Integration Points:**
- Phase 3 of Complete Debugging Workflow
- Test Debugging Workflow
- CI/CD pipelines
- Pre-commit validation

---

### 5. Git-MCP - Version Control

**Purpose:** Commit, push, history analysis, blame tracking

**Capabilities:**
- ✅ Commit with automated messages
- ✅ Push to remote repositories
- ✅ View commit history and diffs
- ✅ Blame analysis (who changed what)
- ✅ Branch management
- ✅ Conflict resolution
- ✅ Pre-commit hook integration

**Use Cases:**
- Automatic commit after fixes
- Track changes across debugging sessions
- Generate changelogs
- Issue linking
- Code review preparation

**Commands:**
```bash
# Status
git status

# Commit with AI-generated message
git add -A && git commit -m "..."

# Push
git push origin main

# History
git log --oneline -n 10
git diff HEAD~1
```

**Integration Points:**
- Phase 2, 6 of Complete Debugging Workflow
- All workflows (for change tracking)
- Session continuity

---

### 6. Filesystem - File Operations

**Purpose:** Search, read, analyze files and directories

**Capabilities:**
- ✅ Glob pattern matching
- ✅ Grep content search (regex support)
- ✅ File read/write/edit
- ✅ Directory traversal
- ✅ Metadata extraction (size, modified time)
- ✅ Batch operations

**Use Cases:**
- Code search and analysis
- Log file analysis
- Configuration validation
- Documentation generation
- Batch file operations

**Commands:**
```bash
# Search patterns
find src/ -name "*.py" -type f
grep -r "ClassicalSMC" src/

# Read files
cat src/controllers/classic_smc.py

# File stats
ls -lh logs/
du -sh .test_artifacts/
```

**Integration Points:**
- All workflows (fundamental tool)
- Log analysis
- Configuration management
- Report generation

---

### 7. Sequential-Thinking - Methodical Analysis

**Purpose:** Step-by-step problem decomposition and systematic reasoning

**Capabilities:**
- ✅ Break complex problems into steps
- ✅ Track reasoning chains
- ✅ Validate assumptions
- ✅ Generate debugging hypotheses
- ✅ Document decision rationale

**Use Cases:**
- Complex bug investigation
- Design decision analysis
- Architecture review
- Optimization strategy
- Root cause analysis

**Integration Points:**
- Phase 3, 4 of Complete Debugging Workflow
- Test debugging (isolating failures)
- Thread safety analysis (deadlock detection)
- Performance bottleneck identification

---

### 8. Numpy-MCP - Numerical Computing

**Purpose:** Array operations, linear algebra validation, numerical analysis

**Capabilities:**
- ✅ Array creation and manipulation
- ✅ Linear algebra operations (inverse, eigenvalues, SVD)
- ✅ Matrix condition number analysis
- ✅ Numerical stability checks
- ✅ Random number generation (reproducible)
- ✅ Signal processing utilities

**Use Cases:**
- Validate dynamics equations
- Check matrix conditioning (LinAlgError debugging)
- Analyze controller gains
- Verify numerical stability
- Test signal processing algorithms

**Integration Points:**
- Phase 4 of Complete Debugging Workflow (thread safety with numpy operations)
- Numerical stability validation
- Controller gain validation
- Dynamics model verification

---

### 9. GitHub - Issue Management

**Purpose:** Create issues, track bugs, manage projects

**Capabilities:**
- ✅ Create/update/close issues
- ✅ Add labels and milestones
- ✅ Link commits to issues
- ✅ Search issue history
- ✅ Project board management
- ✅ Pull request integration

**Use Cases:**
- Track manual review items
- Document known issues
- Link fixes to problems
- Project planning
- Team coordination

**Commands:**
```bash
# Create issue
gh issue create --title "..." --body "..." --label "bug"

# List issues
gh issue list --label "code-quality"

# View issue
gh issue view 123
```

**Integration Points:**
- Phase 6 of Complete Debugging Workflow
- Manual review tracking
- Bug reporting
- Feature requests

---

### 10. SQLite-MCP - Data Analysis (Optional)

**Purpose:** Query simulation results, analyze metrics databases

**Capabilities:**
- ✅ SQL query execution
- ✅ Database schema inspection
- ✅ Aggregate statistics
- ✅ Time-series analysis
- ✅ Join operations for complex queries

**Use Cases:**
- Analyze PSO optimization history
- Query simulation result databases
- Generate performance reports
- Track metrics over time
- Benchmark comparisons

**Commands:**
```sql
-- Query PSO results
SELECT iteration, best_cost FROM pso_history WHERE run_id = 123;

-- Aggregate statistics
SELECT controller, AVG(settling_time) FROM simulations GROUP BY controller;
```

**Integration Points:**
- Performance Analysis Workflow
- PSO optimization analysis
- Benchmark result comparison

---

### 11. Pandas-MCP - Data Analysis

**Purpose:** DataFrame operations, data manipulation, statistical analysis

**Capabilities:**
- ✅ CSV/JSON data loading
- ✅ DataFrame filtering and transformation
- ✅ Statistical computations
- ✅ Time-series operations
- ✅ Data visualization preparation
- ✅ Merge/join operations

**Use Cases:**
- Analyze simulation results
- Process PSO optimization data
- Generate statistical reports
- Data cleaning and preprocessing
- Result comparison

**Integration Points:**
- Performance Analysis Workflow
- PSO convergence analysis
- Statistical validation
- Result aggregation

---

## Workflow Integration Matrix

| Workflow | Primary Servers | Secondary Servers | Duration |
|----------|-----------------|-------------------|----------|
| **Complete Debugging** | ruff, vulture, pytest-mcp, git-mcp | filesystem, sequential-thinking, numpy-mcp | 3 hours |
| **Code Quality** | ruff, vulture | filesystem, git-mcp | 45 min |
| **Streamlit Testing** | playwright | filesystem | 65 min |
| **Test Debugging** | pytest-mcp | sequential-thinking, filesystem | 45 min |
| **Production Validation** | filesystem | github | 30 min |
| **Performance Analysis** | numpy-mcp, pandas-mcp | sqlite-mcp, filesystem | 60 min |

## Server Selection Guide

### When to Use Each Server

**RUFF:**
- Code review preparation
- Pre-commit validation
- Style enforcement
- Legacy code cleanup

**VULTURE:**
- Refactoring preparation
- Dependency optimization
- Code coverage improvement
- Dead code cleanup

**Playwright:**
- UI/UX validation
- Visual regression testing
- Performance monitoring
- End-to-end testing
- Pre-deployment checks

**Pytest-MCP:**
- Debugging test failures
- Coverage analysis
- Regression testing
- Benchmark validation
- CI/CD integration

**Git-MCP:**
- Change tracking
- Commit automation
- History analysis
- Issue linking

**Filesystem:**
- Log analysis
- Code search
- Configuration management
- Documentation generation

**Sequential-Thinking:**
- Complex bug investigation
- Design decisions
- Root cause analysis
- Optimization strategy

**Numpy-MCP:**
- Numerical validation
- Matrix conditioning
- Stability analysis
- Signal processing

**GitHub:**
- Issue tracking
- Team coordination
- Project planning
- Release management

**SQLite/Pandas-MCP:**
- Result analysis
- Statistical reporting
- Performance tracking
- Data aggregation

## Installation & Setup

### Python-based Servers

```bash
# Install via pip
pip install ruff vulture pytest pytest-cov pytest-benchmark

# Verify installation
ruff --version
vulture --version
pytest --version
```

### Node.js-based Servers

```bash
# Install Playwright MCP
npm install -g @modelcontextprotocol/server-playwright

# Install browsers
npx playwright install

# Verify
npx playwright --version
```

### Custom Servers

```bash
# Clone custom MCP servers
cd .mcp_servers/

# Numpy MCP
git clone https://github.com/your-org/numpy-mcp

# Pandas MCP
git clone https://github.com/your-org/pandas-mcp-server
```

## Best Practices

### 1. Server Selection
- ✅ Use most specific server for task (don't use filesystem for tests when pytest-mcp available)
- ✅ Combine servers for comprehensive analysis
- ✅ Start with high-priority servers (ruff, pytest-mcp, git-mcp)

### 2. Workflow Integration
- ✅ Follow established workflows when possible
- ✅ Use parallel execution for independent servers
- ✅ Validate each phase before moving to next

### 3. Result Validation
- ✅ Cross-check results from multiple servers
- ✅ Generate reports for all major analyses
- ✅ Commit incremental changes

### 4. Maintenance
- ✅ Keep servers updated to latest versions
- ✅ Review capabilities quarterly
- ✅ Document new server integrations

## Troubleshooting

### Server Not Available

```bash
# Check installation
which ruff  # or npm list -g | grep playwright

# Reinstall
pip install --upgrade ruff
npm install -g @modelcontextprotocol/server-playwright --force
```

### Server Timeout

```bash
# Increase timeout in requests
# For Playwright: page.wait_for_selector("selector", timeout=60000)
# For pytest: pytest --timeout=300
```

### Permission Errors

```bash
# Check Claude Code settings
cat .claude/settings.local.json

# Add permissions if needed
# "allow": ["Bash(python:*)", "Bash(npx:*)"]
```

---

**Version:** 1.0.0
**Last Updated:** 2025-10-10
**Total Servers:** 11 (9 active, 2 optional)
**Coverage:** Code Quality, Testing, Browser Automation, Version Control, Data Analysis
