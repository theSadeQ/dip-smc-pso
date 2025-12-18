#!/bin/bash
# ============================================================================
# claude-profile.sh
# Bash Profile Integration for Claude Code Multi-Account System
# ============================================================================
#
# Purpose: Add account switching aliases to bash profile
# Author: Claude Code Multi-Account System
# Created: 2025-10-22
#
# Installation:
#   1. Add this line to your ~/.bashrc or ~/.bash_profile:
#      source /media/sadeq/asus1/Projects/main/.dev_tools/claude-profile.sh
#   2. Reload profile: source ~/.bashrc
#
# ============================================================================

SWITCHER_PATH="/media/sadeq/asus1/Projects/main/.dev_tools/switch-claude-account.sh"

if [ -f "$SWITCHER_PATH" ]; then
    # Make switcher executable if not already
    chmod +x "$SWITCHER_PATH"

    # Create the main switching function
    switch-claude-account() {
        "$SWITCHER_PATH" "$@"
    }

    # Create a smart function that handles c{number} pattern
    c() {
        if [ $# -eq 0 ]; then
            echo "Usage: c <account_number> [--no-launch]"
            echo "Example: c 5"
            return 1
        fi

        local account_num=$1
        local no_launch=false

        # Check for --no-launch flag
        shift
        while [[ $# -gt 0 ]]; do
            case $1 in
                --no-launch)
                    no_launch=true
                    shift
                    ;;
                *)
                    echo -e "\033[0;31m[ERROR]\033[0m Unknown option: $1"
                    return 1
                    ;;
            esac
        done

        # Run switch script to initialize account (but don't launch yet)
        "$SWITCHER_PATH" "$account_num" --no-launch
        local switch_result=$?

        if [ $switch_result -ne 0 ]; then
            echo -e "\033[0;31m[ERROR]\033[0m Failed to switch account"
            return 1
        fi

        # Set environment variable in CURRENT shell (not subprocess)
        local account_dir="$HOME/.claude$account_num"
        export CLAUDE_CONFIG_DIR="$account_dir"

        echo -e "\033[0;32m[OK]\033[0m Environment updated: CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"

        # Launch Claude Code if requested
        if [ "$no_launch" = false ]; then
            echo -e "\033[0;36m[INFO]\033[0m Launching Claude Code..."
            claude --dangerously-skip-permissions
        fi
    }

    # Additional helpful aliases
    claude-status() {
        "$SWITCHER_PATH" --validate
    }

    claude-primary() {
        # Clear environment variable in current shell
        if [ -n "$CLAUDE_CONFIG_DIR" ]; then
            unset CLAUDE_CONFIG_DIR
            echo -e "\033[0;32m[OK]\033[0m Cleared CLAUDE_CONFIG_DIR"
        fi

        echo -e "\033[0;32m[OK]\033[0m Now using primary .claude directory"
        echo -e "\033[0;36m[INFO]\033[0m Location: $HOME/.claude"

        # Launch Claude Code if not in no-launch mode
        if [ "$1" != "--no-launch" ]; then
            echo -e "\033[0;36m[INFO]\033[0m Launching Claude Code..."
            claude --dangerously-skip-permissions
        fi
    }

    claude-whoami() {
        if [ -z "$CLAUDE_CONFIG_DIR" ]; then
            echo -e "\033[0;36mCurrent account:\033[0m \033[1;37mprimary\033[0m"
            echo -e "\033[0;37mLocation: $HOME/.claude\033[0m"
        else
            # Extract account number
            if [[ "$CLAUDE_CONFIG_DIR" =~ \.claude([0-9]+)$ ]]; then
                local account_num="${BASH_REMATCH[1]}"
                echo -e "\033[0;36mCurrent account:\033[0m \033[1;37m$account_num\033[0m"
                echo -e "\033[0;37mLocation: $CLAUDE_CONFIG_DIR\033[0m"

                # Check authentication status
                if [ -f "$CLAUDE_CONFIG_DIR/.credentials.json" ]; then
                    echo -e "\033[0;37mAuth status: \033[0;32m✓ Authenticated\033[0m"
                else
                    echo -e "\033[0;37mAuth status: \033[1;33m! Needs login\033[0m"
                fi
            else
                echo -e "\033[0;36mCurrent account:\033[0m \033[1;33munknown\033[0m"
                echo -e "\033[0;37mCLAUDE_CONFIG_DIR: $CLAUDE_CONFIG_DIR\033[0m"
            fi
        fi
    }

    claude-help() {
        echo -e "\033[0;36mClaude Code Multi-Account Switcher\033[0m"
        echo -e "\033[0;36m====================================\033[0m"
        echo ""
        echo -e "\033[1;33mQuick switch:\033[0m"
        echo -e "  \033[1;37mc <number>\033[0m            Switch to account (1-5000)"
        echo -e "  \033[0;37mExample: c 15\033[0m         # Switches to account 15"
        echo -e "  \033[0;37mExample: c 2\033[0m          # Switches to account 2"
        echo ""
        echo -e "\033[1;33mCommands:\033[0m"
        echo -e "  \033[1;37mclaude-whoami\033[0m         Show current active account"
        echo -e "  \033[1;37mclaude-primary\033[0m        Switch back to primary .claude"
        echo -e "  \033[1;37mclaude-status\033[0m         Show all accounts and auth status"
        echo -e "  \033[1;37mclaude-help\033[0m           Show this help message"
        echo ""
        echo -e "\033[1;33mVSCode Integration:\033[0m"
        echo -e "  \033[1;37mcode-c <number> [path]\033[0m"
        echo -e "                        Launch VSCode with specific account"
        echo -e "  \033[0;37mExample: code-c 2 .\033[0m   # Opens current dir with account 2"
        echo -e "  \033[1;37mcode-primary [path]\033[0m   Launch VSCode with primary account"
        echo ""
        echo -e "\033[1;33mOptions:\033[0m"
        echo -e "  \033[1;37mc <number> --no-launch\033[0m"
        echo -e "                        Switch account without launching Claude"
        echo -e "  \033[1;37mclaude-primary --no-launch\033[0m"
        echo -e "                        Switch to primary without launching"
        echo ""
    }

    # VSCode Integration Functions
    code-c() {
        if [ $# -eq 0 ]; then
            echo "Usage: code-c <account_number> [path]"
            echo "Example: code-c 2 /path/to/project"
            return 1
        fi

        local account_num=$1
        shift

        # Validate account number
        if [ "$account_num" -lt 1 ] || [ "$account_num" -gt 5000 ]; then
            echo -e "\033[0;31m[ERROR]\033[0m Account number must be between 1 and 5000"
            return 1
        fi

        # Initialize account if needed (without launching)
        "$SWITCHER_PATH" "$account_num" --no-launch > /dev/null 2>&1

        # Set environment and launch VSCode
        local account_dir="$HOME/.claude$account_num"
        export CLAUDE_CONFIG_DIR="$account_dir"

        echo -e "\033[0;32m[OK]\033[0m Launching VSCode with Account $account_num"
        echo -e "\033[0;37m     CLAUDE_CONFIG_DIR: $CLAUDE_CONFIG_DIR\033[0m"

        # Launch VSCode with environment variable
        CLAUDE_CONFIG_DIR="$account_dir" code "$@"
    }

    code-primary() {
        # Unset environment variable
        unset CLAUDE_CONFIG_DIR

        echo -e "\033[0;32m[OK]\033[0m Launching VSCode with primary account"
        echo -e "\033[0;37m     Using: $HOME/.claude\033[0m"

        # Launch VSCode
        code "$@"
    }

    echo -e "\033[0;32m[OK]\033[0m Claude Code multi-account switcher loaded"
    echo -e "\033[0;37m     Type 'claude-help' for usage instructions\033[0m"

else
    echo -e "\033[1;33m[WARN]\033[0m Claude Code switcher not found at: $SWITCHER_PATH"
fi
