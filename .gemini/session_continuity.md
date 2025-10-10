# Session Continuity System (Zero-Effort Account Switching)

## Overview

When token limits are reached, users can switch Gemini accounts with **zero manual handoff effort**. The system automatically maintains session state and resumes work seamlessly.

**User Experience:**
1. Account A hits token limit
2. User switches to Account B
3. User says: "continue" or "hi" or anything
4. Gemini auto-loads context and resumes immediately

## Auto-Detection Protocol (MANDATORY)

On the **first message** of any new session, Gemini MUST:

1. **Check for session state**: Read `.dev_tools/session_state.json`
2. **Evaluate recency**: If file exists and `last_updated` < 24 hours ago:
   - Auto-load session context
   - Display brief summary: "Continuing from previous session: [task summary]"
   - Show: current task, phase, completed/pending todos
   - Resume work immediately without asking for confirmation
3. **Fresh session**: If file is old (>24h) or doesn't exist:
   - Start fresh session
   - Create new session state file

**Detection Code Pattern:**
```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / ".dev_tools"))

from session_manager import has_recent_session, get_session_summary, load_session

if has_recent_session():
    print(get_session_summary())
    state = load_session()
    # Resume work based on state['context'] and state['next_actions']
```

## Session State Maintenance (MANDATORY)

Throughout **every session**, Gemini MUST update `.dev_tools/session_state.json` after:

1. **Completing any todo item**
   ```python
   from session_manager import add_completed_todo
   add_completed_todo("Create PowerShell backup script")
   ```

2. **Making important decisions**
   ```python
   from session_manager import add_decision
   add_decision("Task Scheduler frequency: 1 minute")
   ```

3. **Starting new tasks or changing phases**
   ```python
   from session_manager import update_session_context
   update_session_context(
       current_task="Implementing feature X",
       phase="testing",
       last_commit="abc1234"
   )
   ```

4. **Modifying significant files**
   - Update `files_modified` list in session state

5. **Identifying next actions**
   ```python
   from session_manager import add_next_action
   add_next_action("Register Task Scheduler job")
   ```

## Token Limit Protocol

When approaching token limit (automatically detected or explicit):

1. **Mark token limit approaching**
   ```python
   from session_manager import mark_token_limit_approaching, finalize_session
   mark_token_limit_approaching()
   finalize_session("Completed automated backup system implementation")
   ```

2. **Ensure session state is comprehensive**
   - All todos updated (completed/in_progress/pending)
   - All decisions recorded
   - Next actions clearly specified
   - Important context preserved

3. **Commit session state**
   - Session state is automatically included in backup commits (every 1 minute)
   - No manual git operations required

4. **User switches accounts** - No manual prompt writing needed!

## Session State File Structure

**Location:** `.dev_tools/session_state.json`

**Schema:**
```json
{
  "session_id": "session_20251001_104700",
  "last_updated": "2025-10-01T10:47:00",
  "account": "account_1",
  "token_limit_approaching": false,
  "status": "active",
  "context": {
    "current_task": "Current work description",
    "phase": "implementation|testing|documentation|completed",
    "last_commit": "abc1234",
    "branch": "main",
    "working_directory": "D:\\Projects\\main"
  },
  "todos": {
    "completed": ["Task 1", "Task 2"],
    "in_progress": ["Task 3"],
    "pending": ["Task 4", "Task 5"]
  },
  "decisions": [
    "Important decision 1",
    "Important decision 2"
  ],
  "next_actions": [
    "Next step 1",
    "Next step 2"
  ],
  "files_modified": [
    "file1.py",
    "file2.md"
  ],
  "important_context": {
    "key": "value"
  }
}
```

## Integration with Automated Backups

- Session state is **automatically committed** every 1 minute via Task Scheduler
- Backup script (`.dev_tools/gemini-backup.ps1`) includes session_state.json
- No manual session state commits required
- Git history provides full session audit trail

## Python Helper: session_manager.py

**Location:** `.dev_tools/session_manager.py`

**Key Functions:**
```python
# example-metadata:
# runnable: false

# Check for continuable session
has_recent_session(threshold_hours=24) -> bool

# Load session state
load_session() -> Optional[Dict]

# Get human-readable summary
get_session_summary() -> str

# Update session context
update_session_context(**kwargs) -> bool

# Track progress
add_completed_todo(todo: str) -> bool
add_decision(decision: str) -> bool
add_next_action(action: str) -> bool

# Prepare for handoff
mark_token_limit_approaching() -> bool
finalize_session(summary: str) -> bool
```

## Benefits

[OK] **Zero manual handoff** - No prompt writing when switching accounts
[OK] **Automatic resume** - Gemini knows exactly where you left off
[OK] **Audit trail** - Full session history in git commits
[OK] **Reliability** - JSON schema with validation
[OK] **Transparency** - Human-readable state file
[OK] **Efficiency** - Resume work in seconds, not minutes

## Example Usage

**Session 1 (Account A - hitting token limit):**
```python
# Gemini automatically throughout session:
update_session_context(current_task="Implementing backup system", phase="testing")
add_completed_todo("Create PowerShell script")
add_completed_todo("Write documentation")
add_next_action("User needs to register Task Scheduler")

# As token limit approaches:
mark_token_limit_approaching()
finalize_session("Backup system implementation complete")
```

**Session 2 (Account B - fresh start):**
```
User: "continue"

Gemini: [Auto-checks session_state.json]
"Continuing from previous session (2 hours ago):
Task: Implementing backup system
Phase: testing
Last commit: c8c9c64

Completed: 5 items
In progress: 0 items
Pending: 2 items

Next actions:
1. User needs to register Task Scheduler
2. Run smoke test to verify functionality

Let me check the current status..."

[Gemini immediately resumes work based on state]
```
