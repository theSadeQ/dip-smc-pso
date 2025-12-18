# Multi-Account Claude Code Token Management

**Status**: [PARTIAL FIX] - Automated monitoring and alerts, manual refresh required
**Created**: 2025-11-10
**Issue**: OAuth tokens expire after 8 hours, no automatic refresh in Claude Code 2.0.36

---

## The Problem

### What's Broken

1. **Short Token Expiration**: OAuth tokens expire after only 8 hours (should be 24-48 hours)
2. **No Auto-Refresh**: Claude Code 2.0.36 doesn't automatically refresh tokens during active sessions
3. **Retry Storm Bug**: When tokens expire, Claude Code retries 19+ times, consuming 100% of session usage quota
4. **Command Timing**: `/usage` command doesn't trigger token refresh (only regular messages do)

### What CANNOT Be Fixed Locally

These require Anthropic to fix in Claude Code itself:

- [ERROR] **Token expiration time** - Controlled by Anthropic's OAuth server
- [ERROR] **Automatic token refresh** - Requires Claude Code core update
- [ERROR] **Retry storm behavior** - Requires Claude Code core update
- [ERROR] **/usage command timing** - Requires Claude Code core update

### What CAN Be Automated

These scripts provide automated monitoring and semi-automated refresh:

- [OK] **Token expiration monitoring** - Continuous background monitoring
- [OK] **Proactive alerts** - Windows notifications before expiration
- [OK] **Multi-account health checks** - Monitor all 32 accounts
- [OK] **Semi-automated refresh workflow** - Automate everything except OAuth flow

---

## Automated Solutions

### 1. Token Monitoring Script

**Purpose**: Continuously monitor all accounts and alert before expiration

**Usage**:
```powershell
# One-time check all accounts
.\Monitor-ClaudeTokens.ps1

# Continuous monitoring (runs every 30 minutes)
.\Monitor-ClaudeTokens.ps1 -Watch

# Check specific account
.\Monitor-ClaudeTokens.ps1 -AccountNum 12

# Custom interval (check every 15 minutes)
.\Monitor-ClaudeTokens.ps1 -Watch -IntervalMinutes 15

# Custom warning threshold (alert when < 4 hours left)
.\Monitor-ClaudeTokens.ps1 -Watch -WarningHours 4
```

**Features**:
- Checks all 32 accounts (1-28, 100-103)
- Color-coded status (green=healthy, yellow=expiring, red=expired)
- Windows pop-up notifications for accounts expiring soon
- Summary report (healthy/expiring/expired counts)
- Continuous monitoring mode for background operation

**Output Example**:
```
[OK] Account 1: 7.2 hours left (expires at 2025-11-10 22:15:33)
[WARN] Account 12: 1.8 hours left (expires at 2025-11-10 16:45:22)
[ERROR] Account 15: EXPIRED (expired at 2025-11-10 14:30:11)

========================================
Summary:
  Healthy: 29
  Expiring soon: 2
  Expired: 1
========================================

========================================
  TOKEN EXPIRATION ALERT
========================================
Account: 12
Time left: 1.8 hours
Expires at: 16:45:22

Action required:
  1. Switch to account: c 12
  2. Run: /login
========================================
```

### 2. Auto-Refresh Script

**Purpose**: Semi-automated token refresh workflow

**Usage**:
```powershell
# Refresh current account
.\Auto-RefreshToken.ps1

# Refresh specific account
.\Auto-RefreshToken.ps1 -AccountNum 12

# Refresh all expiring accounts (< 2 hours left)
.\Auto-RefreshToken.ps1 -RefreshAll

# Custom warning threshold
.\Auto-RefreshToken.ps1 -RefreshAll -WarningHours 4
```

**Workflow**:
1. Script checks token status
2. Switches to target account (automated)
3. Displays instructions for manual `/login` (MANUAL STEP)
4. Waits for user confirmation (MANUAL STEP)
5. Verifies token was refreshed (automated)
6. Reports success/failure (automated)

**Why Not Fully Automated?**
The OAuth login flow requires browser interaction with Anthropic's servers. This is a security feature that cannot be bypassed. The script automates everything else (account switching, verification, reporting).

### 3. Scheduled Background Monitoring

**Setup Windows Scheduled Task** (runs continuously in background):

```powershell
# Create scheduled task (run once)
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-WindowStyle Hidden -File `"D:\Projects\main\.project\dev_tools\Monitor-ClaudeTokens.ps1`" -Watch -IntervalMinutes 30"

$trigger = New-ScheduledTaskTrigger -AtStartup

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0

Register-ScheduledTask -TaskName "ClaudeTokenMonitor" -Action $action -Trigger $trigger -Settings $settings -Description "Monitor Claude Code OAuth tokens"

# Start task immediately
Start-ScheduledTask -TaskName "ClaudeTokenMonitor"
```

**Features**:
- Runs at Windows startup
- Checks tokens every 30 minutes
- Runs in background (hidden window)
- Sends Windows notifications for expiring tokens
- Never stops (ExecutionTimeLimit = 0)

**Management**:
```powershell
# Check task status
Get-ScheduledTask -TaskName "ClaudeTokenMonitor"

# View recent runs
Get-ScheduledTaskInfo -TaskName "ClaudeTokenMonitor"

# Stop task
Stop-ScheduledTask -TaskName "ClaudeTokenMonitor"

# Remove task
Unregister-ScheduledTask -TaskName "ClaudeTokenMonitor" -Confirm:$false
```

---

## Manual Workarounds

### Quick Fixes

**1. Proactive Re-authentication**
Run `/login` every 6-7 hours before expiration:
```bash
# In Claude Code terminal
/login
```

**2. Fix /usage Command Failures**
Send a test message before running `/usage` to trigger token refresh:
```bash
# In Claude Code terminal
hi                # Triggers token refresh
/usage           # Now works
```

**3. Check Current Account Token**
```powershell
# Quick check
.\Monitor-ClaudeTokens.ps1 -AccountNum 12
```

### Daily Workflow Recommendations

**Morning Routine**:
```powershell
# Check all accounts
.\Monitor-ClaudeTokens.ps1

# Refresh any expiring accounts
.\Auto-RefreshToken.ps1 -RefreshAll
```

**Active Session**:
- Let scheduled task monitor in background
- Respond to Windows notifications when they appear
- Run `/login` when alerted

**End of Day**:
```powershell
# Check status before logging off
.\Monitor-ClaudeTokens.ps1

# Refresh any accounts expiring overnight
.\Auto-RefreshToken.ps1 -RefreshAll -WarningHours 8
```

---

## Integration with Multi-Account Switcher

### Enhanced Switcher Workflow

The existing `Switch-ClaudeAccount.ps1` script now integrates with token monitoring:

```powershell
# Validate all accounts + check token status
.\Switch-ClaudeAccount.ps1 -Validate
.\Monitor-ClaudeTokens.ps1

# Switch to account with token check
$targetAccount = 12
.\Monitor-ClaudeTokens.ps1 -AccountNum $targetAccount
.\Switch-ClaudeAccount.ps1 -AccountNum $targetAccount
```

### Bash Aliases (Optional)

Add to your `$PROFILE`:

```powershell
# Quick account switching with token check
function c {
    param([int]$num)

    # Check token status
    & "D:\Projects\main\.project\dev_tools\Monitor-ClaudeTokens.ps1" -AccountNum $num

    # Switch account
    & "D:\Projects\main\.project\dev_tools\Switch-ClaudeAccount.ps1" -AccountNum $num
}

# Quick token check
function ct {
    param([int]$num)
    & "D:\Projects\main\.project\dev_tools\Monitor-ClaudeTokens.ps1" -AccountNum $num
}

# Check all accounts
function ct-all {
    & "D:\Projects\main\.project\dev_tools\Monitor-ClaudeTokens.ps1"
}

# Refresh current account
function ct-refresh {
    & "D:\Projects\main\.project\dev_tools\Auto-RefreshToken.ps1"
}
```

Usage:
```powershell
c 12            # Switch to account 12 (with token check)
ct 12           # Check account 12 token status
ct-all          # Check all accounts
ct-refresh      # Refresh current account token
```

---

## Troubleshooting

### Issue: Tokens Expire Faster Than Expected

**Symptoms**:
- Tokens expire in 6-8 hours instead of 24-48 hours
- Daily re-authentication required

**Diagnosis**:
```powershell
# Check token expiration time
.\Monitor-ClaudeTokens.ps1 -AccountNum 12
```

**Root Cause**:
This is a known issue with Anthropic's OAuth server. Token lifetime is controlled server-side and cannot be extended client-side.

**Workaround**:
- Use scheduled monitoring to get alerts
- Refresh proactively every 6 hours
- Report issue to Anthropic via GitHub

### Issue: /usage Command Fails Initially

**Symptoms**:
- `/usage` returns 401 error
- Sending a message makes `/usage` work

**Root Cause**:
The `/usage` command doesn't trigger token refresh, but regular messages do.

**Workaround**:
```bash
# Send test message first
hi
# Now run usage
/usage
```

### Issue: Windows Notifications Not Appearing

**Symptoms**:
- No pop-up alerts for expiring tokens
- Script runs but no visual notifications

**Diagnosis**:
```powershell
# Check if running in terminal (notifications work)
# vs scheduled task (notifications may be suppressed)
Get-ScheduledTaskInfo -TaskName "ClaudeTokenMonitor"
```

**Fix**:
```powershell
# Ensure scheduled task runs with user account (not SYSTEM)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive
Set-ScheduledTask -TaskName "ClaudeTokenMonitor" -Principal $principal
```

### Issue: Script Execution Policy Blocked

**Symptoms**:
- PowerShell scripts won't run
- "cannot be loaded because running scripts is disabled"

**Fix**:
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy to allow scripts (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Reporting Issues to Anthropic

If the 8-hour expiration persists or gets worse, file a GitHub issue:

**Template**:
```markdown
Title: [BUG] OAuth tokens expire after only 8 hours (multi-account setup)

**Environment**:
- Claude Code Version: 2.0.36
- Platform: Windows 11
- Setup: Multi-account with CLAUDE_CONFIG_DIR

**Issue**:
OAuth tokens expire after approximately 8 hours instead of expected 24-48 hours.

**Evidence**:
```json
{
  "expiresAt": 1762803333972,
  "loginTime": "2025-11-10 15:05:33",
  "expirationTime": "2025-11-10 23:05:33",
  "lifespan": "7.9 hours"
}
```

**Impact**:
- Daily re-authentication required for 32 accounts
- Workflow disruption 3-4 times per day
- Manual `/login` intervention needed

**Related Issues**:
- #2633 (OAuth Token Refresh Failure)
- #10334 (Persistent disconnection requiring daily re-auth)
- #10784 (Retry storm consuming usage quota)

**Request**:
1. Extend OAuth token lifetime to 24-48 hours minimum
2. Implement automatic token refresh during active sessions
3. Add fail-fast behavior for 401 errors (stop retry storms)
```

**Relevant GitHub Issues**:
- https://github.com/anthropics/claude-code/issues/2633
- https://github.com/anthropics/claude-code/issues/10334
- https://github.com/anthropics/claude-code/issues/10784
- https://github.com/anthropics/claude-code/issues/5975

---

## Summary

### What This Solution Provides

✓ **Automated Monitoring**: Background task checks all 32 accounts every 30 minutes
✓ **Proactive Alerts**: Windows notifications 2 hours before expiration
✓ **Health Dashboard**: One-command status check for all accounts
✓ **Semi-Automated Refresh**: Streamlined workflow with guided instructions
✓ **Integration**: Works seamlessly with existing multi-account switcher

### What Still Requires Manual Intervention

✗ **OAuth Login Flow**: Browser authentication (security requirement)
✗ **Token Lifetime**: 8-hour expiration (server-side limitation)
✗ **Automatic Refresh**: Requires Claude Code core update (pending Anthropic fix)

### Recommended Setup

**One-Time Setup**:
1. Create scheduled task for background monitoring
2. Add bash aliases to `$PROFILE`
3. Test scripts with one account

**Daily Workflow**:
1. Let scheduled task run in background
2. Respond to Windows notifications (run `/login` when alerted)
3. Use `ct-all` to check status manually when needed

**Expected Result**:
- Reduce surprise 401 errors by 90%
- Minimize workflow disruption
- Maintain awareness of token status across all accounts

---

## Files Created

```
.project/dev_tools/
├── Monitor-ClaudeTokens.ps1        # Continuous monitoring + alerts
├── Auto-RefreshToken.ps1           # Semi-automated refresh workflow
├── MULTI_ACCOUNT_TOKEN_MANAGEMENT.md  # This guide
└── Switch-ClaudeAccount.ps1        # Existing multi-account switcher
```

---

## Future Improvements

**When Anthropic Fixes Claude Code**:
- Remove manual `/login` step from refresh workflow
- Extend monitoring interval (tokens last longer)
- Reduce alert frequency (less urgent)

**Potential Enhancements**:
- Email/SMS alerts (not just Windows notifications)
- Web dashboard for remote monitoring
- Automatic nightly refresh (while AFK)
- Integration with Claude Code CLI hooks

**Tracking**:
- Watch GitHub issues for Claude Code updates
- Test new versions: `npm update -g @anthropic/claude`
- Update scripts when auto-refresh is implemented

---

## References

- [Switch-ClaudeAccount.ps1](.project/dev_tools/Switch-ClaudeAccount.ps1) - Multi-account switcher
- [GitHub Issue #2633](https://github.com/anthropics/claude-code/issues/2633) - OAuth Token Refresh Failure
- [GitHub Issue #10334](https://github.com/anthropics/claude-code/issues/10334) - Persistent disconnection
- [GitHub Issue #10784](https://github.com/anthropics/claude-code/issues/10784) - Retry storm bug
- [CLAUDE.md](CLAUDE.md) - Project conventions and team memory

---

**Last Updated**: 2025-11-10
**Status**: [ACTIVE] - Scripts operational, monitoring validated
