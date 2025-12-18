#!/bin/bash
# ==============================================================================
# Shell Initialization - Automatic Recovery on Terminal Startup
# ==============================================================================
# Add this to your ~/.bashrc or ~/.zshrc for automatic recovery prompts:
#
#   if [ -f "$HOME/Projects/main/.dev_tools/shell_init.sh" ]; then
#       source "$HOME/Projects/main/.dev_tools/shell_init.sh"
#   fi
#
# Features:
#   - Detects if you're in the project directory
#   - Prompts for recovery if git commits detected since last session
#   - Silent if no recovery needed
# ==============================================================================

# Only run if in the project directory
if [[ "$PWD" == *"/Projects/main"* ]] || [[ "$PWD" == *"\Projects\main"* ]]; then
    PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"

    if [[ -n "$PROJECT_ROOT" ]] && [[ -f "$PROJECT_ROOT/.dev_tools/recover_project.sh" ]]; then
        STATE_FILE="$PROJECT_ROOT/.ai/config/project_state.json"
        LAST_RECOVERY_FILE="$PROJECT_ROOT/.ai/config/.last_recovery"

        # Check if recovery needed (new commits since last recovery)
        CURRENT_COMMIT=$(git rev-parse HEAD 2>/dev/null)
        LAST_RECOVERY=""

        if [[ -f "$LAST_RECOVERY_FILE" ]]; then
            LAST_RECOVERY=$(cat "$LAST_RECOVERY_FILE")
        fi

        # Recovery needed if:
        #   1. Never recovered before, OR
        #   2. New commits since last recovery
        if [[ -z "$LAST_RECOVERY" ]] || [[ "$CURRENT_COMMIT" != "$LAST_RECOVERY" ]]; then
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "[INFO] New commits detected - recovery available"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "Run: bash .dev_tools/recover_project.sh"
            echo "      (30-second context restoration)"
            echo ""

            # Optional: Auto-recover on startup (uncomment to enable)
            # bash "$PROJECT_ROOT/.dev_tools/recover_project.sh"
            # echo "$CURRENT_COMMIT" > "$LAST_RECOVERY_FILE"
        fi
    fi
fi
