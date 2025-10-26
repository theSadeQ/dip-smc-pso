# Session Continuity & Automated Backup - Quick Reference

## 🚀 One-Time Setup

### 1. Register Task Scheduler (Windows)
```batch
# Run once to enable automated backups every 1 minute
.dev_tools\register-task-scheduler.bat
```

### 2. Verify Setup
```bash
# Check Task Scheduler registration
schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST

# Test session continuity system
python scripts/test_session_continuity.py
```

---

## 📋 Daily Usage

### Manual Checkpoint (Force Backup Now)
```powershell
# From repository root
powershell -NoProfile -ExecutionPolicy Bypass -File .\.dev_tools\claude-backup.ps1 -Checkpoint
```

### Check Backup Logs
```powershell
# View recent backups
Get-Content .\.dev_tools\backup\backup.log -Tail 20

# Search for errors
Select-String -Path .\.dev_tools\backup\backup.log -Pattern "ERROR"
```

### Session Continuity (Zero-Effort Account Switching)

**When hitting token limit:**
1. No action needed - session state automatically saved
2. Switch to new Claude Code account
3. Say **"continue"** or **"hi"** - Claude auto-loads context and resumes work

**Manual session inspection:**
```python
# Check current session state
python -c "
import sys
sys.path.insert(0, '.dev_tools')
from session_manager import get_session_summary
print(get_session_summary())
"
```

---

## 🔧 Common Commands

### Task Scheduler Management
```batch
# Run backup immediately (test)
schtasks /Run /TN "ClaudeCode-AutoBackup"

# Check status
schtasks /Query /TN "ClaudeCode-AutoBackup"

# Disable automatic backups
schtasks /Change /TN "ClaudeCode-AutoBackup" /DISABLE

# Enable automatic backups
schtasks /Change /TN "ClaudeCode-AutoBackup" /ENABLE

# Unregister (remove completely)
schtasks /Delete /TN "ClaudeCode-AutoBackup" /F
```

### Git History Review
```bash
# View recent auto-backup commits
git log --oneline --grep="Auto-backup" -10

# View all changes from last manual commit
git log --oneline --since="1 hour ago"

# Compare current state with last manual commit
git diff HEAD~10  # Adjust number based on backup frequency
```

---

## 🛠️ Troubleshooting

### Backup Not Running Automatically

**Check Task Scheduler status:**
```batch
schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST
```

**Common fixes:**
1. Re-register task: `.dev_tools\register-task-scheduler.bat`
2. Check PowerShell execution policy: `Get-ExecutionPolicy`
3. Verify script exists: `ls .dev_tools\claude-backup.ps1`

### Git Authentication Errors

**Configure credential helper:**
```bash
# Windows (recommended)
git config --global credential.helper manager-core

# Test authentication
git push origin main --dry-run
```

**Use Personal Access Token:**
1. Generate PAT: https://github.com/settings/tokens (repo scope)
2. Store credentials:
   ```bash
   git config --global credential.helper store
   git push  # Enter PAT when prompted
   ```

### Session State Issues

**Reset session state:**
```python
python -c "
import sys
sys.path.insert(0, '.dev_tools')
from session_manager import get_default_state, save_session
save_session(get_default_state())
print('Session state reset to defaults')
"
```

**Validate session state:**
```bash
python scripts/test_session_continuity.py
```

---

## 📊 System Health Checks

### Backup System Health
```bash
# 1. Check recent backups in git log
git log --oneline --grep="Auto-backup" -5

# 2. Verify Task Scheduler is running
schtasks /Query /TN "ClaudeCode-AutoBackup" | findstr "Ready Running"

# 3. Check backup log for errors
Select-String -Path .\.dev_tools\backup\backup.log -Pattern "ERROR" -Tail 20
```

### Session Continuity Health
```bash
# Run validation suite
python scripts/test_session_continuity.py

# Check session age
python -c "
import sys
sys.path.insert(0, '.dev_tools')
from session_manager import load_session
from datetime import datetime
state = load_session()
print(f\"Last updated: {state['last_updated']}\")
print(f\"Status: {state['status']}\")
"
```

---

## 🎯 Best Practices

### 1. Let Automatic Backups Work
- Don't manually commit too frequently (Task Scheduler handles it)
- Use manual checkpoints only for critical milestones
- Review auto-backup commits periodically to ensure quality

### 2. Session Continuity Tips
- Always say **"continue"** when resuming in new account (triggers auto-load)
- If context missing, check `.dev_tools/session_state.json` exists
- Update important decisions: Use `add_decision()` in session_manager

### 3. Git History Management
- Auto-backup commits are intentionally frequent (1 min intervals)
- Squash backup commits before merging if needed:
  ```bash
  git rebase -i HEAD~50  # Squash last 50 auto-backups
  ```
- Keep manual commits for feature milestones separate

---

## 📚 Additional Resources

- **Full Documentation**: `docs/claude-backup.md`
- **Session Manager API**: `.dev_tools/session_manager.py`
- **Backup Script**: `.dev_tools/claude-backup.ps1`
- **Project Guidelines**: `CLAUDE.md` (Section 3: Session Continuity)

---

## 💡 Quick Tips

| Scenario | Command |
|----------|---------|
| Force backup now | `powershell .dev_tools\claude-backup.ps1 -Checkpoint` |
| View recent backups | `git log --oneline --grep="Auto-backup" -10` |
| Check backup status | `schtasks /Query /TN "ClaudeCode-AutoBackup"` |
| Test session system | `python scripts/test_session_continuity.py` |
| Resume session | Say **"continue"** in new Claude Code account |
| View session state | `python -c "from session_manager import get_session_summary; print(get_session_summary())"` |

---

**Last Updated**: 2025-10-01
**System Version**: 1.0
**Status**: ✅ Production Ready
