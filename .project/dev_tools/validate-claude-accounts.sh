#!/bin/bash
# ============================================================================
# validate-claude-accounts.sh
# Safety Validation for Claude Code Multi-Account System (Linux Version)
# ============================================================================
#
# Purpose: Validate account isolation and detect safety violations
# Author: Claude Code Multi-Account System
# Created: 2025-10-22
#
# Usage:
#   ./validate-claude-accounts.sh
#   ./validate-claude-accounts.sh --verbose
#   ./validate-claude-accounts.sh --fix-issues
#
# ============================================================================

# Configuration
PRIMARY_CLAUDE_DIR="$HOME/.claude"
MAX_ACCOUNTS=5000
AUTH_FILES=(".credentials.json" "history.jsonl" ".claude.json" "settings.json")

# Safety thresholds
MAX_WARNINGS=0  # Zero tolerance for auth file symlinks

# Statistics
TOTAL_ACCOUNTS=0
AUTHENTICATED=0
NEEDS_LOGIN=0
SYMLINKS=0
ERRORS=0
WARNINGS=0

# Options
FIX_ISSUES=false
SHOW_DETAILS=false

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m'

# ============================================================================
# Helper Functions
# ============================================================================

write_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

write_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

write_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    ((WARNINGS++))
}

write_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    ((ERRORS++))
}

write_verbose() {
    if [ "$SHOW_DETAILS" = true ]; then
        echo -e "  ${GRAY}[DEBUG]${NC} $1"
    fi
}

test_auth_file_symlinks() {
    local account_dir="$1"
    local account_num="$2"
    local violations=0

    for file in "${AUTH_FILES[@]}"; do
        local path="$account_dir/$file"
        if [ -L "$path" ]; then
            local target=$(readlink "$path")
            write_error "Account $account_num has symlink: $file -> $target"
            ((violations++))
            ((SYMLINKS++))
        elif [ -f "$path" ]; then
            write_verbose "Account $account_num $file is a real file (safe)"
        fi
    done

    if [ $violations -gt 0 ]; then
        return 1
    fi

    return 0
}

test_account_authentication() {
    local account_dir="$1"
    local cred_file="$account_dir/.credentials.json"

    [ -f "$cred_file" ] && return 0 || return 1
}

get_account_file_count() {
    local account_dir="$1"
    find "$account_dir" -maxdepth 1 -type f 2>/dev/null | wc -l
}

test_directory_structure() {
    local account_dir="$1"
    local required_dirs=("ide" "projects" "session-env" "shell-snapshots" "statsig" "todos" "debug" "downloads")
    local missing_count=0

    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$account_dir/$dir" ]; then
            ((missing_count++))
        fi
    done

    if [ $missing_count -eq 0 ]; then
        return 0  # All directories present
    else
        return $missing_count  # Return count of missing directories
    fi
}

remove_auth_symlinks() {
    local account_dir="$1"
    local account_num="$2"

    write_info "Attempting to remove auth file symlinks from Account $account_num..."

    local removed=0
    for file in "${AUTH_FILES[@]}"; do
        local path="$account_dir/$file"
        if [ -L "$path" ]; then
            if rm "$path"; then
                write_success "Removed symlink: $file"
                ((removed++))
            else
                write_error "Failed to remove symlink $file"
            fi
        fi
    done

    if [ $removed -gt 0 ]; then
        write_success "Removed $removed symlink(s) from Account $account_num"
        return 0
    fi

    return 1
}

# ============================================================================
# Parse Arguments
# ============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --fix-issues)
            FIX_ISSUES=true
            shift
            ;;
        --verbose)
            SHOW_DETAILS=true
            shift
            ;;
        --help|-h)
            echo "Claude Code Account Safety Validator (Linux)"
            echo ""
            echo "Usage:"
            echo "  $0                  Run validation"
            echo "  $0 --verbose        Show detailed debug output"
            echo "  $0 --fix-issues     Automatically remove symlinks"
            echo "  $0 --help           Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# ============================================================================
# Main Validation Logic
# ============================================================================

echo ""
echo -e "${CYAN}======================================${NC}"
echo -e "${CYAN} Claude Code Account Safety Validator${NC}"
echo -e "${CYAN}======================================${NC}"
echo ""

# 1. Check primary directory
write_info "Checking primary .claude directory..."
if [ ! -d "$PRIMARY_CLAUDE_DIR" ]; then
    write_warning "Primary .claude directory not found at: $PRIMARY_CLAUDE_DIR"
    write_info "This is okay if Claude Code hasn't been used yet."
else
    primary_file_count=$(get_account_file_count "$PRIMARY_CLAUDE_DIR")
    write_success "Primary .claude exists ($primary_file_count files)"
fi

# 2. Check current CLAUDE_CONFIG_DIR
write_info "Checking current environment..."
if [ -n "$CLAUDE_CONFIG_DIR" ]; then
    write_info "CLAUDE_CONFIG_DIR is set: $CLAUDE_CONFIG_DIR"

    # Extract account number
    if [[ "$CLAUDE_CONFIG_DIR" =~ \.claude([0-9]+)$ ]]; then
        current_account="${BASH_REMATCH[1]}"
        write_info "Currently using Account $current_account"
    fi
else
    write_info "CLAUDE_CONFIG_DIR not set (using primary)"
fi

# 3. Scan all accounts
write_info "Scanning accounts 1-$MAX_ACCOUNTS..."
echo ""

accounts_found=0

for i in $(seq 1 $MAX_ACCOUNTS); do
    account_dir="$HOME/.claude$i"

    if [ -d "$account_dir" ]; then
        ((TOTAL_ACCOUNTS++))
        ((accounts_found++))

        echo -ne "${WHITE}Account $i:${NC}"

        # Check authentication
        if test_account_authentication "$account_dir"; then
            ((AUTHENTICATED++))
            echo -ne " ${GREEN}[✓ Auth]${NC}"
        else
            ((NEEDS_LOGIN++))
            echo -ne " ${YELLOW}[! Login]${NC}"
        fi

        # Check directory structure
        test_directory_structure "$account_dir"
        local missing_dirs=$?
        if [ $missing_dirs -eq 0 ]; then
            echo -ne " ${GREEN}[✓ Dirs]${NC}"
        else
            echo -ne " ${RED}[✗ $missing_dirs missing]${NC}"
        fi

        # Check file count
        file_count=$(get_account_file_count "$account_dir")
        echo -n " ($file_count files)"

        # Safety check: no auth file symlinks
        if test_auth_file_symlinks "$account_dir" "$i"; then
            echo -e " ${GREEN}[✓]${NC}"
        else
            echo -e " ${RED}[UNSAFE]${NC}"

            if [ "$FIX_ISSUES" = true ]; then
                remove_auth_symlinks "$account_dir" "$i"
            fi
        fi
    fi
done

# 4. Summary
echo ""
echo -e "${CYAN}======================================${NC}"
echo -e "${CYAN} Validation Summary${NC}"
echo -e "${CYAN}======================================${NC}"
echo ""

echo -e "${WHITE}Total accounts found: $TOTAL_ACCOUNTS${NC}"
echo -e "  ${GREEN}Authenticated:      $AUTHENTICATED${NC}"
echo -e "  ${YELLOW}Needs login:        $NEEDS_LOGIN${NC}"
echo ""
echo -e "${WHITE}Safety checks:${NC}"
if [ $SYMLINKS -eq 0 ]; then
    echo -e "  ${GREEN}Auth symlinks:      $SYMLINKS${NC}"
else
    echo -e "  ${RED}Auth symlinks:      $SYMLINKS${NC}"
fi
if [ $ERRORS -eq 0 ]; then
    echo -e "  ${GREEN}Errors:             $ERRORS${NC}"
else
    echo -e "  ${RED}Errors:             $ERRORS${NC}"
fi
if [ $WARNINGS -eq 0 ]; then
    echo -e "  ${GREEN}Warnings:           $WARNINGS${NC}"
else
    echo -e "  ${YELLOW}Warnings:           $WARNINGS${NC}"
fi
echo ""

# 5. Final verdict
if [ $ERRORS -eq 0 ] && [ $WARNINGS -le $MAX_WARNINGS ]; then
    write_success "All safety checks passed!"
    echo ""
    exit 0
elif [ $SYMLINKS -gt 0 ]; then
    write_error "CRITICAL: Auth file symlinks detected!"
    write_warning "This violates the safety protocol."
    write_info "Run with --fix-issues to automatically remove symlinks."
    echo ""
    exit 1
else
    write_warning "Validation completed with warnings."
    write_info "Review the output above for details."
    echo ""
    exit 0
fi
