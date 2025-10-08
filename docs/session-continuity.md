# Session Continuity System - Zero-Effort Account Switching

## Overview

The **Session Continuity System** enables completely **automatic context handoff** when switching Claude Code accounts due to token limits. No manual prompt writing required—just switch accounts and say "continue" (or even "hi"), and Claude automatically resumes where you left off.

## Problem Solved

**Before Session Continuity:**
```
1. Account A hits token limit (200k tokens consumed)
2. You manually write detailed handoff:
   - "We were implementing feature X..."
   - "Completed: task 1, task 2..."
   - "In progress: task 3..."
   - "Next steps: task 4, task 5..."
   - "Important context: decision A, decision B..."
3. Copy handoff text
4. Switch to Account B
5. Paste handoff as new prompt
6. Claude reads and resumes

⏱️ Time: 5-10 minutes of manual work
❌ Error-prone: Easy to forget context
```

**After Session Continuity:**
```
1. Account A hits token limit
2. Switch to Account B
3. Say: "continue"
4. Claude: "Continuing from previous session (2 hours ago):
            Task: Implementing feature X
            Completed: 5 items, Pending: 2 items
            Let me check current status..."
5. Claude automatically resumes work

⏱️ Time: 10 seconds
✅ Reliable: Full context auto-loaded
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Session State (.dev_tools/session_state.json)      │
│  ├─ Current task & phase                            │
│  ├─ Completed/In progress/Pending todos             │
│  ├─ Important decisions made                        │
│  ├─ Next actions to take                            │
│  ├─ Files modified                                  │
│  └─ Timestamp & metadata                            │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  Automated Backups (every 1 minute)                 │
│  ├─ Commits session_state.json to git              │
│  ├─ Pushes to origin/main                          │
│  └─ Creates audit trail                            │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  Claude Auto-Detection (new session)                │
│  ├─ Checks for session_state.json                  │
│  ├─ Verifies timestamp < 24 hours                  │
│  ├─ Loads context automatically                    │
│  └─ Displays summary & resumes                     │
└─────────────────────────────────────────────────────┘
```

## How It Works

### During Active Session (Account A)

Claude **automatically** maintains session state throughout work:

1. **Starting new task:**
   ```python
   update_session_context(
       current_task="Implementing automated backup system",
       phase="implementation"
   )
   ```

2. **Completing todo items:**
   ```python
   add_completed_todo("Create PowerShell backup script")
   add_completed_todo("Write documentation")
   ```

3. **Making decisions:**
   ```python
   add_decision("Task Scheduler frequency: 1 minute")
   add_decision("Use ISO 8601 timestamp format")
   ```

4. **Identifying next actions:**
   ```python
   add_next_action("User needs to register Task Scheduler job")
   add_next_action("Run smoke test to verify functionality")
   ```

5. **Automatic commits:**
   - Session state committed every 1 minute (automated backup system)
   - Git history provides full audit trail

### Approaching Token Limit (Account A)

Claude detects token pressure and finalizes session:

```python
mark_token_limit_approaching()
finalize_session("Automated backup system implementation complete")
```

**Session state now contains:**
- Complete task summary
- All completed/pending todos
- All decisions made
- Clear next actions
- Comprehensive context

**User action:** Switch to Account B (no manual handoff needed!)

### New Session Start (Account B)

**User says:** `"continue"` (or `"hi"` or `"help"` or anything)

**Claude automatically:**
1. Checks `.dev_tools/session_state.json`
2. Verifies `last_updated` < 24 hours ago
3. Loads session context
4. Displays summary:

```
Continuing from previous session (2 hours ago):
Task: Implementing automated backup system
Phase: implementation
Last commit: c8c9c64

Completed: 5 items
In progress: 0 items
Pending: 2 items

Next actions:
1. User needs to register Task Scheduler job
2. Run smoke test to verify functionality

Let me check the current repository status...
```

5. **Immediately resumes work** based on loaded context

## Session State File

**Location:** `.dev_tools/session_state.json`

**Structure:**
```json
{
  "session_id": "session_20251001_104700",
  "last_updated": "2025-10-01T10:47:00",
  "account": "account_1",
  "token_limit_approaching": false,
  "status": "active",

  "context": {
    "current_task": "Implementing automated backup system",
    "phase": "completed",
    "last_commit": "c8c9c64",
    "branch": "main",
    "working_directory": "D:\\Projects\\main"
  },

  "todos": {
    "completed": [
      "Create PowerShell backup script",
      "Create backup log directory",
      "Create documentation",
      "Update README.md",
      "Commit and push"
    ],
    "in_progress": [],
    "pending": [
      "User needs to register Task Scheduler job",
      "Run smoke test"
    ]
  },

  "decisions": [
    "Task Scheduler frequency: 1 minute",
    "Commit timestamp format: ISO 8601",
    "Log location: .dev_tools/backup/backup.log"
  ],

  "next_actions": [
    "Register Task Scheduler: schtasks /Create ...",
    "Run smoke test: Make change → checkpoint → verify",
    "Monitor first automatic backups"
  ],

  "files_modified": [
    ".dev_tools/claude-backup.ps1",
    "docs/claude-backup.md",
    "README.md"
  ],

  "important_context": {
    "remote_url": "https://github.com/theSadeQ/dip-smc-pso.git",
    "backup_frequency_minutes": 1,
    "manual_checkpoint_command": "powershell ... -Checkpoint"
  },

  "metadata": {
    "schema_version": "1.0",
    "created": "2025-10-01T10:47:00",
    "last_account_switch": null,
    "session_count": 1
  }
}
```

## Python Helper API

**Location:** `.dev_tools/session_manager.py`

### Core Functions

#### **Session Detection**
```python
from session_manager import has_recent_session, get_session_summary

# Check if there's a recent session to continue
if has_recent_session(threshold_hours=24):
    print(get_session_summary())
```

#### **Session Loading**
```python
from session_manager import load_session

state = load_session()
if state:
    current_task = state['context']['current_task']
    phase = state['context']['phase']
    next_actions = state['next_actions']
```

#### **Context Updates**
```python
from session_manager import update_session_context

update_session_context(
    current_task="Implementing feature X",
    phase="testing",
    last_commit="abc1234"
)
```

#### **Progress Tracking**
```python
from session_manager import add_completed_todo, add_decision, add_next_action

# Mark todo as complete
add_completed_todo("Write unit tests")

# Record important decision
add_decision("Use pytest for testing framework")

# Specify next action
add_next_action("Run full test suite")
```

#### **Token Limit Preparation**
```python
from session_manager import mark_token_limit_approaching, finalize_session

# Mark approaching limit
mark_token_limit_approaching()

# Finalize with summary
finalize_session("Completed feature X implementation")
```

## Integration with Automated Backups

The session continuity system is **fully integrated** with the automated backup system:

1. **Session state is automatically committed** every 1 minute
2. **No manual git operations** required
3. **Git history provides audit trail** of all session state changes
4. **Backup script** (`.dev_tools/claude-backup.ps1`) includes `session_state.json`

**Verification:**
```bash
# Check recent commits including session state
git log --oneline -10 -- .dev_tools/session_state.json

# View session state changes over time
git diff HEAD~5..HEAD -- .dev_tools/session_state.json
```

## Usage Examples

### Example 1: Simple Feature Implementation

**Session 1 (Account A):**
```python
# Claude automatically throughout:
update_session_context(current_task="Add logging module", phase="implementation")
add_completed_todo("Create logger.py")
add_completed_todo("Add log configuration")
add_decision("Use Python logging library")
add_next_action("Write unit tests for logger")

# Token limit approaching:
finalize_session("Logging module implementation complete")
```

**Session 2 (Account B):**
```
User: "continue"

Claude: "Continuing from previous session (1 hour ago):
Task: Add logging module
Phase: implementation
Completed: 2 items, Pending: 1 item

Next actions:
1. Write unit tests for logger

Let me check the logger.py file and create tests..."
```

### Example 2: Long-Running PSO Optimization

**Session 1 (Account A - Starting PSO):**
```python
update_session_context(
    current_task="PSO optimization for classical SMC",
    phase="running"
)
add_decision("PSO parameters: 30 particles, 150 iterations")
add_next_action("Wait for PSO completion (~3 hours)")
add_next_action("Validate results when complete")
finalize_session("PSO optimization started, awaiting completion")
```

**Session 2 (Account B - 3 hours later):**
```
User: "continue"

Claude: "Continuing from previous session (3 hours ago):
Task: PSO optimization for classical SMC
Phase: running
Next action: Wait for PSO completion, then validate

Let me check if PSO has completed...
[Checks log files]
PSO complete! Let me validate the results..."
```

## Configuration

### Auto-Load Threshold

Default: **24 hours**

Change threshold by modifying `.dev_tools/session_manager.py`:
```python
AUTO_LOAD_THRESHOLD_HOURS = 48  # 48 hours instead of 24
```

### Session State Schema Version

Current: **1.0**

Future versions will maintain backward compatibility with older schemas.

## Troubleshooting

### Claude Doesn't Auto-Load Session

**Symptoms:** New session starts fresh, ignores session_state.json

**Possible Causes:**
1. Session state file > 24 hours old
2. File doesn't exist or is malformed JSON
3. CLAUDE.md not loaded properly

**Solutions:**
```bash
# 1. Check file exists and is recent
ls -lh .dev_tools/session_state.json
cat .dev_tools/session_state.json | python -m json.tool

# 2. Verify CLAUDE.md is in repo root
ls CLAUDE.md

# 3. Manually trigger continuation
python .dev_tools/session_manager.py
```

### Session State Not Updating

**Symptoms:** Session state stays stale, doesn't reflect current work

**Possible Causes:**
1. Claude not calling update functions
2. File permissions issue
3. Automatic backups not running

**Solutions:**
```bash
# 1. Check file is writable
ls -lh .dev_tools/session_state.json

# 2. Manually update to test
python -c "from sys import path; path.insert(0, '.dev_tools'); from session_manager import update_session_context; update_session_context(current_task='test')"

# 3. Verify automatic backups are running
schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST
```

### Session State Merge Conflicts

**Symptoms:** Git merge conflicts in session_state.json

**Cause:** Multiple accounts editing simultaneously (rare)

**Solution:**
```bash
# Accept the most recent version
git checkout --theirs .dev_tools/session_state.json
git add .dev_tools/session_state.json
git commit -m "Resolve session state conflict"
```

## Benefits Summary

✅ **Zero Manual Handoff** - No prompt writing when switching accounts
✅ **Instant Resume** - Claude continues work in seconds, not minutes
✅ **Full Context** - All todos, decisions, and next actions preserved
✅ **Audit Trail** - Git history tracks all session state changes
✅ **Reliable** - JSON schema with validation and error handling
✅ **Transparent** - Human-readable session state file
✅ **Automatic** - No user intervention required during session
✅ **Efficient** - Minimal overhead (JSON read/write)

## Advanced Features

### Session Count Tracking

Track how many times accounts have been switched:
```python
state = load_session()
session_count = state['metadata']['session_count']
print(f"This is session #{session_count}")
```

### Custom Session ID

Each session has a unique ID:
```python
state = load_session()
session_id = state['session_id']
# Example: "session_20251001_104700"
```

### Last Account Switch Timestamp

Know when the last account switch occurred:
```python
state = load_session()
last_switch = state['metadata']['last_account_switch']
# Example: "2025-10-01T12:30:00"
```

## Security Considerations

- **Session state committed to git** - Full history tracked
- **No sensitive data** - Only task descriptions, file paths, decisions
- **Local file access** - Only accessible on development machine
- **No authentication tokens** - Session state doesn't store credentials

**Recommendation:** Avoid including sensitive information (passwords, API keys) in task descriptions or decisions.

## Performance Impact

- **Disk I/O:** Minimal (~1-2KB JSON file)
- **Memory:** Negligible (<100KB Python module)
- **Git:** ~1KB per commit (session state changes)
- **Network:** Included in regular backup pushes (no extra overhead)

**Conclusion:** Zero noticeable performance impact.

## Future Enhancements

Potential improvements for future versions:

1. **Multi-project support** - Track sessions across multiple repositories
2. **Session branching** - Support multiple parallel work streams
3. **Session replay** - Reconstruct full session history from git
4. **Web dashboard** - Visual session state monitoring
5. **Slack/Discord notifications** - Alert when session is ready to continue
6. **Voice handoff** - Audio summary of session state
7. **AI-powered summaries** - Automatic session highlight generation

## Related Documentation

- [Automated Backups](claude-backup.md) - Git backup system documentation
- [CLAUDE.md](CLAUDE.md) - Full project instructions for Claude
- [README.md](../README.md) - Project overview and quick start

---

**Last Updated:** 2025-10-01
**Version:** 1.0
**Author:** Claude Code Team
**License:** MIT
