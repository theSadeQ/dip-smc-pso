#!/bin/bash
# ==============================================================================
# Phase 2 Rollback Helper Script
# ==============================================================================
# Purpose: Emergency rollback for Phase 2 refactoring (Tasks 1-3)
# Usage: bash .ai_workspace/dev_tools/audit/phase2/rollback_helper.sh [options]
#
# Capabilities:
#   - Full rollback to pre-Phase-2 state
#   - Task-specific rollback (rollback only Task 1, 2, or 3)
#   - Incremental rollback (undo last N commits)
#   - Automated backup verification
#   - Safe rollback with confirmation prompts
#
# Exit Codes:
#   0 - Rollback successful
#   1 - Rollback failed or aborted
# ==============================================================================

set -e  # Exit on error (will be disabled for controlled error handling)

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_BRANCH_PREFIX="phase2-backup-"
START_TAG_PREFIX="phase2-start-"
ARTIFACTS_DIR=".artifacts/audit_cleanup"
ROLLBACK_LOG="${ARTIFACTS_DIR}/rollback_log.txt"

# Initialize rollback log
mkdir -p "$ARTIFACTS_DIR"
echo "=== Phase 2 Rollback Log ===" > "$ROLLBACK_LOG"
echo "Timestamp: $(date)" >> "$ROLLBACK_LOG"
echo "" >> "$ROLLBACK_LOG"

# ==============================================================================
# Helper Functions
# ==============================================================================

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║              PHASE 2 ROLLBACK HELPER                       ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
    echo "[ERROR] $1" >> "$ROLLBACK_LOG"
}

print_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
    echo "[SUCCESS] $1" >> "$ROLLBACK_LOG"
}

print_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
    echo "[WARNING] $1" >> "$ROLLBACK_LOG"
}

print_info() {
    echo -e "${BLUE}[INFO] $1${NC}"
    echo "[INFO] $1" >> "$ROLLBACK_LOG"
}

confirm_action() {
    local prompt="$1"
    local default="${2:-n}"  # Default to 'n' (no) for safety

    echo -e "${YELLOW}${prompt} [y/N]${NC}"
    read -r response

    response=${response:-$default}
    if [[ "$response" =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

check_git_status() {
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "Working directory has uncommitted changes"
        echo ""
        git status --short
        echo ""

        if ! confirm_action "Continue rollback anyway? (uncommitted changes will be LOST)"; then
            print_error "Rollback aborted by user"
            exit 1
        fi
    fi
}

find_backup_branch() {
    # Find most recent backup branch
    LATEST_BACKUP=$(git branch --list "${BACKUP_BRANCH_PREFIX}*" | sort -r | head -1 | sed 's/^[* ]*//')

    if [ -z "$LATEST_BACKUP" ]; then
        print_error "No backup branch found (expected: ${BACKUP_BRANCH_PREFIX}YYYYMMDD)"
        print_info "Backup branches should be created by pre-flight check"
        return 1
    fi

    echo "$LATEST_BACKUP"
    return 0
}

find_start_tag() {
    # Find most recent start tag
    LATEST_TAG=$(git tag --list "${START_TAG_PREFIX}*" | sort -r | head -1)

    if [ -z "$LATEST_TAG" ]; then
        print_error "No start tag found (expected: ${START_TAG_PREFIX}YYYYMMDD_HHMMSS)"
        print_info "Start tags should be created by pre-flight check"
        return 1
    fi

    echo "$LATEST_TAG"
    return 0
}

# ==============================================================================
# Rollback Strategies
# ==============================================================================

rollback_full() {
    print_header
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║           FULL ROLLBACK TO PRE-PHASE-2 STATE              ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    print_info "This will rollback ALL Phase 2 changes (Tasks 1, 2, and 3)"
    echo ""

    # Find start tag
    START_TAG=$(find_start_tag)
    if [ $? -ne 0 ]; then
        print_error "Cannot proceed without start tag"
        return 1
    fi

    print_info "Found start tag: $START_TAG"

    # Show what will be lost
    echo ""
    print_info "Commits that will be rolled back:"
    git log --oneline "$START_TAG"..HEAD | head -20
    COMMIT_COUNT=$(git log --oneline "$START_TAG"..HEAD | wc -l)
    echo ""
    print_warning "Total commits to rollback: $COMMIT_COUNT"
    echo ""

    # Confirmation
    if ! confirm_action "⚠️  DANGER: Proceed with full rollback? This CANNOT be undone easily!"; then
        print_info "Rollback aborted by user"
        return 1
    fi

    # Check git status
    check_git_status

    # Perform rollback
    print_info "Rolling back to $START_TAG..."
    if git reset --hard "$START_TAG"; then
        print_success "Full rollback completed"
        print_success "Repository restored to pre-Phase-2 state"
        echo ""
        print_info "Current commit: $(git log -1 --oneline)"
        echo ""
        print_info "Rollback log: $ROLLBACK_LOG"
        return 0
    else
        print_error "Rollback failed"
        return 1
    fi
}

rollback_task() {
    local task_number="$1"

    print_header
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║              TASK $task_number ROLLBACK                              ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Find commits related to this task
    local task_grep_pattern=""
    case "$task_number" in
        1)
            task_grep_pattern="optimizer\|Task 1\|Phase 2.*1"
            print_info "Searching for Task 1 (optimizer deprecation) commits..."
            ;;
        2)
            task_grep_pattern="factory\|Task 2\|Phase 2.*2"
            print_info "Searching for Task 2 (factory refactoring) commits..."
            ;;
        3)
            task_grep_pattern="CLAUDE.*config\|Task 3\|Phase 2.*3"
            print_info "Searching for Task 3 (CLAUDE.md update) commits..."
            ;;
        *)
            print_error "Invalid task number: $task_number (must be 1, 2, or 3)"
            return 1
            ;;
    esac

    # Find relevant commits
    local relevant_commits=$(git log --oneline --grep="$task_grep_pattern" -i --all | head -10)

    if [ -z "$relevant_commits" ]; then
        print_warning "No commits found for Task $task_number"
        print_info "Task may not have been started or commits don't match pattern"
        return 1
    fi

    echo ""
    print_info "Found Task $task_number commits:"
    echo "$relevant_commits"
    echo ""

    # Get first commit hash
    local first_commit=$(echo "$relevant_commits" | tail -1 | awk '{print $1}')

    print_warning "This will revert commits related to Task $task_number"
    echo ""

    if ! confirm_action "Proceed with Task $task_number rollback?"; then
        print_info "Rollback aborted by user"
        return 1
    fi

    check_git_status

    # Revert commits (in reverse order)
    print_info "Reverting Task $task_number commits..."
    while IFS= read -r line; do
        local commit_hash=$(echo "$line" | awk '{print $1}')
        local commit_msg=$(echo "$line" | cut -d' ' -f2-)

        print_info "Reverting: $commit_msg"
        if git revert --no-edit "$commit_hash"; then
            print_success "Reverted: $commit_hash"
        else
            print_error "Failed to revert: $commit_hash"
            print_warning "You may need to resolve conflicts manually"
            return 1
        fi
    done <<< "$relevant_commits"

    print_success "Task $task_number rollback completed"
    echo ""
    print_info "Rollback log: $ROLLBACK_LOG"
    return 0
}

rollback_incremental() {
    local num_commits="$1"

    print_header
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║         INCREMENTAL ROLLBACK (Last $num_commits commits)              ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    print_info "This will rollback the last $num_commits commit(s)"
    echo ""

    # Show commits to be rolled back
    print_info "Commits to rollback:"
    git log --oneline -n "$num_commits"
    echo ""

    if ! confirm_action "Proceed with incremental rollback of last $num_commits commit(s)?"; then
        print_info "Rollback aborted by user"
        return 1
    fi

    check_git_status

    # Perform rollback
    print_info "Rolling back last $num_commits commit(s)..."
    if git reset --hard HEAD~"$num_commits"; then
        print_success "Incremental rollback completed"
        echo ""
        print_info "Current commit: $(git log -1 --oneline)"
        echo ""
        print_info "Rollback log: $ROLLBACK_LOG"
        return 0
    else
        print_error "Rollback failed"
        return 1
    fi
}

list_recovery_points() {
    print_header
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║              AVAILABLE RECOVERY POINTS                     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # List backup branches
    print_info "Backup Branches:"
    local backup_branches=$(git branch --list "${BACKUP_BRANCH_PREFIX}*")
    if [ -z "$backup_branches" ]; then
        echo "  (none found)"
    else
        echo "$backup_branches" | sed 's/^/  /'
    fi
    echo ""

    # List start tags
    print_info "Start Tags:"
    local start_tags=$(git tag --list "${START_TAG_PREFIX}*" | sort -r)
    if [ -z "$start_tags" ]; then
        echo "  (none found)"
    else
        echo "$start_tags" | sed 's/^/  /'
    fi
    echo ""

    # Show recent commits
    print_info "Recent Commits (last 10):"
    git log --oneline -n 10 | sed 's/^/  /'
    echo ""

    print_info "Use these recovery points with: git reset --hard <tag-or-branch>"
}

# ==============================================================================
# Main Menu
# ==============================================================================

show_usage() {
    cat << EOF
Usage: bash rollback_helper.sh [OPTION]

Rollback Phase 2 refactoring changes with various strategies.

Options:
  --full              Full rollback to pre-Phase-2 state (uses start tag)
  --task N            Rollback specific task (N=1,2,3)
  --incremental N     Rollback last N commits
  --list              List available recovery points
  --help              Show this help message

Examples:
  # Full rollback to pre-Phase-2
  bash rollback_helper.sh --full

  # Rollback only Task 2 (factory refactoring)
  bash rollback_helper.sh --task 2

  # Rollback last 3 commits
  bash rollback_helper.sh --incremental 3

  # List all recovery points
  bash rollback_helper.sh --list

Safety Features:
  - Confirmation prompts before destructive actions
  - Git status check (warns about uncommitted changes)
  - Detailed logging to $ROLLBACK_LOG
  - Recovery point validation

EOF
}

# ==============================================================================
# Main Script
# ==============================================================================

# Parse arguments
case "${1:-}" in
    --full)
        rollback_full
        exit $?
        ;;
    --task)
        if [ -z "${2:-}" ]; then
            print_error "Task number required (1, 2, or 3)"
            show_usage
            exit 1
        fi
        rollback_task "$2"
        exit $?
        ;;
    --incremental)
        if [ -z "${2:-}" ]; then
            print_error "Number of commits required"
            show_usage
            exit 1
        fi
        if ! [[ "$2" =~ ^[0-9]+$ ]]; then
            print_error "Number of commits must be a positive integer"
            exit 1
        fi
        rollback_incremental "$2"
        exit $?
        ;;
    --list)
        list_recovery_points
        exit 0
        ;;
    --help)
        show_usage
        exit 0
        ;;
    "")
        # No arguments - show interactive menu
        print_header
        echo "Select rollback strategy:"
        echo ""
        echo "  1) Full rollback to pre-Phase-2 state"
        echo "  2) Rollback Task 1 (optimizer deprecation)"
        echo "  3) Rollback Task 2 (factory refactoring)"
        echo "  4) Rollback Task 3 (CLAUDE.md update)"
        echo "  5) Incremental rollback (last N commits)"
        echo "  6) List recovery points"
        echo "  7) Exit"
        echo ""
        read -p "Choice [1-7]: " choice

        case "$choice" in
            1) rollback_full ;;
            2) rollback_task 1 ;;
            3) rollback_task 2 ;;
            4) rollback_task 3 ;;
            5)
                read -p "Number of commits to rollback: " num_commits
                rollback_incremental "$num_commits"
                ;;
            6) list_recovery_points ;;
            7) echo "Exiting..."; exit 0 ;;
            *) print_error "Invalid choice"; exit 1 ;;
        esac
        exit $?
        ;;
    *)
        print_error "Unknown option: $1"
        show_usage
        exit 1
        ;;
esac
