# Browser Profile Setup Guide for Fully Automated OAuth

**Status**: [SOLUTION] - Fully automated token refresh using browser profiles
**Created**: 2025-11-10
**Issue**: OAuth tokens expire after 8 hours in Claude Code 2.0.36
**Solution**: Use dedicated browser profiles that stay logged into Anthropic

---

## How It Works

### The Problem
- OAuth tokens expire after 8 hours
- Manual `/login` required every 6-8 hours
- 32 accounts = lots of manual intervention

### The Solution
- Create separate browser profile for each Claude account (1-28, 100-103)
- Each profile stays logged into Anthropic (persistent session)
- When token expires, script opens browser with correct profile
- Browser auto-completes OAuth (already logged in)
- Token refreshed automatically
- Browser closes
- **Result: 95% automated** (only 1 manual step remaining)

---

## Setup Steps (One-Time)

### Step 1: Create Browser Profiles

```powershell
# Run the setup wizard
.\Setup-BrowserProfiles.ps1 -InitialSetup
```

**Wizard will ask:**
1. **Choose browser**: Chrome (recommended), Edge, or Firefox
2. **Choose accounts**: All 32 accounts, specific accounts, or only expired
3. **Creates profiles**: One profile per account

**Output:**
- Browser profiles created in browser's profile directory
- Configuration saved to `browser_profiles_config.json`
- Ready for authentication

### Step 2: Authenticate Each Profile

This is the **one-time manual step**. You need to log each browser profile into Anthropic.

#### Option A: Batch Authentication (Recommended)

```powershell
# Authenticate all profiles in sequence
.\Authenticate-AllProfiles.ps1

# Or only expired accounts
.\Authenticate-AllProfiles.ps1 -OnlyExpired

# Or specific accounts
.\Authenticate-AllProfiles.ps1 -AccountNums 1,5,12,20
```

**Process:**
1. Script opens browser with profile for account 1
2. You log in to claude.com
3. Check "Stay logged in"
4. Close browser
5. Press Enter
6. Repeat for next account

**Time estimate:** ~2 minutes per account = ~60 minutes for 32 accounts

#### Option B: Manual Authentication

```powershell
# Open profile for specific account
.\Open-ProfileForAuth.ps1 -AccountNum 12
```

Then:
1. Log in to claude.com
2. Check "Stay logged in"
3. Close browser

### Step 3: Validate Setup

```powershell
# Verify all profiles are configured correctly
.\Setup-BrowserProfiles.ps1 -ValidateProfiles
```

**Output:**
```
[OK] Account 1: Profile active (156 files)
[OK] Account 5: Profile active (142 files)
[OK] Account 12: Profile active (189 files)
...
========================================
Summary:
  Valid profiles: 32
  Invalid profiles: 0
========================================
```

---

## Usage (Automated Token Refresh)

### Refresh Single Account

```powershell
# Refresh current account
.\Auto-RefreshToken-Browser.ps1

# Refresh specific account
.\Auto-RefreshToken-Browser.ps1 -AccountNum 12
```

**Process:**
1. Script detects token expiring/expired
2. Switches to target account
3. Opens browser with correct profile
4. **(MANUAL)** You run `claude` and type `/login` in new terminal
5. Browser auto-completes OAuth (no login needed!)
6. Token refreshed
7. Browser closes

**Manual step:** Only running `claude` + `/login` command (can't be automated yet)

### Refresh All Expiring Accounts

```powershell
# Check and refresh all accounts with < 2 hours left
.\Auto-RefreshToken-Browser.ps1 -RefreshAll

# Custom threshold (< 4 hours)
.\Auto-RefreshToken-Browser.ps1 -RefreshAll -WarningHours 4
```

### Continuous Monitoring Mode

```powershell
# Monitor and auto-refresh every 30 minutes
.\Auto-RefreshToken-Browser.ps1 -Watch

# Custom interval (every 15 minutes)
.\Auto-RefreshToken-Browser.ps1 -Watch -IntervalMinutes 15
```

**This runs forever:**
- Checks all accounts every N minutes
- Automatically refreshes expiring tokens
- Only requires manual `/login` command when token is expiring

---

## Scheduled Automation (Windows Task)

### Create Scheduled Task for Auto-Refresh

```powershell
# Run token refresh every 30 minutes
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File `"D:\Projects\main\.project\dev_tools\Auto-RefreshToken-Browser.ps1`" -RefreshAll"

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "ClaudeAutoRefresh" -Action $action -Trigger $trigger -Settings $settings -Description "Auto-refresh Claude Code OAuth tokens"

# Start task
Start-ScheduledTask -TaskName "ClaudeAutoRefresh"
```

**Management:**
```powershell
# Check status
Get-ScheduledTask -TaskName "ClaudeAutoRefresh"

# Stop task
Stop-ScheduledTask -TaskName "ClaudeAutoRefresh"

# Remove task
Unregister-ScheduledTask -TaskName "ClaudeAutoRefresh" -Confirm:$false
```

---

## How Automated Is This?

### Before Browser Profiles
- [MANUAL] Run `/login` every 6-8 hours per account
- [MANUAL] Complete OAuth in browser (login, password, 2FA)
- [MANUAL] Switch between accounts
- **Time:** 2-3 minutes per refresh × 4 times/day × 32 accounts = **~4 hours/day**

### After Browser Profiles
- [AUTO] Token expiration detected
- [AUTO] Browser opens with correct profile
- [MANUAL] Run `claude` + `/login` (10 seconds)
- [AUTO] Browser auto-completes OAuth (no login needed!)
- [AUTO] Token refreshed
- [AUTO] Browser closes
- **Time:** 10 seconds per refresh × 4 times/day × 32 accounts = **~20 minutes/day**

**Time saved: 95%** (3h 40m per day)

---

## Why One Manual Step Remains

The `/login` command in Claude Code triggers OAuth programmatically and generates a unique callback URL. We cannot:

1. **Automate `/login` command** - Requires interactive terminal session
2. **Predict OAuth URL** - Generated dynamically by Claude Code
3. **Bypass OAuth flow** - Security requirement

**Best we can do:** Automate everything except the `/login` trigger.

**Future improvement:** If Claude Code adds:
- Command-line flag for headless OAuth
- HTTP API for token refresh
- Auto-refresh on token expiration

Then we can achieve 100% automation.

---

## Maintenance

### Check Token Status

```powershell
# Check all accounts
.\Monitor-ClaudeTokens.ps1

# Check specific account
.\Monitor-ClaudeTokens.ps1 -AccountNum 12

# Continuous monitoring
.\Monitor-ClaudeTokens.ps1 -Watch
```

### Re-authenticate a Profile

If a browser profile loses its Anthropic session:

```powershell
# Open profile for re-authentication
.\Open-ProfileForAuth.ps1 -AccountNum 12
```

Then log in to claude.com again.

### Add New Account

```powershell
# Create profile for new account
.\Setup-BrowserProfiles.ps1 -AccountNum 50 -Browser Chrome

# Authenticate it
.\Open-ProfileForAuth.ps1 -AccountNum 50
```

---

## Troubleshooting

### Issue: Browser Opens But OAuth Doesn't Complete

**Symptom:** Browser opens, but token doesn't refresh

**Cause:** Browser profile not logged into Anthropic

**Fix:**
```powershell
.\Open-ProfileForAuth.ps1 -AccountNum 12
# Log in to claude.com
# Check "Stay logged in"
```

### Issue: "Profile Not Found" Error

**Symptom:** Script says profile doesn't exist

**Cause:** Browser profile not created

**Fix:**
```powershell
.\Setup-BrowserProfiles.ps1 -AccountNum 12
.\Open-ProfileForAuth.ps1 -AccountNum 12
```

### Issue: OAuth Asks for Login Every Time

**Symptom:** Browser keeps asking for login despite "Stay logged in"

**Cause:** Browser profile not persisting cookies

**Fix:**
1. Check browser privacy settings
2. Ensure cookies are allowed for claude.com
3. Disable "Clear cookies on exit"
4. Try different browser (Chrome vs Edge)

### Issue: Multiple Browser Windows Open

**Symptom:** Each refresh opens new browser window

**Cause:** Browser instances not closing properly

**Fix:**
```powershell
# Kill all Chrome/Edge processes
Stop-Process -Name chrome -Force
Stop-Process -Name msedge -Force

# Then retry
.\Auto-RefreshToken-Browser.ps1 -AccountNum 12
```

---

## Security Considerations

### Browser Profiles Are Isolated

- Each profile is independent
- Separate cookies, history, cache
- Logging into one doesn't affect others

### Session Persistence

- Browser profiles persist login across reboots
- Protected by Windows user account
- Encryption same as regular browser usage

### Risk Assessment

**Risks:**
- If someone accesses your Windows account, they can use profiles
- Physical access to PC = access to all Claude accounts

**Mitigations:**
- Use Windows account password/PIN
- Enable BitLocker disk encryption
- Lock PC when away (Win+L)
- Consider using Windows Hello biometrics

**Comparison:**
- Same risk as staying logged into browser normally
- More secure than storing API keys in plain text
- Less secure than requiring login every time (but that's impractical)

---

## File Structure

```
.project/dev_tools/
├── Setup-BrowserProfiles.ps1           # Create and manage profiles
├── Authenticate-AllProfiles.ps1        # Batch authenticate profiles
├── Open-ProfileForAuth.ps1             # Open profile for auth
├── Auto-RefreshToken-Browser.ps1       # Automated token refresh
├── Monitor-ClaudeTokens.ps1            # Token monitoring
├── browser_profiles_config.json        # Configuration (auto-generated)
└── BROWSER_PROFILE_SETUP_GUIDE.md      # This guide
```

---

## Quick Start (TL;DR)

```powershell
# 1. Create profiles
.\Setup-BrowserProfiles.ps1 -InitialSetup

# 2. Authenticate (one-time, ~60 minutes for 32 accounts)
.\Authenticate-AllProfiles.ps1

# 3. Validate
.\Setup-BrowserProfiles.ps1 -ValidateProfiles

# 4. Start automated monitoring
.\Auto-RefreshToken-Browser.ps1 -Watch
```

From now on: When script alerts you, just run `claude` + `/login` and browser auto-completes!

---

## Future Enhancements

**When Claude Code 2.0.37+ is released:**
- Check if token lifetime is fixed (back to 24-48 hours)
- Check if auto-refresh is implemented
- Reduce monitoring frequency if tokens last longer

**Potential improvements:**
- PowerShell module for easier management
- GUI dashboard for token status
- Email/SMS alerts for expiring tokens
- Integration with Windows Action Center
- Automatic `/login` trigger (if Claude Code adds support)

---

## Support

**Issues with scripts:**
- Check PowerShell execution policy: `Get-ExecutionPolicy`
- Run as Administrator if needed
- Ensure browser is installed and updated

**Issues with Claude Code:**
- Monitor: https://github.com/anthropics/claude-code/issues/11242
- Report if token lifetime doesn't improve in 2.0.37

**Issues with multi-account setup:**
- Verify CLAUDE_CONFIG_DIR is set correctly
- Check `.credentials.json` exists in each account directory
- Run account validation: `.\Switch-ClaudeAccount.ps1 -Validate`

---

**Last Updated:** 2025-11-10
**Status:** [ACTIVE] - Ready for production use
**Automation Level:** 95% (only `/login` command remains manual)
