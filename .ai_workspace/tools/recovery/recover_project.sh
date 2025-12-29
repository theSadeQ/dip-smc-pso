#!/bin/bash
# =============================================================================
# Project Recovery Script - 30-second recovery from token limit or multi-month gap
# =============================================================================
#
# Purpose: Show complete project context in one command
# Usage: bash .ai_workspace/tools/recovery/recover_project.sh
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

# Canonical state file location (migrated 2025-12-18)
if [ -f ".ai_workspace/state/project_state.json" ]; then
    STATE_FILE=".ai_workspace/state/project_state.json"
elif [ -f ".ai_workspace/ai/config/project_state.json" ]; then
    STATE_FILE=".ai_workspace/ai/config/project_state.json"
    echo -e "${YELLOW}[WARNING] Using deprecated state file path (.ai_workspace/ai/config/)${NC}"
    echo -e "${YELLOW}           Please migrate to .ai_workspace/recovery/state/${NC}"
else
    echo -e "${YELLOW}[WARNING] Project state not initialized${NC}"
    echo "Run: python .ai_workspace/tools/recovery/project_state_manager.py init"
    STATE_FILE=""
fi

if [ -n "$STATE_FILE" ]; then
    # Use Python to parse and display state
    python .ai_workspace/tools/recovery/project_state_manager.py status
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
\) -mtime -7 2>/dev/null || true)

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
# 5. Incomplete Agent Work
# =============================================================================

echo -e "${GREEN}[5] INCOMPLETE AGENT WORK${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"

# Detect incomplete multi-agent orchestrations
incomplete_agents=$(python -c "
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location('agent_checkpoint', '.dev_tools/agent_checkpoint.py')
    agent_checkpoint = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent_checkpoint)

    agents = agent_checkpoint.get_incomplete_agents()
    if agents:
        for agent in agents:
            print(f\"{agent['task_id']}|{agent['agent_id']}|{agent['role']}|{agent['launched_timestamp']}\")
            if agent.get('last_progress'):
                print(f\"  PROGRESS|{agent['last_progress'].get('current_phase', 'Unknown')}\")
except Exception as e:
    import traceback
    traceback.print_exc()
" 2>/dev/null)

if [ -n "$incomplete_agents" ]; then
    echo -e "${YELLOW}⚠️  INCOMPLETE AGENT WORK DETECTED${NC}"
    echo ""

    current_task=""
    while IFS='|' read -r task agent role timestamp rest; do
        if [ "$task" = "  PROGRESS" ]; then
            echo -e "    ${CYAN}Last progress: $agent${NC}"
        else
            if [ "$task" != "$current_task" ]; then
                [ -n "$current_task" ] && echo ""
                echo -e "${YELLOW}Task: $task${NC}"
                current_task="$task"
            fi
            echo -e "  Agent: ${YELLOW}$agent${NC}"
            echo -e "    Role: $role"
            echo -e "    Launched: $timestamp"
        fi
    done <<< "$incomplete_agents"

    echo ""
    echo -e "${CYAN}RECOMMENDATION:${NC}"
    echo "  One or more agents were interrupted before completion."
    echo "  Check .artifacts/*_launched.json for details."
    echo "  Resume work by re-launching the incomplete agent."
else
    echo -e "${GREEN}✓ No incomplete agent work detected${NC}"
fi

echo ""

# =============================================================================

# =============================================================================
# 6. Thesis Verification Status (LT-8)
# =============================================================================

echo -e "${GREEN}[6] THESIS VERIFICATION STATUS${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"

# Check if thesis verification is in progress
if [ -d ".artifacts/thesis/checkpoints" ] && [ -f ".artifacts/thesis/checkpoints/checkpoint_latest.json" ]; then
    echo -e "${YELLOW}[THESIS VERIFICATION IN PROGRESS]${NC}"
    echo ""

    # Use Python checkpoint manager to show status
    python scripts/thesis/checkpoint_verification.py --status

    echo ""
    echo -e "${CYAN}RESUME THESIS VERIFICATION:${NC}"
    echo "  python scripts/thesis/checkpoint_verification.py --resume"
    echo "  python scripts/thesis/verify_chapter.py --chapter N --comprehensive --save"
    echo ""
elif [ -d ".artifacts/thesis" ]; then
    echo -e "${YELLOW}[INFO] Thesis verification artifacts found but no active checkpoint${NC}"
    echo "Start thesis verification:"
    echo "  python scripts/thesis/verify_chapter.py --chapter 0 --comprehensive --save"
    echo ""
else
    echo -e "${GREEN}[OK] No thesis verification in progress${NC}"
    echo "To start LT-8 thesis verification:"
    echo "  See: docs/thesis/verification/VERIFICATION_ROADMAP.md"
    echo "  Run: python scripts/thesis/verify_chapter.py --chapter 0 --comprehensive --save"
fi

echo ""

# 6. Recommended Next Actions
# =============================================================================

echo -e "${GREEN}[7] RECOMMENDED NEXT ACTIONS${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"

# Dual-path support for state files
if [ -f ".ai_workspace/recovery/state/project_state.json" ] || [ -f ".ai_workspace/ai/config/project_state.json" ]; then
    python .ai_workspace/tools/recovery/project_state_manager.py recommend-next
else
    echo -e "${YELLOW}[WARNING] Project state not initialized - cannot recommend tasks${NC}"
    echo "Run: python .ai_workspace/tools/recovery/project_state_manager.py init"
fi

echo ""

# =============================================================================
# 8. Quick Start Commands
# =============================================================================

echo -e "${GREEN}[8] QUICK START COMMANDS${NC}"
echo -e "${CYAN}------------------------------------------------------------------------------${NC}"
echo ""
echo "Initialize project state:"
echo "  python .ai_workspace/tools/recovery/project_state_manager.py init"
echo ""
echo "Mark task complete:"
echo "  python .ai_workspace/tools/recovery/project_state_manager.py complete MT-5 --deliverables MT5_COMPLETE_ANALYSIS.md"
echo ""
echo "Check roadmap progress:"
echo "  python .ai_workspace/tools/recovery/roadmap_tracker.py"
echo ""
echo "Run recovery again:"
echo "  bash .ai_workspace/tools/recovery/recover_project.sh"
echo ""

echo -e "${CYAN}=============================================================================="
echo -e "RECOVERY COMPLETE"
echo -e "==============================================================================${NC}"
echo ""
