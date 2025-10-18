#!/bin/bash
# =============================================================================
# Project Recovery Script - 30-second recovery from token limit or multi-month gap
# =============================================================================
#
# Purpose: Show complete project context in one command
# Usage: bash .dev_tools/recover_project.sh
#
# What it shows:
# - Current phase and roadmap progress
# - Completed phases (Phase 3, Phase 4)
# - Last 5 commits (recent work)
# - Current git status (uncommitted changes)
# - Next recommended tasks
#
# Author: Recovery System Implementation (Oct 2025)
# =============================================================================

set -e  # Exit on error

# Colors for output (works in Git Bash on Windows)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${CYAN}=============================================================================="
echo -e "PROJECT RECOVERY - Complete Context"
echo -e "==============================================================================${NC}"
echo ""

# =============================================================================
# 1. Project State (from project_state_manager.py)
# =============================================================================

echo -e "${GREEN}[1] PROJECT STATE${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"

if [ -f ".ai/config/project_state.json" ]; then
    # Use Python to parse and display state
    python .dev_tools/project_state_manager.py status
else
    echo -e "${YELLOW}[WARNING] Project state not initialized${NC}"
    echo "Run: python .dev_tools/project_state_manager.py init"
fi

echo ""

# =============================================================================
# 2. Git Context (last 5 commits)
# =============================================================================

echo -e "${GREEN}[2] RECENT WORK (Last 5 Commits)${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"

git log -5 --oneline --decorate --graph --all

echo ""

# =============================================================================
# 3. Current Branch & Status
# =============================================================================

echo -e "${GREEN}[3] CURRENT GIT STATUS${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"

echo -e "Branch: ${YELLOW}$(git branch --show-current)${NC}"
echo -e "Remote: ${YELLOW}$(git remote get-url origin)${NC}"
echo ""

# Show uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}[UNCOMMITTED CHANGES]${NC}"
    git status --short
else
    echo -e "${GREEN}[OK] No uncommitted changes${NC}"
fi

echo ""

# =============================================================================
# 4. Checkpoint Files (recent deliverables)
# =============================================================================

echo -e "${GREEN}[4] RECENT CHECKPOINT FILES${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"

# Find checkpoint files (modified in last 7 days)
checkpoint_files=$(find . -maxdepth 1 -type f \( \
    -name "*.json" -o \
    -name "*_results.json" -o \
    -name "*_benchmark*.csv" -o \
    -name "*_ANALYSIS.md" -o \
    -name "*_SUMMARY.md" \
) -mtime -7 2>/dev/null || true)

if [ -n "$checkpoint_files" ]; then
    echo "$checkpoint_files" | while read -r file; do
        if [ -f "$file" ]; then
            size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo "?")
            mod_time=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1 || stat -f%Sm -t "%Y-%m-%d" "$file" 2>/dev/null || echo "unknown")
            echo "  $file ($size bytes, modified: $mod_time)"
        fi
    done
else
    echo -e "${YELLOW}[INFO] No recent checkpoint files found${NC}"
fi

echo ""

# =============================================================================
# 5. Recommended Next Actions
# =============================================================================

echo -e "${GREEN}[5] RECOMMENDED NEXT ACTIONS${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"

if [ -f ".ai/config/project_state.json" ]; then
    python .dev_tools/project_state_manager.py recommend-next
else
    echo -e "${YELLOW}[WARNING] Project state not initialized - cannot recommend tasks${NC}"
    echo "Run: python .dev_tools/project_state_manager.py init"
fi

echo ""

# =============================================================================
# 6. Quick Start Commands
# =============================================================================

echo -e "${GREEN}[6] QUICK START COMMANDS${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"
echo ""
echo "Initialize project state:"
echo "  python .dev_tools/project_state_manager.py init"
echo ""
echo "Mark task complete:"
echo "  python .dev_tools/project_state_manager.py complete MT-5 --deliverables MT5_COMPLETE_ANALYSIS.md"
echo ""
echo "Check roadmap progress:"
echo "  python .dev_tools/roadmap_tracker.py"
echo ""
echo "Run recovery again:"
echo "  bash .dev_tools/recover_project.sh"
echo ""

echo -e "${CYAN}=============================================================================="
echo -e "RECOVERY COMPLETE"
echo -e "==============================================================================${NC}"
echo ""
