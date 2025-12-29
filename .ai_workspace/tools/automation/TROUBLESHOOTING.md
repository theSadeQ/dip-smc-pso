# Task Scheduler Troubleshooting Guide

## Current Status: Backup Not Running Automatically

After waiting 60 seconds with pending changes, **no automatic backup occurred**.

**Symptoms:**
- ❌ No backup log created (`.dev_tools/backup/backup.log`)
- ❌ No auto-backup commits in git history
- ❌ Changes remain uncommitted

---

## Diagnostic Steps

### Step 1: Verify Task Registration

```batch
schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST
```

**Expected Output:**
```
TaskName: \ClaudeCode-AutoBackup
Status: Ready
Triggers: At 11:XX every day, starting 2025-10-01, every 1 minute
```

**If task not found:**
- Task was not registered successfully
- **Fix:** Re-run `.dev_tools\register-task-scheduler.bat`

---

### Step 2: Check Task Status

```batch
schtasks /Query /TN "ClaudeCode-AutoBackup" /FO CSV /NH
```

**Look for:**
- Status column should show "Ready" or "Running"
- If "Disabled", enable it:
  ```batch
  schtasks /Change /TN "ClaudeCode-AutoBackup" /ENABLE
  ```

---

### Step 3: Check Last Run Result

```batch
schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST | findstr /C:"Last Result"
```

**Result Codes:**
- `0x0` = Success
- `0x1` = Incorrect function
- `0x41301` = Task is currently running
- Other codes = Error occurred

---

### Step 4: Test Manual Execution

Force the task to run immediately:

```batch
schtasks /Run /TN "ClaudeCode-AutoBackup"
```

Wait 5-10 seconds, then check:

```powershell
# Check if backup log was created
Get-Content .dev_tools\backup\backup.log -Tail 20

# Check for new commits
git log --oneline -5
```

**If manual run works but automatic doesn't:**
- Task Scheduler trigger may be misconfigured
- Check trigger settings:
  ```batch
  schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST | findstr /C:"Schedule"
  ```

**If manual run also fails:**
- Check error in backup log
- Verify PowerShell execution policy
- Check file paths and permissions

---

### Step 5: Check PowerShell Execution Policy

```powershell
Get-ExecutionPolicy
```

**If "Restricted":**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Step 6: Test Backup Script Directly

Run the backup script manually to see detailed output:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File D:\Projects\main\.dev_tools\claude-backup.ps1 -Checkpoint
```

**Expected Output:**
```
[TIMESTAMP] [Info] === Claude Code Auto-Backup Script ===
[TIMESTAMP] [Info] Repository root: D:\Projects\main
[TIMESTAMP] [Info] Remote URL verified: https://github.com/theSadeQ/dip-smc-pso.git
[TIMESTAMP] [Info] Changes detected. Proceeding with backup...
[TIMESTAMP] [Success] Backup completed successfully!
```

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| "Authentication failed" | Git credentials not configured | Run `git config --global credential.helper manager-core` |
| "Not a git repository" | Wrong working directory | Verify path in Task Scheduler |
| "Remote not found" | Incorrect remote URL | Run backup script to auto-fix |
| "Permission denied" | File locked by another process | Close other Git clients |

---

## Quick Diagnostic Script

Run this comprehensive check:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.dev_tools\verify-task-scheduler.ps1
```

This will check all 5 components:
1. Task registration
2. Task status
3. Backup script existence
4. Repository status
5. Backup logs

---

## Common Issues and Fixes

### Issue 1: Task Scheduler Service Not Running

**Check:**
```batch
sc query Schedule
```

**Fix:**
```batch
sc start Schedule
```

### Issue 2: User Account Issues

Task may be registered for different user account.

**Fix:**
```batch
# Delete and re-register with current user
schtasks /Delete /TN "ClaudeCode-AutoBackup" /F
.dev_tools\register-task-scheduler.bat
```

### Issue 3: Path Issues (Spaces in Path)

If repository path contains spaces, Task Scheduler may have issues.

**Fix:** Edit task manually in Task Scheduler GUI:
1. Open Task Scheduler (taskschd.msc)
2. Find "ClaudeCode-AutoBackup"
3. Edit action, ensure path is quoted:
   ```
   "powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "D:\Projects\main\.dev_tools\claude-backup.ps1"
   ```

### Issue 4: Git Authentication Not Configured

**Check:**
```bash
git config --get credential.helper
```

**Fix:**
```bash
git config --global credential.helper manager-core
git push  # Authenticate when prompted
```

---

## Expected Behavior Timeline

**After successful Task Scheduler registration:**

| Time | Expected Event |
|------|----------------|
| T+0s | Task registered, status: Ready |
| T+60s | First trigger fires |
| T+65s | Backup log appears with entries |
| T+70s | Git commit created (if changes present) |
| T+75s | Push to GitHub completes |

**To monitor in real-time:**
```powershell
# Terminal 1: Watch backup log
Get-Content .dev_tools\backup\backup.log -Wait

# Terminal 2: Watch git log
while ($true) { Clear-Host; git log --oneline -10; Start-Sleep -Seconds 5 }
```

---

## Success Indicators

✅ **Backup system is working if:**
1. Backup log exists and shows recent entries
2. "Last Result: 0x0" in Task Scheduler
3. Auto-backup commits appear in git log every ~1 minute (when changes present)
4. "Status: Ready" in Task Scheduler query
5. No error entries in backup log

---

## Getting Help

If none of the above steps work, gather this diagnostic information:

```powershell
# Run all diagnostics and save to file
$output = @"
=== Task Scheduler Status ===
$(schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST 2>&1)

=== PowerShell Execution Policy ===
$(Get-ExecutionPolicy -List)

=== Git Status ===
$(git status)

=== Git Remote ===
$(git remote -v)

=== Backup Script Test ===
$(powershell -NoProfile -ExecutionPolicy Bypass -File .\.dev_tools\claude-backup.ps1 -Checkpoint 2>&1)
"@

$output | Out-File -FilePath "task_scheduler_diagnostics.txt"
Write-Host "Diagnostics saved to: task_scheduler_diagnostics.txt"
```

Share the `task_scheduler_diagnostics.txt` file for troubleshooting assistance.

---

**Last Updated:** 2025-10-01
**Status:** Troubleshooting automated backup system
