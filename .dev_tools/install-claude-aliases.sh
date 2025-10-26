#!/bin/bash
# ============================================================================
# install-claude-aliases.sh
# One-time setup script for Claude multi-account aliases
# ============================================================================

PROFILE_SCRIPT="/media/sadeq/asus1/Projects/main/.dev_tools/claude-profile.sh"

# Detect shell
if [ -n "$BASH_VERSION" ]; then
    SHELL_NAME="bash"
    PROFILE_FILE="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_NAME="zsh"
    PROFILE_FILE="$HOME/.zshrc"
else
    echo "Unknown shell. Please manually add to your shell profile:"
    echo "source $PROFILE_SCRIPT"
    exit 1
fi

echo "Detected shell: $SHELL_NAME"
echo "Profile file: $PROFILE_FILE"
echo ""

# Check if already installed
if grep -q "claude-profile.sh" "$PROFILE_FILE" 2>/dev/null; then
    echo "[INFO] Claude multi-account aliases already installed in $PROFILE_FILE"
    echo "[INFO] Reload your shell profile to ensure latest version:"
    echo ""
    echo "    source $PROFILE_FILE"
    echo ""
    exit 0
fi

# Add to profile
echo "Adding Claude multi-account aliases to $PROFILE_FILE..."
echo "" >> "$PROFILE_FILE"
echo "# Claude Code Multi-Account System" >> "$PROFILE_FILE"
echo "source $PROFILE_SCRIPT" >> "$PROFILE_FILE"

echo ""
echo "[OK] Successfully installed Claude multi-account aliases!"
echo ""
echo "To activate in current session, run:"
echo ""
echo "    source $PROFILE_FILE"
echo ""
echo "Then you can use commands like:"
echo "    c 5          # Switch to account 5"
echo "    c 42         # Switch to account 42"
echo "    claude-help  # Show all commands"
echo ""
