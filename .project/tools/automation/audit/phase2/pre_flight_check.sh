#!/bin/bash
# ==============================================================================
# Phase 2 Pre-Flight Check Automation Script
# ==============================================================================
# Purpose: Automated validation and safety net setup before Phase 2 refactoring
# Execution Time: 10-15 minutes
# Outputs:
#   - .artifacts/audit_cleanup/phase2_preflight_report.txt
#   - .artifacts/audit_cleanup/phase2_baseline.json
#   - Git backups (branch + tag)
#
# Usage: bash .project/dev_tools/audit/phase2/pre_flight_check.sh
# ==============================================================================

set -e  # Exit on error (disabled for controlled error handling)
set +e  # Re-enable to handle errors gracefully

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNED=0

# Create artifacts directory
mkdir -p .artifacts/audit_cleanup

# Initialize report
echo "╔════════════════════════════════════════════════════════════╗" > .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "║        PHASE 2 PRE-FLIGHT HEALTH CHECK DASHBOARD          ║" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "╚════════════════════════════════════════════════════════════╝" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "Generated: $(date)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "" >> .artifacts/audit_cleanup/phase2_preflight_report.txt

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        PHASE 2 PRE-FLIGHT HEALTH CHECK                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ==============================================================================
# CHECK 1: Phase 1 Completion Verification
# ==============================================================================
echo -e "${BLUE}[1/8] Checking Phase 1 completion...${NC}"

if [ -f .artifacts/audit_cleanup/phase1_validation.txt ]; then
    if grep -q "PHASE 1 COMPLETE" .artifacts/audit_cleanup/phase1_validation.txt 2>/dev/null; then
        echo -e "${GREEN}[✓] Phase 1 Completion: PASS${NC}"
        echo "[✓] Phase 1 Completion: PASS" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo -e "${YELLOW}[⚠] Phase 1 Completion: WARN (validation file unclear)${NC}"
        echo "[⚠] Phase 1 Completion: WARN (validation file unclear)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
        CHECKS_WARNED=$((CHECKS_WARNED + 1))
    fi
else
    echo -e "${RED}[✗] Phase 1 Completion: FAIL (not found)${NC}"
    echo "[✗] Phase 1 Completion: FAIL (not found)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "   → Run Phase 1 first (see PHASE_1_IMMEDIATE.md)"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
fi

# ==============================================================================
# CHECK 2: Git Working Tree State
# ==============================================================================
echo -e "${BLUE}[2/8] Checking git working tree...${NC}"

if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}[✗] Git Working Tree: FAIL (dirty)${NC}"
    echo "[✗] Git Working Tree: FAIL (dirty)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "   → Uncommitted changes detected:"
    git status --short | head -5
    echo "   → Commit or stash changes before proceeding"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
else
    echo -e "${GREEN}[✓] Git Working Tree: PASS (clean)${NC}"
    echo "[✓] Git Working Tree: PASS (clean)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# Check branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}   ⚠ Not on main branch (currently on: $CURRENT_BRANCH)${NC}"
fi

# ==============================================================================
# CHECK 3: Test Suite Baseline
# ==============================================================================
echo -e "${BLUE}[3/8] Running test suite to establish baseline...${NC}"
echo "   (This may take 30-60 seconds)"

python -m pytest tests/ -v --tb=short > .artifacts/audit_cleanup/phase2_test_output.txt 2>&1
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    PASSING_TESTS=$(grep -c "PASSED" .artifacts/audit_cleanup/phase2_test_output.txt || echo "0")
    echo -e "${GREEN}[✓] Test Suite: PASS ($PASSING_TESTS tests)${NC}"
    echo "[✓] Test Suite: PASS ($PASSING_TESTS tests)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "$PASSING_TESTS" > .artifacts/audit_cleanup/phase2_test_count_baseline.txt
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${RED}[✗] Test Suite: FAIL${NC}"
    echo "[✗] Test Suite: FAIL" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "   → Failed tests:"
    grep "FAILED" .artifacts/audit_cleanup/phase2_test_output.txt | head -5
    echo "   → Fix tests before proceeding"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
fi

# ==============================================================================
# CHECK 4: Import Dependency Analysis
# ==============================================================================
echo -e "${BLUE}[4/8] Analyzing import dependencies...${NC}"

echo "=== Import Dependency Analysis ===" > .artifacts/audit_cleanup/phase2_import_baseline.txt
echo "Generated: $(date)" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
echo "" >> .artifacts/audit_cleanup/phase2_import_baseline.txt

# Find optimizer imports
echo "=== src.optimizer Imports ===" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
grep -rn "src.optimizer" src/ tests/ 2>/dev/null >> .artifacts/audit_cleanup/phase2_import_baseline.txt || echo "No optimizer imports found" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
OPTIMIZER_IMPORT_COUNT=$(grep -rn "src.optimizer" src/ tests/ 2>/dev/null | wc -l)

# Find factory imports
echo "" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
echo "=== src.controllers.factory Imports ===" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
grep -rn "src.controllers.factory" src/ tests/ 2>/dev/null >> .artifacts/audit_cleanup/phase2_import_baseline.txt || echo "No factory imports found" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
FACTORY_IMPORT_COUNT=$(grep -rn "src.controllers.factory" src/ tests/ 2>/dev/null | wc -l)

# Summary
echo "" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
echo "=== Summary ===" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
echo "Optimizer imports to review: $OPTIMIZER_IMPORT_COUNT" >> .artifacts/audit_cleanup/phase2_import_baseline.txt
echo "Factory imports to review: $FACTORY_IMPORT_COUNT" >> .artifacts/audit_cleanup/phase2_import_baseline.txt

TOTAL_IMPORTS=$((OPTIMIZER_IMPORT_COUNT + FACTORY_IMPORT_COUNT))
if [ "$TOTAL_IMPORTS" -gt 0 ]; then
    echo -e "${GREEN}[✓] Import Baseline: PASS ($TOTAL_IMPORTS imports tracked)${NC}"
    echo "[✓] Import Baseline: PASS ($TOTAL_IMPORTS imports tracked)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${YELLOW}[⚠] Import Baseline: WARN (no target imports found)${NC}"
    echo "[⚠] Import Baseline: WARN (no target imports found)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_WARNED=$((CHECKS_WARNED + 1))
fi

# ==============================================================================
# CHECK 5: Git Safety Net
# ==============================================================================
echo -e "${BLUE}[5/8] Creating git safety net...${NC}"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATESTAMP=$(date +%Y%m%d)

# Create backup branch
git branch "phase2-backup-${DATESTAMP}" 2>/dev/null
BRANCH_EXIT=$?

# Create start tag
git tag "phase2-start-${TIMESTAMP}" 2>/dev/null
TAG_EXIT=$?

# Verify
LATEST_TAG=$(git tag -l "phase2-start-*" | tail -1)
if [ -n "$LATEST_TAG" ]; then
    echo -e "${GREEN}[✓] Git Safety Net: PASS${NC}"
    echo "[✓] Git Safety Net: PASS" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "   → Backup branch: phase2-backup-${DATESTAMP}"
    echo "   → Start tag: $LATEST_TAG"
    echo "   → Rollback command: git reset --hard $LATEST_TAG"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${RED}[✗] Git Safety Net: FAIL${NC}"
    echo "[✗] Git Safety Net: FAIL" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
fi

# ==============================================================================
# CHECK 6: Python Environment Validation
# ==============================================================================
echo -e "${BLUE}[6/8] Validating Python environment...${NC}"

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

PYTHON_OK=1
if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
    echo "   ✓ Python version: $PYTHON_VERSION"
else
    echo -e "${RED}   ✗ Python version $PYTHON_VERSION < 3.9${NC}"
    PYTHON_OK=0
fi

# Verify src package
if python -c "import src" 2>/dev/null; then
    echo "   ✓ src package resolves"
else
    echo -e "${RED}   ✗ Cannot import src package${NC}"
    PYTHON_OK=0
fi

# Check critical dependencies
MISSING_DEPS=""
for pkg in pytest numpy scipy pydantic; do
    if python -c "import $pkg" 2>/dev/null; then
        VERSION=$(python -c "import $pkg; print($pkg.__version__)")
        echo "   ✓ $pkg: $VERSION"
    else
        echo -e "${RED}   ✗ Missing: $pkg${NC}"
        MISSING_DEPS="$MISSING_DEPS $pkg"
        PYTHON_OK=0
    fi
done

if [ "$PYTHON_OK" -eq 1 ]; then
    echo -e "${GREEN}[✓] Python Environment: PASS${NC}"
    echo "[✓] Python Environment: PASS" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${RED}[✗] Python Environment: FAIL${NC}"
    echo "[✗] Python Environment: FAIL" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    if [ -n "$MISSING_DEPS" ]; then
        echo "   → Install missing: pip install$MISSING_DEPS"
    fi
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
fi

# ==============================================================================
# CHECK 7: Disk Space & Performance
# ==============================================================================
echo -e "${BLUE}[7/8] Checking disk space and performance...${NC}"

# Check disk space
AVAILABLE_SPACE=$(df -h . | awk 'NR==2 {print $4}')
AVAILABLE_KB=$(df -k . | awk 'NR==2 {print $4}')
echo "   • Available disk space: $AVAILABLE_SPACE"

if [ "$AVAILABLE_KB" -lt 1048576 ]; then
    echo -e "${YELLOW}   ⚠ Low disk space (<1GB)${NC}"
    CHECKS_WARNED=$((CHECKS_WARNED + 1))
fi

# Check .artifacts size
if [ -d .artifacts/ ]; then
    ARTIFACTS_SIZE=$(du -sh .artifacts/ 2>/dev/null | awk '{print $1}')
    echo "   • Artifacts directory: $ARTIFACTS_SIZE"
fi

# Test execution time baseline
echo "   • Measuring test suite performance..."
START_TIME=$(date +%s)
python -m pytest tests/ -q > /dev/null 2>&1
END_TIME=$(date +%s)
TEST_DURATION=$((END_TIME - START_TIME))
echo "   • Test suite duration: ${TEST_DURATION}s"
echo "$TEST_DURATION" > .artifacts/audit_cleanup/phase2_test_duration_baseline.txt

if [ "$TEST_DURATION" -lt 60 ]; then
    echo -e "${GREEN}[✓] Disk Space & Performance: PASS${NC}"
    echo "[✓] Disk Space & Performance: PASS" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${YELLOW}[⚠] Performance: WARN (slow test suite: ${TEST_DURATION}s)${NC}"
    echo "[⚠] Disk Space & Performance: WARN (slow test suite)" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_WARNED=$((CHECKS_WARNED + 1))
fi

# ==============================================================================
# CHECK 8: Additional Safety Checks
# ==============================================================================
echo -e "${BLUE}[8/8] Running additional safety checks...${NC}"

SAFETY_OK=1

# Check for uncommitted large files
LARGE_FILES=$(find . -type f -size +10M 2>/dev/null | grep -v ".git" | head -5)
if [ -n "$LARGE_FILES" ]; then
    echo -e "${YELLOW}   ⚠ Large files detected (>10MB):${NC}"
    echo "$LARGE_FILES" | head -3
fi

# Check for Python syntax errors in src/
echo "   • Checking Python syntax in src/..."
SYNTAX_ERRORS=$(find src/ -name "*.py" -exec python -m py_compile {} \; 2>&1)
if [ -n "$SYNTAX_ERRORS" ]; then
    echo -e "${RED}   ✗ Python syntax errors detected${NC}"
    echo "$SYNTAX_ERRORS" | head -5
    SAFETY_OK=0
else
    echo "   ✓ No syntax errors in src/"
fi

if [ "$SAFETY_OK" -eq 1 ]; then
    echo -e "${GREEN}[✓] Additional Safety Checks: PASS${NC}"
    echo "[✓] Additional Safety Checks: PASS" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "${RED}[✗] Additional Safety Checks: FAIL${NC}"
    echo "[✗] Additional Safety Checks: FAIL" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
fi

# ==============================================================================
# SUMMARY
# ==============================================================================
echo ""
echo "────────────────────────────────────────────────────────────" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "SUMMARY" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "────────────────────────────────────────────────────────────" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "Checks Passed:  $CHECKS_PASSED" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "Checks Failed:  $CHECKS_FAILED" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "Checks Warned:  $CHECKS_WARNED" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
echo "" >> .artifacts/audit_cleanup/phase2_preflight_report.txt

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                      SUMMARY                               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Checks Passed: ${GREEN}$CHECKS_PASSED${NC}"
echo -e "  Checks Failed: ${RED}$CHECKS_FAILED${NC}"
echo -e "  Checks Warned: ${YELLOW}$CHECKS_WARNED${NC}"
echo ""

# Final verdict
if [ "$CHECKS_FAILED" -eq 0 ]; then
    echo "STATUS: ✓ READY TO PROCEED" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "Next Steps:" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "1. Review this report: .artifacts/audit_cleanup/phase2_preflight_report.txt" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "2. Proceed with Task 1: Deprecate src/optimizer/" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "3. See: .project/ai/planning/workspace_audit_2025_10/PHASE_2_THIS_WEEK.md" >> .artifacts/audit_cleanup/phase2_preflight_report.txt

    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  STATUS: ✓ READY TO PROCEED WITH PHASE 2                  ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Pre-flight report: .artifacts/audit_cleanup/phase2_preflight_report.txt"
    echo ""
    echo "Next Steps:"
    echo "  1. Review baseline files in .artifacts/audit_cleanup/"
    echo "  2. Proceed with Task 1: Deprecate src/optimizer/"
    echo "  3. Follow: .project/ai/planning/workspace_audit_2025_10/PHASE_2_THIS_WEEK.md"
    echo ""
    exit 0
else
    echo "STATUS: ✗ NOT READY - FIX FAILURES FIRST" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    echo "Failed Checks:" >> .artifacts/audit_cleanup/phase2_preflight_report.txt
    grep "✗" .artifacts/audit_cleanup/phase2_preflight_report.txt >> .artifacts/audit_cleanup/phase2_preflight_report.txt

    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  STATUS: ✗ NOT READY - FIX FAILURES FIRST                 ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Pre-flight report: .artifacts/audit_cleanup/phase2_preflight_report.txt"
    echo ""
    echo "Failed checks:"
    grep "\[✗\]" .artifacts/audit_cleanup/phase2_preflight_report.txt | sed 's/^/  /'
    echo ""
    echo "Fix failures and re-run this script."
    echo ""
    exit 1
fi
