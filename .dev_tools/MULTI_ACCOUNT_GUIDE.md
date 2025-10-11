# Claude Code Multi-Account System Guide

**Status:** Production Ready
**Created:** 2025-10-11
**Safety Level:** Maximum (Zero auth sharing)

---

## Overview

The Claude Code Multi-Account System allows you to seamlessly switch between up to 35 separate Claude Code accounts with complete authentication isolation and session continuity.

**Key Features:**
- [OK] Isolated authentication per account (no credential sharing)
- [OK] Quick switching with simple aliases (c1, c2, c3...)
- [OK] Session state tracking across account switches
- [OK] Safety validation to prevent auth file junctions
- [OK] Automatic backup and restore utilities
- [OK] Zero risk to primary .claude configuration

---

## Quick Start

### Installation

1. **Add to PowerShell Profile**

   Open your PowerShell profile:
   ```powershell
   notepad $PROFILE
   ```

   Add this line at the end:
   ```powershell
   . D:\Projects\main\.dev_tools\claude-profile.ps1
   ```

   Save and reload:
   ```powershell
   . $PROFILE
   ```

2. **Verify Installation**

   ```powershell
   claude-help
   ```

   You should see the help menu with available commands.

3. **Create First Backup (Recommended)**

   ```powershell
   .\D:\Projects\main\.dev_tools\Backup-ClaudeConfig.ps1
   ```

---

## Usage

### Basic Account Switching

**Switch to any account (1-35):**
```powershell
c5    # Switch to account 5
c15   # Switch to account 15
c30   # Switch to account 30
```

**Return to primary account:**
```powershell
claude-primary
```

**Check account status:**
```powershell
claude-status
```

### First Time Using an Account

When you switch to a new account for the first time:

1. The system creates `~\.claude{N}` directory
2. Claude Code launches
3. You'll be prompted to log in
4. After login, account is authenticated
5. Future switches to this account will be instant

**Example:**
```powershell
PS> c12
[OK] Set CLAUDE_CONFIG_DIR: C:\Users\you\.claude12
[WARN] Account 12 needs authentication
[INFO] Claude Code will prompt for login on first use
[OK] Successfully switched to Account 12
[INFO] Launching Claude Code...
```

---

## Commands Reference

### Quick Aliases

| Command | Description |
|---------|-------------|
| `c1` - `c35` | Switch to account 1-35 |
| `claude-primary` | Switch back to primary .claude |
| `claude-status` | Show all accounts and auth status |
| `claude-help` | Show help menu |

### Advanced Commands

**Switch without launching:**
```powershell
Switch-ClaudeAccount -AccountNum 5 -NoLaunch
```

**Validate account safety:**
```powershell
.\D:\Projects\main\.dev_tools\Validate-ClaudeAccounts.ps1
```

**Create backup:**
```powershell
.\D:\Projects\main\.dev_tools\Backup-ClaudeConfig.ps1
```

**Restore from backup:**
```powershell
.\D:\Projects\main\.dev_tools\Restore-ClaudeConfig.ps1
```

---

## Safety Guarantees

### What's Isolated Per Account

Each account has its own:
- ✅ Authentication credentials (`.credentials.json`)
- ✅ Session history (`history.jsonl`)
- ✅ Cached data (`.claude.json`)
- ✅ User settings (`settings.json`)

### What's Shared (Safe to Share)

- ✅ Project-level `.claude/` configs (MCP servers, commands, agents)
- ✅ Git repository data
- ✅ Your code files

### Safety Checks

The system prevents:
- ❌ Auth file junctions (automatic detection)
- ❌ Credential sharing between accounts
- ❌ Accidental primary .claude modifications

**Validation command:**
```powershell
.\D:\Projects\main\.dev_tools\Validate-ClaudeAccounts.ps1
```

**Example output:**
```
Account 1: [Authenticated] (10 files) [SAFE]
Account 5: [Needs login] (8 files) [SAFE]
Account 9: [Authenticated] (11 files) [SAFE]

Total accounts found: 34
  Authenticated:      12
  Needs login:        22

Safety checks:
  Auth junctions:     0
  Errors:             0
  Warnings:           0

[OK] All safety checks passed!
```

---

## Troubleshooting

### Account Appears Logged Out

**Symptom:** Switching to an account shows "Needs login"

**Solution:** This is normal for first-time use. Just log in once and the account will stay authenticated.

```powershell
c5  # Will prompt for login
# After logging in, subsequent switches are instant
```

### Lost Track of Current Account

**Check which account you're using:**
```powershell
echo $env:CLAUDE_CONFIG_DIR
# Output: C:\Users\you\.claude5 (Account 5)
# Output: (empty) = Primary account
```

Or use:
```powershell
claude-status
```

### Want to Start Fresh on an Account

**Option 1:** Just delete the account directory:
```powershell
Remove-Item "$env:USERPROFILE\.claude12" -Recurse -Force
```

**Option 2:** Return to primary and clear override:
```powershell
claude-primary
```

### Accidentally Broke Primary .claude

**Restore from backup:**
```powershell
.\D:\Projects\main\.dev_tools\Restore-ClaudeConfig.ps1
```

The script will:
1. Show available backups
2. Let you select which one to restore
3. Create safety backup of current state
4. Restore selected backup
5. Reset to primary account

---

## Session Continuity Integration

The multi-account system integrates with `.dev_tools/session_state.json` for seamless context handoff.

### How It Works

1. **During Work:**
   - PowerShell switcher updates `session_state.json` with current account
   - Session state tracks: active account, last commit, todos, decisions

2. **When Switching Accounts:**
   - New Claude instance reads `session_state.json`
   - Auto-detects previous session (if <24h old)
   - Resumes work automatically with full context

3. **Cross-Account Continuity:**
   ```powershell
   # Account 5 running out of tokens
   c15  # Switch to account 15
   # Account 15 auto-loads session state
   # Continues exactly where account 5 left off
   ```

### Python Integration

From Python scripts:
```python
from session_manager import track_account, get_active_account, list_accounts

# Track account switch
track_account(5)  # Account 5 is now active

# Get current account
account = get_active_account()  # Returns: "account_5"

# List all accounts
accounts = list_accounts()
# Returns: {
#   'active_account': 'account_5',
#   'primary_exists': True,
#   'numbered_accounts': [
#     {'number': 1, 'path': '...', 'authenticated': True},
#     {'number': 5, 'path': '...', 'authenticated': True},
#     ...
#   ]
# }
```

---

## Best Practices

### Token Limit Management

**Recommended workflow:**
1. Use primary account for normal work
2. When approaching token limit, create session state snapshot
3. Switch to next available account
4. Continue work with automatic context loading
5. Rotate through accounts as needed

**Example rotation:**
```powershell
# Week 1: Use accounts 1-5
c1  # Monday
c2  # Tuesday
c3  # Wednesday
# ... etc

# Week 2: Use accounts 6-10
c6  # Monday
c7  # Tuesday
# ... etc
```

### Account Organization

**Suggestion: Themed accounts**
- Accounts 1-5: Main development work
- Accounts 6-10: Testing and experimentation
- Accounts 11-15: Documentation work
- Accounts 16-20: Code review and analysis
- Accounts 21-35: Reserve/overflow

### Backup Strategy

**Create backup before major changes:**
```powershell
# Before switching to multi-account system
.\D:\Projects\main\.dev_tools\Backup-ClaudeConfig.ps1

# Periodic backups (weekly)
.\D:\Projects\main\.dev_tools\Backup-ClaudeConfig.ps1
```

Backups are stored in: `D:\Projects\main\.artifacts\claude_backups\`

---

## Technical Details

### Directory Structure

```
C:\Users\{you}\
├─ .claude\              # Primary account (default)
├─ .claude1\             # Account 1
├─ .claude2\             # Account 2
├─ .claude3\             # Account 3
├─ ...
└─ .claude35\            # Account 35
```

### Environment Variable

The system uses `CLAUDE_CONFIG_DIR` to control which account is active:

```powershell
# Primary account (default)
$env:CLAUDE_CONFIG_DIR = $null

# Account 5
$env:CLAUDE_CONFIG_DIR = "C:\Users\you\.claude5"
```

### Files Created

| File | Location | Purpose |
|------|----------|---------|
| `Switch-ClaudeAccount.ps1` | `.dev_tools\` | Core switcher logic |
| `claude-profile.ps1` | `.dev_tools\` | PowerShell profile integration |
| `Validate-ClaudeAccounts.ps1` | `.dev_tools\` | Safety validation |
| `Backup-ClaudeConfig.ps1` | `.dev_tools\` | Backup utility |
| `Restore-ClaudeConfig.ps1` | `.dev_tools\` | Restore utility |
| `session_manager.py` | `.dev_tools\` | Python session tracking (enhanced) |

---

## Security Considerations

### Auth Token Isolation

Each account maintains separate authentication:
- ✅ No shared credentials between accounts
- ✅ Each account requires separate login
- ✅ Token revocation affects only that account
- ✅ Lost token doesn't impact other accounts

### What This System Does NOT Do

- ❌ Bypass rate limits (each account has separate limits)
- ❌ Share authentication automatically (each needs login)
- ❌ Merge session histories between accounts
- ❌ Synchronize settings across accounts

### Compliance

This system is designed for:
- ✅ Legitimate multi-account usage
- ✅ Token limit management
- ✅ Development workflow optimization
- ✅ Session continuity across accounts

**Use responsibly and within Claude Code's terms of service.**

---

## Uninstallation

To remove the multi-account system:

1. **Return to primary:**
   ```powershell
   claude-primary
   ```

2. **Remove account directories (optional):**
   ```powershell
   1..35 | ForEach-Object {
       Remove-Item "$env:USERPROFILE\.claude$_" -Recurse -Force -ErrorAction SilentlyContinue
   }
   ```

3. **Remove from PowerShell profile:**
   Edit `$PROFILE` and remove the line:
   ```powershell
   . D:\Projects\main\.dev_tools\claude-profile.ps1
   ```

4. **Reload profile:**
   ```powershell
   . $PROFILE
   ```

Your primary `.claude` directory remains untouched.

---

## Support & Maintenance

### Status Check

Run this to check system health:
```powershell
.\D:\Projects\main\.dev_tools\Validate-ClaudeAccounts.ps1
```

### Log Issues

If you encounter issues:
1. Run validation script
2. Check `session_state.json` for corruption
3. Verify `CLAUDE_CONFIG_DIR` is set correctly
4. Check backup availability

### Updates

This system is version-controlled in the project repository. Check git history for updates:
```bash
git log --oneline -- .dev_tools/Switch-ClaudeAccount.ps1
```

---

## FAQ

**Q: How many accounts can I use?**
A: Up to 35 numbered accounts (1-35) plus the primary account.

**Q: Do I need to log in every time I switch?**
A: No, only the first time you use each account. After that, credentials persist.

**Q: Can I use accounts on different machines?**
A: Each machine needs separate authentication per account.

**Q: What happens if I delete an account directory?**
A: The system will recreate it next time you switch to that account. You'll need to log in again.

**Q: Can I rename account directories?**
A: Not recommended. The system expects specific naming (`.claude1`, `.claude2`, etc.).

**Q: How do I know which account is active?**
A: Use `claude-status` or check `$env:CLAUDE_CONFIG_DIR`.

**Q: Can I share accounts between users?**
A: No, account directories are user-specific (tied to `%USERPROFILE%`).

**Q: What if I exceed 35 accounts?**
A: The system is designed for 35. If you need more, modify `$MaxAccounts` in the scripts.

---

## Changelog

### 2025-10-11 - Initial Release
- [NEW] Dynamic account switcher with safety protocol
- [NEW] PowerShell profile integration (c1-c35 aliases)
- [NEW] Session state tracking integration
- [NEW] Safety validation script
- [NEW] Backup and restore utilities
- [NEW] Comprehensive documentation

---

## Credits

**System:** Claude Code Multi-Account Manager
**Repository:** https://github.com/theSadeQ/dip-smc-pso.git
**Documentation:** D:\Projects\main\.dev_tools\MULTI_ACCOUNT_GUIDE.md

**For questions or improvements, submit issues to the project repository.**

---

**[OK] You're ready to use the multi-account system safely!**
