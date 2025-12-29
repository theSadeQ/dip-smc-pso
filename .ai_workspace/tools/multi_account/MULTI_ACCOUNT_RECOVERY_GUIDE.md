# Multi-Account Recovery Guide - Quick Start

**Purpose:** Resume work seamlessly when switching Claude Code accounts or starting new sessions.

**Audience:** You (when you need to pick up where another account left off)

**Time to recover:** 2-5 minutes

---

## Quick Recovery (30 seconds)

When you start a new session with a different account:

### Option 1: One-Command Recovery (Recommended)

```bash
bash .ai_workspace/dev_tools/recover_project.sh
```

This automatically:
- Shows project status and current phase
- Detects incomplete multi-agent work
- Lists recent commits
- Displays roadmap progress

**Then ask Claude:**
> "What was I working on in my last session? What should I resume?"

Claude will read the recovery output and tell you exactly what to do next.

---

## Detailed Recovery Workflow (5 minutes)

Use this when you need more control or context.

### Step 1: Check Project Status (30 seconds)

```bash
# Quick status overview
bash .ai_workspace/dev_tools/recover_project.sh

# Check recent work
git log --oneline -10
```

**What to look for:**
- Last commit message shows what was completed
- Current branch (usually `main`)
- Any uncommitted changes

### Step 2: Check for Incomplete Multi-Agent Work (1 minute)

```bash
# Analyze checkpoint status
python .ai_workspace/dev_tools/analyze_checkpoints.py
```

**Output shows:**
- [COMPLETE] - Agent finished successfully
- [INCOMPLETE] - Agent may need resumption

**IMPORTANT:** Not all "incomplete" agents need resumption! See Step 3.

### Step 3: Verify Real vs Test Checkpoints (2 minutes)

For each [INCOMPLETE] agent, verify if it's real work or a test artifact:

```bash
# Check if deliverable was actually completed
git log --oneline --all --grep="<TASK-ID>" -10

# Example: Check LT-4 completion
git log --oneline --all --grep="LT-4" -10

# Verify deliverable file exists and is complete
# (Check last 20 lines for completion markers)
tail -20 docs/theory/<deliverable-file>.md
```

**Signs work is COMPLETE (not really incomplete):**
- Git commit shows "Complete <TASK-ID>"
- Deliverable file has "Status: COMPLETE" or "PRODUCTION-READY"
- Commit date is BEFORE checkpoint creation date
- Deliverable file is 1000+ lines (substantial work)

**Signs work is REALLY INCOMPLETE:**
- No git commit for the task
- Deliverable file doesn't exist or is partial
- Checkpoint creation date is recent (today or yesterday)
- Progress checkpoint shows < 50% completion

### Step 4A: Resume Real Incomplete Work

If you found truly incomplete work, use the task wrapper to resume:

```python
from .project.dev_tools.task_wrapper import checkpoint_task_launch

# Read the progress checkpoint first
import json
progress = json.load(open('academic/<task>_<agent>_progress.json'))
print(f"Progress: {progress['hours_completed']}/{progress.get('estimated_hours', 'unknown')} hours")
print(f"Phase: {progress['current_phase']}")
print(f"Deliverables: {progress['deliverables_created']}")

# Resume from checkpoint
result = checkpoint_task_launch(
    task_id="<TASK-ID>",
    agent_id="<AGENT-ID>",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Resume incomplete work",
        "prompt": f"""Continue from checkpoint:

        Previous progress:
        - Hours completed: {progress['hours_completed']}
        - Current phase: {progress['current_phase']}
        - Deliverables created: {progress['deliverables_created']}

        Next steps:
        {progress.get('notes', 'Continue where you left off')}

        Please read the existing deliverables and continue the work.
        """
    },
    role=progress.get('role', 'Agent (resumed)')
)
```

### Step 4B: Clean Up Test Checkpoints

If all "incomplete" checkpoints are test artifacts, clean them up:

```bash
# Dry run (see what will be deleted)
python .ai_workspace/dev_tools/cleanup_test_checkpoints.py

# Actually delete test checkpoints
python .ai_workspace/dev_tools/cleanup_test_checkpoints.py --execute
```

---

## Common Scenarios

### Scenario 1: "I just switched accounts, what was I working on?"

**Solution:**
```bash
bash .ai_workspace/dev_tools/recover_project.sh
git log --oneline -10
```

Then ask Claude:
> "Based on the recovery output and recent commits, what was the last task completed and what should I work on next?"

---

### Scenario 2: "Multi-agent task hit token limit mid-execution"

**Solution:**
```bash
# Check checkpoint status
python .ai_workspace/dev_tools/analyze_checkpoints.py

# Find incomplete agents (look for [INCOMPLETE])
# Resume each incomplete agent
```

Then use Step 4A above to resume each agent.

---

### Scenario 3: "I see incomplete checkpoints but don't know if work is done"

**Solution:**
```bash
# For each incomplete checkpoint, check git history
git log --oneline --all --grep="<TASK-ID>" -10

# Check deliverable file completion status
tail -20 <deliverable-file>

# If file shows "COMPLETE" or "PRODUCTION-READY", it's a false positive
# If file is partial or missing, work is truly incomplete
```

Use Step 3 workflow above for detailed verification.

---

### Scenario 4: "Can I just delete all checkpoints and start fresh?"

**Answer:** Yes, but ONLY after verifying all work is committed to git!

```bash
# DANGEROUS - Verify work is committed first!
git log --oneline -20  # Check all recent work is committed

# Delete ALL checkpoints (only if safe)
python .ai_workspace/dev_tools/cleanup_test_checkpoints.py --all --execute
```

**Safer approach:** Only delete test checkpoints:
```bash
python .ai_workspace/dev_tools/cleanup_test_checkpoints.py --execute
```

---

## File Locations

### Recovery Tools
- **Main recovery script:** `.ai_workspace/dev_tools/recover_project.sh`
- **Checkpoint analyzer:** `.ai_workspace/dev_tools/analyze_checkpoints.py`
- **Cleanup script:** `.ai_workspace/dev_tools/cleanup_test_checkpoints.py`
- **Task wrapper:** `.ai_workspace/dev_tools/task_wrapper.py`

### Checkpoint Files
- **Location:** `academic/*.json`
- **Pattern:** `<task-id>_<agent-id>_[launched|progress|complete|output|failed].json`
- **Examples:**
  - `lt4_agent1_theory_launched.json` - Agent launch checkpoint
  - `lt4_agent1_theory_progress.json` - Progress checkpoint
  - `lt4_agent1_theory_complete.json` - Completion checkpoint
  - `lt4_agent1_theory_output.json` - Agent output artifact

### Documentation
- **This guide:** `.ai_workspace/dev_tools/MULTI_ACCOUNT_RECOVERY_GUIDE.md`
- **Task wrapper usage:** `.ai_workspace/dev_tools/TASK_WRAPPER_USAGE.md`
- **Checkpoint system design:** `.ai_workspace/config/agent_checkpoint_system.md`

---

## Understanding Checkpoint Lifecycle

### 1. Plan Approved
```json
{
  "task_id": "LT-4",
  "plan_summary": "Derive Lyapunov proofs for 5 controllers",
  "estimated_hours": 12.0,
  "agents": ["agent1_theory", "agent2_validation"]
}
```
**File:** `lt4_plan_approved.json`

### 2. Agent Launched
```json
{
  "task_id": "LT-4",
  "agent_id": "agent1_theory",
  "role": "Theory Specialist - Derive Lyapunov proofs",
  "status": "RUNNING",
  "launched_timestamp": "2025-11-11T11:04:28"
}
```
**File:** `lt4_agent1_theory_launched.json`

### 3. Agent Progress (auto-updated every 5 min)
```json
{
  "task_id": "LT-4",
  "agent_id": "agent1_theory",
  "status": "IN_PROGRESS",
  "hours_completed": 2.5,
  "deliverables_created": ["docs/theory/lyapunov_proofs.md"],
  "current_phase": "Proving Classical SMC",
  "notes": "Classical proof 50% complete"
}
```
**File:** `lt4_agent1_theory_progress.json`

### 4. Agent Complete
```json
{
  "task_id": "LT-4",
  "agent_id": "agent1_theory",
  "status": "COMPLETE",
  "hours_spent": 18.0,
  "deliverables": ["docs/theory/lyapunov_proofs.md"],
  "summary": "Completed all 6 Lyapunov proofs",
  "completion_timestamp": "2025-11-05T20:10:57"
}
```
**File:** `lt4_agent1_theory_complete.json`

### 5. Agent Output (captured automatically)
```json
{
  "task_id": "LT-4",
  "agent_id": "agent1_theory",
  "task_result": "... full agent output ...",
  "checkpoint_file": "lt4_agent1_theory_complete.json",
  "hours_spent": 18.0
}
```
**File:** `lt4_agent1_theory_output.json`

---

## Checkpoint Status Detection

### An agent is INCOMPLETE if:
1. `*_launched.json` exists
2. `*_complete.json` does NOT exist
3. `*_failed.json` does NOT exist

### An agent is COMPLETE if:
1. `*_complete.json` exists

### An agent FAILED if:
1. `*_failed.json` exists

### False Positives (appear incomplete but are actually complete):
1. Test checkpoints (task_id contains "TEST", "DEMO", "EXAMPLE")
2. Work completed outside checkpoint system (check git history)
3. Checkpoint from system testing (creation date after work completion)

---

## Troubleshooting

### Problem: "Checkpoint says incomplete but work looks done"

**Solution:** Check git history and deliverable file:
```bash
git log --oneline --all --grep="<TASK-ID>" -10
tail -30 <deliverable-file>
```

If git shows completion commit and file has "COMPLETE" status, it's a false positive. Safe to ignore or clean up.

---

### Problem: "Don't know which task to resume"

**Solution:** Check roadmap and current status:
```bash
bash .ai_workspace/dev_tools/recover_project.sh
cat .ai_workspace/planning/CURRENT_STATUS.md
```

Then ask Claude:
> "What's the current phase and what task should I work on next based on the roadmap?"

---

### Problem: "Multiple incomplete agents, which one first?"

**Solution:** Check hours completed and priority:
```bash
# For each incomplete agent
cat academic/<task>_<agent>_progress.json
```

Resume in this priority order:
1. Agents with highest hours_completed (finish what's closest to done)
2. Agents marked as dependencies for other tasks
3. Critical path tasks (LT-* long-term tasks usually more important than MT-* medium-term)

---

### Problem: "Token limit hit during multi-agent task, lost all work?"

**Answer:** No! Your work is safe. The checkpoint system preserves everything:

```bash
# Check what was saved
python .ai_workspace/dev_tools/analyze_checkpoints.py

# Resume incomplete agents
# (Use Step 4A workflow above)
```

All agent progress, deliverables, and outputs are saved in `academic/`.

---

## Best Practices

### DO:
- [OK] Run `recover_project.sh` at start of every new session
- [OK] Verify "incomplete" checkpoints against git history before resuming
- [OK] Ask Claude to read recovery output and recommend next steps
- [OK] Clean up test checkpoints periodically (monthly)
- [OK] Check deliverable files for completion markers before assuming incomplete

### DON'T:
- [ERROR] Delete checkpoints without checking git commits first
- [ERROR] Assume all "incomplete" flags mean work is unfinished
- [ERROR] Resume work without reading progress checkpoint first
- [ERROR] Skip verification step (Step 3) when recovering
- [ERROR] Delete production checkpoints (only clean test/demo)

---

## Quick Reference Commands

```bash
# START HERE - One-command recovery
bash .ai_workspace/dev_tools/recover_project.sh

# Check checkpoint status
python .ai_workspace/dev_tools/analyze_checkpoints.py

# Verify task completion in git
git log --oneline --all --grep="<TASK-ID>" -10

# Check deliverable completion
tail -20 <deliverable-file>

# Clean up test checkpoints
python .ai_workspace/dev_tools/cleanup_test_checkpoints.py --execute

# Resume incomplete agent (Python)
python -c "from .project.dev_tools.task_wrapper import checkpoint_task_launch; ..."
```

---

## Visual Workflow

```
[NEW SESSION STARTS]
        |
        v
[Run recover_project.sh] --> Shows: recent commits, project status, incomplete agents
        |
        v
[Check for incomplete agents] --> python analyze_checkpoints.py
        |
        +--> [None incomplete] --> Start new work
        |
        +--> [Some incomplete] --> Verify each against git
                |
                +--> [False positive] --> Clean up checkpoint
                |
                +--> [Really incomplete] --> Read progress checkpoint
                        |
                        v
                    [Resume with task_wrapper]
                        |
                        v
                    [Agent completes work]
                        |
                        v
                    [Commit deliverables to git]
                        |
                        v
                    [Clean up checkpoints]
```

---

## Example Session Recovery

### Real Example from November 11, 2025

**User switched accounts and asked:**
> "For resuming subagents workflow in my previous session with another account what should I do"

**Claude's response workflow:**
1. Ran `analyze_checkpoints.py` - Found 4 "incomplete" agents
2. Checked git history - Found LT-4 completed Nov 5 (6 days before checkpoint)
3. Verified deliverable - `lyapunov_stability_proofs.md` (1,427 lines, COMPLETE)
4. Identified root cause - Checkpoint from Nov 11 was from system testing, not real work
5. Created recovery tools and documentation
6. Result: **No resumption needed - all work complete!**

**Key lesson:** Always verify "incomplete" checkpoints against git history!

---

## Summary

**For quick recovery:**
```bash
bash .ai_workspace/dev_tools/recover_project.sh
```

**Then ask Claude:**
> "What should I resume based on the recovery output?"

**For detailed recovery:** Follow the 4-step workflow (Check Status → Analyze Checkpoints → Verify Real vs Test → Resume or Clean Up)

**Remember:** Not all "incomplete" checkpoints need resumption - always verify against git history first!

---

**Document Version:** 1.0
**Last Updated:** 2025-11-11
**Status:** PRODUCTION-READY
**Location:** `.ai_workspace/dev_tools/MULTI_ACCOUNT_RECOVERY_GUIDE.md`
