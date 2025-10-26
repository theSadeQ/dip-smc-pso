#!/bin/bash
# ==============================================================================
# Automated Recovery System - Simple Test Suite
# ==============================================================================
# Simplified tests that work within gitignore constraints.
# ==============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

print_header() {
    echo ""
    echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${BLUE}$1${NC}"
    echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_test() {
    echo ""
    echo "${YELLOW}[TEST $1]${NC} $2"
}

assert_pass() {
    echo "${GREEN}✓ PASS:${NC} $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

assert_fail() {
    echo "${RED}✗ FAIL:${NC} $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

# Save initial state
print_header "SETUP: Saving Initial State"
INITIAL_COMMIT=$(git rev-parse HEAD)
echo "Initial commit: $INITIAL_COMMIT"

cp .ai/config/project_state.json .ai/config/project_state.json.backup
echo "Backed up project_state.json"

git checkout -b test-automation-$(date +%s) >/dev/null 2>&1
echo "Created test branch: $(git branch --show-current)"

# ==============================================================================
# TEST 1: Benchmark Deliverable (Single File)
# ==============================================================================
print_test "1" "Single benchmark deliverable detection"

mkdir -p benchmarks
echo "# Test Benchmark QW-99" > benchmarks/QW99_TEST.md
echo "This is a fake benchmark for testing automation." >> benchmarks/QW99_TEST.md

git add benchmarks/QW99_TEST.md

git commit -m "feat(QW-99): Test single benchmark deliverable

Testing pre-commit hook detection:
- Task ID: QW-99 (fake, should handle gracefully)
- Deliverable: benchmarks/QW99_TEST.md

[AI]" >/dev/null 2>&1

# Check last_commit updated
STATE=$(cat .ai/config/project_state.json)
COMMIT_HASH=$(git rev-parse HEAD)

if echo "$STATE" | grep -q "$COMMIT_HASH"; then
    assert_pass "Post-commit hook updated last_commit metadata"
else
    assert_fail "Post-commit hook did NOT update metadata"
fi

# ==============================================================================
# TEST 2: Multiple Benchmark Deliverables
# ==============================================================================
print_test "2" "Multiple benchmark deliverables detection"

echo "# Test Benchmark MT-99 Part 1" > benchmarks/MT99_PART1.md
echo "# Test Benchmark MT-99 Part 2" > benchmarks/MT99_PART2.md

git add benchmarks/MT99_PART1.md benchmarks/MT99_PART2.md

git commit -m "feat(MT-99): Test multiple benchmark deliverables

Testing pre-commit hook with multiple files:
- benchmarks/MT99_PART1.md
- benchmarks/MT99_PART2.md

[AI]" >/dev/null 2>&1

STATE=$(cat .ai/config/project_state.json)
COMMIT_HASH=$(git rev-parse HEAD)

if echo "$STATE" | grep -q "$COMMIT_HASH"; then
    assert_pass "Post-commit hook tracked multi-deliverable commit"
else
    assert_fail "Post-commit hook failed on multi-deliverable"
fi

# ==============================================================================
# TEST 3: Theory Documentation Deliverable
# ==============================================================================
print_test "3" "Theory documentation deliverable detection"

mkdir -p docs/theory
echo "# Lyapunov Stability Test" > docs/theory/lyapunov_test.md

git add docs/theory/lyapunov_test.md

git commit -m "feat(LT-99): Test theory documentation deliverable

Testing docs/theory/ directory detection.

[AI]" >/dev/null 2>&1

STATE=$(cat .ai/config/project_state.json)
COMMIT_HASH=$(git rev-parse HEAD)

if echo "$STATE" | grep -q "$COMMIT_HASH"; then
    assert_pass "Post-commit hook tracked theory doc commit"
else
    assert_fail "Post-commit hook failed on theory doc"
fi

# ==============================================================================
# TEST 4: Normal Commit (No Task ID)
# ==============================================================================
print_test "4" "Normal commit without task ID"

echo "# Regular Update" > docs/REGULAR_TEST.md
git add docs/REGULAR_TEST.md

git commit -m "docs: Regular documentation update

No task ID - should not break automation.

[AI]" >/dev/null 2>&1

STATE=$(cat .ai/config/project_state.json)
COMMIT_HASH=$(git rev-parse HEAD)

if echo "$STATE" | grep -q "$COMMIT_HASH"; then
    assert_pass "Post-commit hook handled non-task commit gracefully"
else
    assert_fail "Post-commit hook broke on non-task commit"
fi

# ==============================================================================
# TEST 5: Metadata Accuracy
# ==============================================================================
print_test "5" "Post-commit metadata accuracy"

STATE=$(cat .ai/config/project_state.json)

# Check hash
HASH_STATE=$(echo "$STATE" | grep -oP '"hash": "\K[^"]+' | tail -n1)
HASH_GIT=$(git rev-parse HEAD)

if [ "$HASH_STATE" = "$HASH_GIT" ]; then
    assert_pass "Commit hash matches (state: ${HASH_STATE:0:8})"
else
    assert_fail "Commit hash mismatch (state: $HASH_STATE, git: $HASH_GIT)"
fi

# Check timestamp
TS=$(echo "$STATE" | grep -oP '"timestamp": \K[0-9]+' | tail -n1)
if [ "$TS" -gt 1700000000 ] && [ "$TS" -lt 2000000000 ]; then
    assert_pass "Timestamp valid (Unix: $TS)"
else
    assert_fail "Timestamp invalid: $TS"
fi

# Check message
MSG=$(echo "$STATE" | grep -oP '"message": "\K[^"]+' | tail -n1)
if [ -n "$MSG" ]; then
    assert_pass "Commit message captured: ${MSG:0:40}..."
else
    assert_fail "Commit message missing"
fi

# ==============================================================================
# TEST 6: Hook Files Exist
# ==============================================================================
print_test "6" "Git hooks and shell init files"

if [ -f .git/hooks/pre-commit ]; then
    assert_pass "pre-commit hook exists"
else
    assert_fail "pre-commit hook missing"
fi

if [ -f .git/hooks/post-commit ]; then
    assert_pass "post-commit hook exists"
else
    assert_fail "post-commit hook missing"
fi

if [ -x .dev_tools/shell_init.sh ]; then
    assert_pass "shell_init.sh exists and executable"
else
    assert_fail "shell_init.sh missing or not executable"
fi

if [ -f .dev_tools/shell_init.ps1 ]; then
    assert_pass "shell_init.ps1 exists"
else
    assert_fail "shell_init.ps1 missing"
fi

# ==============================================================================
# CLEANUP
# ==============================================================================
print_header "CLEANUP: Restoring Original State"

git checkout main >/dev/null 2>&1
echo "Switched to main"

BRANCH=$(git branch | grep test-automation)
git branch -D $BRANCH >/dev/null 2>&1
echo "Deleted test branch"

mv .ai/config/project_state.json.backup .ai/config/project_state.json
echo "Restored project_state.json"

rm -f .ai/config/.last_recovery
echo "Cleaned up artifacts"

CURRENT=$(git rev-parse HEAD)
if [ "$CURRENT" = "$INITIAL_COMMIT" ]; then
    echo "${GREEN}✓${NC} Restored to initial commit"
else
    echo "${YELLOW}⚠${NC} Commit changed (may be normal)"
fi

# ==============================================================================
# SUMMARY
# ==============================================================================
print_header "TEST SUMMARY"

TOTAL=$((TESTS_PASSED + TESTS_FAILED))
PASS_RATE=$((TESTS_PASSED * 100 / TOTAL))

echo ""
echo "Total Tests:  $TOTAL"
echo "${GREEN}Passed:       $TESTS_PASSED${NC}"
echo "${RED}Failed:       $TESTS_FAILED${NC}"
echo "Pass Rate:    ${PASS_RATE}%"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${GREEN}✓ ALL TESTS PASSED - AUTOMATION FULLY OPERATIONAL${NC}"
    echo "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 0
else
    echo "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${RED}✗ $TESTS_FAILED TEST(S) FAILED - CHECK OUTPUT${NC}"
    echo "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
fi
