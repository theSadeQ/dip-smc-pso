#!/usr/bin/env bash
#==========================================================================================\\\
#===================== .dev_tools/git-hooks/install-hooks.sh =============================\\\
#==========================================================================================\\\
#
# Git Hooks Installation Script (Bash)
#
# This script installs the documentation quality pre-commit hook.
#
# Usage:
#   bash .dev_tools/git-hooks/install-hooks.sh
#
#==========================================================================================\\\

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Installing Git Hooks for Documentation Quality...${NC}"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not a git repository. Run this script from the project root.${NC}"
    exit 1
fi

# Create hooks directory if it doesn't exist
if [ ! -d ".git/hooks" ]; then
    mkdir -p .git/hooks
    echo -e "${GREEN}Created .git/hooks directory${NC}"
fi

# Install pre-commit hook
if [ -f ".git/hooks/pre-commit" ]; then
    echo -e "${YELLOW}Warning: Existing pre-commit hook found.${NC}"
    echo -e "${YELLOW}Creating backup: .git/hooks/pre-commit.backup${NC}"
    mv .git/hooks/pre-commit .git/hooks/pre-commit.backup
fi

cp .dev_tools/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo -e "${GREEN}✓ Installed pre-commit hook${NC}"
echo ""
echo -e "${BLUE}Git Hook Installation Complete!${NC}"
echo ""
echo -e "The pre-commit hook will now:"
echo -e "  • Scan staged markdown files in docs/ for AI-ish patterns"
echo -e "  • Block commits with >5 patterns per file"
echo -e "  • Enforce CLAUDE.md Section 15: Documentation Quality Standards"
echo ""
echo -e "${YELLOW}To bypass the hook (emergency only):${NC}"
echo -e "  git commit --no-verify"
echo ""
echo -e "${GREEN}Test the hook with:${NC}"
echo -e "  # Stage a documentation file"
echo -e "  git add docs/some-file.md"
echo -e "  git commit -m \"Test commit\""
echo ""
