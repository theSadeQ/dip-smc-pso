# Recovery Tools - Quick Reference

**Location:** `.ai_workspace/dev_tools/`

**Purpose:** Tools for resuming work across sessions, accounts, and token limits

---

## Quick Start (Choose One)

### Option 1: Windows One-Click Recovery
```bash
# Double-click this file in Windows Explorer
quick_recovery.bat
```

### Option 2: Command Line Recovery
```bash
# Linux/Mac/Windows Git Bash
bash .ai_workspace/dev_tools/recover_project.sh
python .ai_workspace/dev_tools/analyze_checkpoints.py
```

### Option 3: Ask Claude
Just ask:
> "What was I working on in my last session? What should I resume?"

Claude will automatically run recovery tools and tell you what to do next.

---

## All Recovery Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| **quick_recovery.bat** | One-click recovery (Windows) | Double-click or run from cmd |
| **recover_project.sh** | Main recovery script | `bash recover_project.sh` |
| **analyze_checkpoints.py** | Check multi-agent status | `python analyze_checkpoints.py` |
| **cleanup_test_checkpoints.py** | Clean test artifacts | `python cleanup_test_checkpoints.py` |
| **task_wrapper.py** | Resume agents with checkpoints | `from task_wrapper import checkpoint_task_launch` |
| **MULTI_ACCOUNT_RECOVERY_GUIDE.md** | Complete recovery workflow | Read for detailed instructions |

---

## Common Scenarios

### "I just switched accounts, what was I working on?"

**Solution:**
```bash
quick_recovery.bat  # Windows
# OR
bash recover_project.sh  # Linux/Mac
```

Then check the output for recent commits and ask Claude what to do next.

---

### "Multi-agent task hit token limit, lost work?"

**Solution:** No work lost! Checkpoints preserved everything.

```bash
python analyze_checkpoints.py
```

Look for [INCOMPLETE] agents, then resume using `task_wrapper.py`.

---

### "See incomplete checkpoints, don't know if real or test?"

**Solution:** Verify against git history:
```bash
git log --oneline --all --grep="<TASK-ID>" -10
tail -20 <deliverable-file>
```

If git shows completion commit and file has "COMPLETE" marker, it's a false positive.

---

### "Want to clean up old test checkpoints?"

**Solution:**
```bash
# Dry run (see what will be deleted)
python cleanup_test_checkpoints.py

# Actually delete
python cleanup_test_checkpoints.py --execute
```

---

## File Locations

### Checkpoint Files
- **Location:** `academic/*.json`
- **Pattern:** `<task-id>_<agent-id>_[launched|progress|complete|output].json`
- **Auto-created:** When using `checkpoint_task_launch()` from `task_wrapper.py`

### Recovery Logs
- **Location:** Terminal output (not saved by default)
- **Contains:** Git commits, project status, incomplete agents

---

## Documentation

- **MULTI_ACCOUNT_RECOVERY_GUIDE.md** - Complete step-by-step recovery workflow
- **TASK_WRAPPER_USAGE.md** - How to use checkpoint system for multi-agent tasks
- **CLAUDE.md (Section 3)** - Quick reference in main project instructions

---

## When to Use Each Tool

| Situation | Tool | Command |
|-----------|------|---------|
| Starting new session | quick_recovery.bat | Double-click |
| Switched accounts | recover_project.sh | `bash recover_project.sh` |
| Token limit hit mid-task | analyze_checkpoints.py | `python analyze_checkpoints.py` |
| Need to resume agent | task_wrapper.py | See TASK_WRAPPER_USAGE.md |
| Clean up after testing | cleanup_test_checkpoints.py | `python cleanup_test_checkpoints.py --execute` |
| Don't know what to do | Just ask Claude | "What should I resume?" |

---

## Recovery Workflow (Visual)

```
[NEW SESSION STARTS]
        |
        v
[Run quick_recovery.bat OR recover_project.sh]
        |
        v
[Check output for incomplete agents]
        |
        +--> [None incomplete] --> Ask Claude: "What should I work on next?"
        |
        +--> [Some incomplete] --> Run: python analyze_checkpoints.py
                |
                v
            [Categorize: Real vs Test]
                |
                +--> [All test artifacts] --> Run: python cleanup_test_checkpoints.py --execute
                |
                +--> [Real incomplete work] --> Verify against git (see guide)
                        |
                        v
                    [If truly incomplete] --> Resume with task_wrapper.py
                        |
                        v
                    [If false positive] --> Ignore or clean up
```

---

## Examples

### Example 1: Quick Recovery
```bash
# Windows
quick_recovery.bat

# Output shows:
# - Recent commits
# - Project status
# - Incomplete agents (if any)
# - Recommendations
```

### Example 2: Check Incomplete Work
```bash
python analyze_checkpoints.py

# Output shows:
# [COMPLETE] ca-02-victory_agent1_docs
# [INCOMPLETE] lt4_agent1_theory
#
# SUMMARY:
#   Real incomplete work: 1
#   Test/demo incomplete: 3
```

### Example 3: Verify False Positive
```bash
# Check git for completion
git log --oneline --all --grep="LT-4" -10

# Output shows:
# 1447585a docs(research): Complete LT-4 Lyapunov proofs
#
# Conclusion: Checkpoint is false positive, work is done!
```

### Example 4: Clean Up Test Checkpoints
```bash
# Dry run
python cleanup_test_checkpoints.py

# Actually delete
python cleanup_test_checkpoints.py --execute

# Output shows:
# Successfully deleted: 13
# Preserved: 12
```

---

## Troubleshooting

### Problem: "Script says incomplete but work looks done"

**Solution:** Check git history and file:
```bash
git log --oneline --all --grep="<TASK-ID>" -10
tail -30 <deliverable-file>
```

If completion commit exists and file has "COMPLETE" marker, it's safe to ignore/clean up.

---

### Problem: "Don't know which recovery tool to use"

**Solution:** Start with the simplest:
```bash
quick_recovery.bat  # Windows one-click
```

Or just ask Claude!

---

### Problem: "Checkpoint system not working"

**Solution:** Check if using `checkpoint_task_launch()`:
```python
from .project.dev_tools.task_wrapper import checkpoint_task_launch

# Correct usage
result = checkpoint_task_launch(task_id="...", agent_id="...", ...)

# Wrong usage (no checkpoints)
Task(description="...", prompt="...", subagent_type="...")
```

Checkpoints only work when using `checkpoint_task_launch()` wrapper!

---

## Best Practices

### DO:
- [OK] Run `quick_recovery.bat` at start of every new session
- [OK] Verify "incomplete" against git before resuming
- [OK] Ask Claude to interpret recovery output
- [OK] Clean up test checkpoints monthly
- [OK] Read MULTI_ACCOUNT_RECOVERY_GUIDE.md for first-time use

### DON'T:
- [ERROR] Delete checkpoints without checking git first
- [ERROR] Assume all "incomplete" means work is unfinished
- [ERROR] Resume without reading progress checkpoint
- [ERROR] Use `--all` flag on cleanup script (deletes production checkpoints!)

---

## Getting Help

1. **Read the guide:** `MULTI_ACCOUNT_RECOVERY_GUIDE.md`
2. **Ask Claude:** "How do I recover my work from the previous session?"
3. **Check CLAUDE.md:** Section 3 (Session Continuity)
4. **Run tools with --help:** Most scripts support `--help` flag

---

**Document Version:** 1.0
**Last Updated:** 2025-11-11
**Status:** PRODUCTION-READY
