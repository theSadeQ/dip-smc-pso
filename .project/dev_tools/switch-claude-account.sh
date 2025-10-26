#!/bin/bash
# ============================================================================
# switch-claude-account.sh
# Dynamic Account Switcher with Safety Protocol (Linux Version)
# ============================================================================
#
# Purpose: Safe multi-account switching for Claude Code with auth isolation
# Author: Claude Code Multi-Account System
# Created: 2025-10-22
#
# Features:
# - Isolated authentication per account
# - Session state tracking integration
# - Safety checks (no auth file sharing)
# - Auto-creates account directories
# - Validates account structure
#
# Usage:
#   ./switch-claude-account.sh 5
#   ./switch-claude-account.sh 1 --no-launch
#   ./switch-claude-account.sh --primary
#   ./switch-claude-account.sh --validate
#
# ============================================================================

# Configuration
PRIMARY_CLAUDE_DIR="$HOME/.claude"
SESSION_STATE_FILE="/media/sadeq/asus1/Projects/main/.ai/config/session_state.json"
MAX_ACCOUNTS=5000  # Support up to 5000 accounts

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

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
}

write_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

test_primary_directory() {
    if [ ! -d "$PRIMARY_CLAUDE_DIR" ]; then
        write_error "Primary .claude directory not found at: $PRIMARY_CLAUDE_DIR"
        write_info "This system requires a primary Claude Code installation."
        return 1
    fi
    write_success "Primary .claude directory exists"
    return 0
}

test_no_auth_symlinks() {
    local account_dir="$1"
    local auth_files=(".credentials.json" "history.jsonl" ".claude.json")
    local symlinks=()

    for file in "${auth_files[@]}"; do
        local path="$account_dir/$file"
        if [ -L "$path" ]; then
            symlinks+=("$file")
        fi
    done

    if [ ${#symlinks[@]} -gt 0 ]; then
        write_error "Auth file symlinks detected: ${symlinks[*]}"
        write_error "This violates safety protocol. Remove symlinks before continuing."
        return 1
    fi

    return 0
}

initialize_account_directory() {
    local acc_num="$1"
    local account_dir="$HOME/.claude$acc_num"
    local needs_init=false

    if [ ! -d "$account_dir" ]; then
        write_info "Creating account directory: $account_dir"
        mkdir -p "$account_dir"
        needs_init=true
        write_success "Account directory created"
    else
        write_info "Account directory exists: $account_dir"
        # Check if subdirectories exist
        if [ ! -d "$account_dir/ide" ] || [ ! -d "$account_dir/projects" ]; then
            needs_init=true
        fi
    fi

    # Initialize required subdirectories
    if [ "$needs_init" = true ]; then
        write_info "Initializing account directory structure..."

        # Required subdirectories for Claude Code
        local required_dirs=("ide" "projects" "session-env" "shell-snapshots" "statsig" "todos" "debug" "downloads")

        for dir in "${required_dirs[@]}"; do
            local target_dir="$account_dir/$dir"
            if [ ! -d "$target_dir" ]; then
                mkdir -p "$target_dir"

                # Set proper permissions (match primary .claude)
                if [ "$dir" = "projects" ] || [ "$dir" = "todos" ] || [ "$dir" = "debug" ]; then
                    chmod 700 "$target_dir"  # Private directories
                else
                    chmod 775 "$target_dir"  # Standard directories
                fi
            fi
        done

        write_success "Account structure initialized (${#required_dirs[@]} directories)"
    fi

    # Validate no auth symlinks
    if ! test_no_auth_symlinks "$account_dir"; then
        return 1
    fi

    echo "$account_dir"
    return 0
}

update_session_state() {
    local acc_num="$1"

    if [ ! -f "$SESSION_STATE_FILE" ]; then
        write_warning "Session state file not found: $SESSION_STATE_FILE"
        return
    fi

    # Update session state using jq if available
    if command -v jq &> /dev/null; then
        local account_name
        if [ "$acc_num" -eq 0 ]; then
            account_name="primary"
        else
            account_name="account_$acc_num"
        fi

        local timestamp=$(date -Iseconds)

        jq --arg account "$account_name" \
           --arg time "$timestamp" \
           '.account = $account | .last_updated = $time' \
           "$SESSION_STATE_FILE" > "$SESSION_STATE_FILE.tmp" && \
           mv "$SESSION_STATE_FILE.tmp" "$SESSION_STATE_FILE"

        write_success "Session state updated: $account_name"
    else
        write_warning "jq not installed, skipping session state update"
    fi
}

get_account_status() {
    local acc_num="$1"
    local account_dir="$HOME/.claude$acc_num"

    if [ ! -d "$account_dir" ]; then
        echo "EXISTS=false AUTHENTICATED=false FILE_COUNT=0 DIRS_INITIALIZED=false"
        return
    fi

    local cred_file="$account_dir/.credentials.json"
    local authenticated="false"
    [ -f "$cred_file" ] && authenticated="true"

    local file_count=$(find "$account_dir" -maxdepth 1 -type f 2>/dev/null | wc -l)

    # Check if directories are initialized
    local dirs_initialized="true"
    if [ ! -d "$account_dir/ide" ] || [ ! -d "$account_dir/projects" ]; then
        dirs_initialized="false"
    fi

    echo "EXISTS=true AUTHENTICATED=$authenticated FILE_COUNT=$file_count DIRS_INITIALIZED=$dirs_initialized"
}

get_current_account() {
    if [ -z "$CLAUDE_CONFIG_DIR" ]; then
        echo "primary"
        return
    fi

    # Extract account number from path like /home/user/.claude5
    if [[ "$CLAUDE_CONFIG_DIR" =~ \.claude([0-9]+)$ ]]; then
        echo "${BASH_REMATCH[1]}"
    else
        echo "unknown"
    fi
}

# ============================================================================
# Main Logic
# ============================================================================

# Parse arguments
NO_LAUNCH=false
PRIMARY=false
VALIDATE=false
ACCOUNT_NUM=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-launch)
            NO_LAUNCH=true
            shift
            ;;
        --primary)
            PRIMARY=true
            shift
            ;;
        --validate)
            VALIDATE=true
            shift
            ;;
        --help|-h)
            echo "Claude Code Multi-Account Switcher (Linux)"
            echo ""
            echo "Usage:"
            echo "  $0 <number>              Switch to account (1-$MAX_ACCOUNTS)"
            echo "  $0 <number> --no-launch  Switch without launching Claude"
            echo "  $0 --primary             Switch to primary .claude"
            echo "  $0 --validate            Validate all accounts"
            echo "  $0 --help                Show this help"
            echo ""
            echo "Examples:"
            echo "  $0 5                     # Switch to account 5 and launch"
            echo "  $0 42 --no-launch        # Switch to account 42 only"
            echo "  $0 --primary             # Return to primary account"
            exit 0
            ;;
        [0-9]*)
            ACCOUNT_NUM="$1"
            shift
            ;;
        *)
            write_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate mode
if [ "$VALIDATE" = true ]; then
    write_info "Running account validation..."

    # Show current account
    current_account=$(get_current_account)
    if [ "$current_account" = "primary" ]; then
        write_info "Currently active: ${CYAN}Primary .claude${NC}"
    else
        write_info "Currently active: ${CYAN}Account $current_account${NC}"
    fi
    echo ""

    if ! test_primary_directory; then
        exit 1
    fi

    write_info "Checking accounts 1-$MAX_ACCOUNTS..."

    results=()
    for i in $(seq 1 $MAX_ACCOUNTS); do
        if [ -d "$HOME/.claude$i" ]; then
            eval $(get_account_status $i)
            if [ "$AUTHENTICATED" = "true" ]; then
                auth_status="${GREEN}[✓] Authenticated${NC}"
            else
                auth_status="${YELLOW}[!] Needs login${NC}"
            fi

            # Directory structure status
            if [ "$DIRS_INITIALIZED" = "true" ]; then
                dir_status="${GREEN}[✓]${NC}"
            else
                dir_status="${RED}[✗]${NC}"
            fi

            results+=("Account $i: $auth_status | Dirs: $dir_status | Files: $FILE_COUNT")
        fi
    done

    if [ ${#results[@]} -eq 0 ]; then
        write_info "No account directories found. Run switcher to create accounts."
    else
        write_success "Found ${#results[@]} account(s):"
        for result in "${results[@]}"; do
            echo -e "  ${WHITE}$result${NC}"
        done
    fi

    exit 0
fi

# Primary mode
if [ "$PRIMARY" = true ]; then
    write_info "Switching to primary .claude directory..."

    if ! test_primary_directory; then
        exit 1
    fi

    # Clear CLAUDE_CONFIG_DIR
    if [ -n "$CLAUDE_CONFIG_DIR" ]; then
        unset CLAUDE_CONFIG_DIR
        write_success "Cleared CLAUDE_CONFIG_DIR"
    fi

    update_session_state 0

    write_success "Now using primary .claude directory"
    write_info "Location: $PRIMARY_CLAUDE_DIR"

    if [ "$NO_LAUNCH" = false ]; then
        write_info "Launching Claude Code..."
        claude --dangerously-skip-permissions
    fi

    exit 0
fi

# Account switching mode
if [ -z "$ACCOUNT_NUM" ]; then
    write_error "Missing required parameter: account number or --primary"
    write_info "Usage: $0 <number>"
    write_info "       $0 --primary"
    write_info "       $0 --validate"
    exit 1
fi

if [ "$ACCOUNT_NUM" -lt 1 ] || [ "$ACCOUNT_NUM" -gt $MAX_ACCOUNTS ]; then
    write_error "Account number must be between 1 and $MAX_ACCOUNTS"
    exit 1
fi

write_info "Switching to Claude Code Account $ACCOUNT_NUM..."

# Validate primary directory
if ! test_primary_directory; then
    exit 1
fi

# Initialize account directory
account_dir=$(initialize_account_directory "$ACCOUNT_NUM")
if [ $? -ne 0 ]; then
    write_error "Failed to initialize account directory"
    exit 1
fi

# Set environment variable
export CLAUDE_CONFIG_DIR="$account_dir"
write_success "Set CLAUDE_CONFIG_DIR: $account_dir"

# Update session state
update_session_state "$ACCOUNT_NUM"

# Check authentication status
eval $(get_account_status "$ACCOUNT_NUM")
if [ "$AUTHENTICATED" = "false" ]; then
    write_warning "Account $ACCOUNT_NUM needs authentication"
    write_info "Claude Code will prompt for login on first use"
else
    write_success "Account $ACCOUNT_NUM is authenticated"
fi

write_success "Successfully switched to Account $ACCOUNT_NUM"

# Launch Claude Code
if [ "$NO_LAUNCH" = false ]; then
    write_info "Launching Claude Code..."
    claude --dangerously-skip-permissions
fi

exit 0
