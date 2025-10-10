# MCP Complete Debugging Workflow

**6-Phase Systematic Debugging for DIP-SMC-PSO Project**

This master workflow coordinates multiple MCP servers to perform comprehensive debugging, analysis, and validation of the control systems codebase.

## Overview

| Phase | Duration | MCP Servers Used | Output |
|-------|----------|------------------|--------|
| 1. Code Quality Analysis | 30 min | ruff, vulture, filesystem | RUFF/VULTURE reports |
| 2. Auto-Fix Safe Issues | 15 min | ruff, pytest-mcp, git-mcp | Zero linting errors |
| 3. Test Debugging | 45 min | pytest-mcp, sequential-thinking | ≥85% coverage |
| 4. Thread Safety Validation | 60 min | filesystem, numpy-mcp | Thread safety report |
| 5. Production Validation | 30 min | filesystem, github | Readiness score ≥7.5/10 |
| 6. Documentation & Reporting | 20 min | filesystem, github, git-mcp | Summary report |

**Total Time:** ~3 hours for complete execution

## Prerequisites

### Environment Check

```bash
# Python environment
python --version  # ≥3.9
pip list | grep -E "(ruff|vulture|pytest|numpy)"

# Node.js for Playwright
node --version  # ≥18.0
npm --version   # ≥9.0

# Git status
git status
git remote -v  # Verify: https://github.com/theSadeQ/dip-smc-pso.git
```

### Workspace Cleanup

```bash
# Remove stale artifacts
python scripts/cleanup/workspace_cleanup.py --verbose

# Check root directory items (target: ≤15)
ls | wc -l
```

## Phase 1: Code Quality Analysis (30 min)

### MCP Servers
- **ruff** - Code linting
- **vulture** - Dead code detection
- **filesystem** - File operations

### Steps

1. **Run RUFF Analysis**
   ```bash
   python -m ruff check src/ tests/ --output-format=json > ruff_analysis.json
   python -m ruff check src/ tests/ --statistics
   ```

2. **Run VULTURE Detection**
   ```bash
   python -m vulture src/ tests/ --min-confidence 80 > vulture_findings.txt
   ```

3. **Generate Analysis Reports**
   - Create `mcp-debugging/analysis_results/RUFF_FINDINGS_YYYYMMDD.md`
   - Create `mcp-debugging/analysis_results/VULTURE_FINDINGS_YYYYMMDD.md`
   - Prioritize issues (critical, high, medium, low)
   - Identify auto-fixable vs manual review

### Validation Criteria
- ✅ RUFF report generated with issue breakdown
- ✅ VULTURE report generated with confidence scores
- ✅ Issues categorized by priority
- ✅ Auto-fix candidates identified

### Example Report Structure

```markdown
# RUFF Analysis Report
**Total Issues:** X
**Auto-fixable:** Y

## Critical (Manual Review)
- E722: Bare except (file:line)
- E402: Module import not at top (file:line)

## Auto-fixable
- F541: f-string missing placeholders
- F401: Unused imports
- F841: Unused variables
```

## Phase 2: Auto-Fix Safe Issues (15 min)

### MCP Servers
- **ruff** - Apply auto-fixes
- **pytest-mcp** - Validate fixes
- **git-mcp** - Version control

### Steps

1. **Fix Critical Manual Issues**
   - Replace bare `except:` with `except Exception:`
   - Move module imports to top (or add `# noqa` if intentional)
   - Document unused parameters with `# noqa` + TODO

2. **Run RUFF Auto-fix**
   ```bash
   python -m ruff check --fix --unsafe-fixes src/ tests/
   ```

3. **Validate No Breakage**
   ```bash
   # Quick smoke tests
   python -m pytest tests/test_documentation/test_cross_references.py -v
   python -m pytest tests/ -k "test_initialization" --co
   ```

4. **Commit Changes**
   ```bash
   git add -A
   git commit -m "refactor(quality): Fix code quality issues from RUFF/VULTURE

   ### Changes:
   - Fix EXX: [description]
   - Fix FXXX: [description]

   [AI] Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

### Validation Criteria
- ✅ All auto-fixable RUFF issues resolved
- ✅ Smoke tests passing
- ✅ Pre-commit hooks passing
- ✅ Clean git commit created

## Phase 3: Test Debugging (45 min)

### MCP Servers
- **pytest-mcp** - Test execution
- **sequential-thinking** - Methodical analysis
- **filesystem** - Log analysis

### Steps

1. **Identify Test Issues**
   ```bash
   # Full test collection
   python -m pytest tests/ --collect-only

   # Run with verbose output
   python -m pytest tests/ -v --tb=short -x 2>&1 | tee test_run.log
   ```

2. **Analyze Failures**
   - Collection errors: Missing fixtures, import issues
   - Skipped tests: Reason analysis
   - Failed tests: Stack trace review
   - Coverage gaps: Identify uncovered code

3. **Debug Systematically**
   ```bash
   # Isolate failing test
   python -m pytest tests/path/to/test_file.py::test_name -vv

   # Run with debugging
   python -m pytest tests/path/to/test_file.py::test_name --pdb
   ```

4. **Generate Coverage Report**
   ```bash
   python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
   ```

### Validation Criteria
- ✅ All test collection errors resolved
- ✅ Skipped tests documented or fixed
- ✅ Coverage ≥85% overall
- ✅ Coverage ≥95% for critical components

### Coverage Targets

| Component | Target | Critical |
|-----------|--------|----------|
| Controllers | ≥95% | ✅ Yes |
| Dynamics | ≥90% | ✅ Yes |
| Optimization | ≥90% | ✅ Yes |
| Utils | ≥85% | No |
| Tests | ≥80% | No |

## Phase 4: Thread Safety Validation (60 min)

### MCP Servers
- **filesystem** - Script execution, log analysis
- **numpy-mcp** - Numerical analysis
- **sequential-thinking** - Deadlock detection

### Steps

1. **Run Thread Safety Tests**
   ```bash
   python scripts/test_thread_safety_fixes.py 2>&1 | tee thread_safety_results.log
   ```

2. **Analyze Failures**
   - Deadlock patterns
   - Race conditions
   - Concurrent access violations
   - Lock contention issues

3. **Review Suspected Components**
   ```python
   # High-risk areas
   - src/interfaces/monitoring/metrics_collector.py
   - src/interfaces/network/udp_interface.py
   - src/controllers/factory/thread_safety.py
   - src/hil/ (all files)
   ```

4. **Fix or Document**
   - **Option A:** Implement thread-safe patterns (locks, queues, atomics)
   - **Option B:** Document single-threaded constraint in CLAUDE.md

### Validation Criteria
- ✅ Thread safety tests passing OR
- ✅ Single-threaded constraint documented
- ✅ Production deployment guidance updated
- ✅ Monitoring added for concurrent operations

### Thread Safety Patterns

```python
# Pattern 1: Lock-based synchronization
with self._lock:
    # Critical section
    pass

# Pattern 2: Thread-safe queue
from queue import Queue
self._queue = Queue()

# Pattern 3: Atomic operations
from threading import Event
self._stop_event = Event()
```

## Phase 5: Production Validation (30 min)

### MCP Servers
- **filesystem** - Script execution
- **github** - Issue tracking

### Steps

1. **Run Validation Scripts**
   ```bash
   python scripts/verify_dependencies.py
   python scripts/test_memory_leak_fixes.py
   python scripts/test_spof_fixes.py
   python scripts/test_thread_safety_fixes.py
   ```

2. **Generate Readiness Report**
   ```bash
   python scripts/generate_production_readiness_report.py > production_readiness.md
   ```

3. **Calculate Readiness Score**
   ```
   Score = (
       dependency_safety * 0.25 +
       memory_safety * 0.25 +
       spof_removal * 0.25 +
       thread_safety * 0.25
   ) * 10

   Target: ≥7.5/10
   ```

4. **Update CLAUDE.md**
   ```markdown
   ## 12) Production Safety & Readiness

   **Production Readiness Score: X.X/10** (updated YYYY-MM-DD)

   ### Status
   - Dependency safety: [PASS/FAIL]
   - Memory safety: [PASS/FAIL]
   - SPOF removal: [PASS/FAIL]
   - Thread safety: [PASS/WARN/FAIL]
   ```

### Validation Criteria
- ✅ All validation scripts executed
- ✅ Production readiness score calculated
- ✅ CLAUDE.md updated
- ✅ Deployment guidance documented

## Phase 6: Documentation & Reporting (20 min)

### MCP Servers
- **filesystem** - Report generation
- **github** - Issue creation
- **git-mcp** - Commit and push

### Steps

1. **Generate Summary Report**
   ```markdown
   # MCP Debugging Session Summary
   **Date:** YYYY-MM-DD
   **Duration:** X hours
   **Status:** [Complete/Partial]

   ## Phase Results
   - Phase 1: [status] - X issues found
   - Phase 2: [status] - X fixes applied
   - Phase 3: [status] - X% coverage achieved
   - Phase 4: [status] - Thread safety [pass/documented]
   - Phase 5: [status] - Readiness score: X.X/10
   - Phase 6: [status] - Report generated

   ## Key Improvements
   - [Improvement 1]
   - [Improvement 2]

   ## Remaining Issues
   - [Issue 1] - [GitHub issue #X]
   - [Issue 2] - [GitHub issue #Y]
   ```

2. **Create GitHub Issues for Manual Review**
   ```bash
   # Use gh CLI or GitHub MCP
   gh issue create --title "Manual review: [description]" \
                   --body "[Details from analysis]" \
                   --label "code-quality,manual-review"
   ```

3. **Update CHANGELOG.md**
   ```markdown
   ## [Unreleased]

   ### Fixed
   - Resolved X RUFF linting errors
   - Fixed Y dead code instances
   - Improved test coverage to Z%

   ### Changed
   - Updated production readiness score to X.X/10
   - Enhanced thread safety documentation
   ```

4. **Commit and Push**
   ```bash
   git add -A
   git commit -m "docs(mcp): Complete MCP debugging session

   ### Summary
   - Code quality: X → 0 errors
   - Test coverage: X% → Y%
   - Production readiness: X.X/10 → Y.Y/10

   [AI] Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>"

   git push origin main
   ```

### Validation Criteria
- ✅ Summary report generated
- ✅ GitHub issues created for manual items
- ✅ CHANGELOG.md updated
- ✅ All changes committed and pushed

## Success Metrics

### Code Quality
- **RUFF Errors:** 0 (100% reduction)
- **VULTURE High-Confidence Issues:** <5
- **Bare Exceptions:** 0
- **Dead Code (Critical):** 0 documented

### Testing
- **Overall Coverage:** ≥85%
- **Critical Coverage:** ≥95%
- **Test Failures:** 0
- **Skipped Tests:** Documented

### Production Readiness
- **Readiness Score:** ≥7.5/10
- **Dependency Safety:** PASS
- **Memory Safety:** PASS
- **SPOF Removal:** PASS
- **Thread Safety:** PASS or documented constraint

### Documentation
- **Analysis Reports:** Generated
- **GitHub Issues:** Created for manual review
- **CHANGELOG:** Updated
- **Git History:** Clean commits with messages

## Troubleshooting

### Phase 1: RUFF/VULTURE Issues

**Problem:** Too many false positives in VULTURE

**Solution:** Increase confidence threshold or create whitelist
```bash
python -m vulture src/ tests/ --min-confidence 90
# Or create .vulture_whitelist.py
```

### Phase 2: Auto-fix Breaks Tests

**Problem:** RUFF auto-fix causes test failures

**Solution:** Revert specific files, apply fixes manually
```bash
git checkout -- path/to/problematic/file.py
# Apply fixes manually with understanding
```

### Phase 3: Low Test Coverage

**Problem:** Coverage below 85% target

**Solution:** Identify untested modules, add targeted tests
```bash
python -m pytest --cov=src --cov-report=term-missing | grep "0%"
```

### Phase 4: Thread Safety Failures

**Problem:** Deadlocks in concurrent operations

**Solution:** Add logging, use thread-safe primitives
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Add extensive logging around locks
```

### Phase 5: Low Production Readiness

**Problem:** Score below 7.5/10

**Solution:** Focus on highest-impact improvements first
1. Fix critical dependency issues
2. Address memory leaks
3. Remove SPOFs
4. Document thread constraints

### Phase 6: Git Push Fails

**Problem:** Pre-commit hooks fail or conflicts

**Solution:** Resolve conflicts, fix hook issues
```bash
git pull --rebase origin main
# Resolve conflicts
git add .
git rebase --continue
git push origin main
```

## Workflow Customization

### Skip Phases

If certain phases are not applicable:

```bash
# Skip Phase 4 (Thread Safety) if single-threaded deployment
# Execute Phases 1, 2, 3, 5, 6 only
```

### Parallel Execution

Run independent phases concurrently:

```bash
# Terminal 1: Phase 1 (Code Quality)
# Terminal 2: Phase 3 (Test Debugging)
# Merge results in Phase 6
```

### Incremental Execution

Execute workflow across multiple sessions:

1. **Session 1:** Phases 1-2 (Code quality fixes)
2. **Session 2:** Phase 3 (Test debugging)
3. **Session 3:** Phases 4-6 (Production validation, reporting)

## Integration with Claude Code

### Automatic Invocation

Claude Code suggests this workflow when:
- Multiple linting errors detected
- Test failures observed
- Production deployment mentioned
- `/debug-with-mcp` command used

### Session Continuity

Workflow state preserved in `.claude/session_continuity.md` for cross-session debugging.

## References

- **Code Quality Standards:** `.claude/testing_standards.md`
- **Production Readiness:** `docs/production_readiness_framework.md`
- **Testing Guide:** `docs/TESTING.md`
- **Project Conventions:** `CLAUDE.md`

---

**Version:** 1.0.0
**Last Updated:** 2025-10-10
**Status:** ✅ Production Ready
