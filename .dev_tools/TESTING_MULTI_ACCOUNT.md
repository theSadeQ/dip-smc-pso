# Multi-Account System - Testing Guide

**Date:** October 22, 2025
**Status:** ✅ All fixes implemented

---

## What Was Fixed

### Root Causes (October 2025)

1. **Empty Account Directories** - `.claude1` and `.claude2` had no subdirectories
2. **Environment Variable Not Persisting** - `CLAUDE_CONFIG_DIR` only set in subprocess
3. **No VSCode Integration** - No way to launch VSCode with specific account
4. **Re-authentication Required** - Credentials weren't saving to account directories

### Fixes Applied

✅ **Directory Structure Auto-Initialization**
- Added 8 required subdirectories: `ide/`, `projects/`, `session-env/`, `shell-snapshots/`, `statsig/`, `todos/`, `debug/`, `downloads/`
- Automatically created when switching accounts
- Validated with enhanced `claude-status` command

✅ **Environment Variable Persistence**
- Rewrote `c` function to set variable in current shell (not subprocess)
- Added `claude-whoami` to show current active account
- Variable now persists for all commands in terminal session

✅ **VSCode Integration**
- Created `code-c <number> [path]` command
- Launches VSCode with `CLAUDE_CONFIG_DIR` environment variable
- Created `code-primary [path]` to return to primary account

✅ **Enhanced Diagnostics**
- `claude-status` shows directory structure status
- `claude-whoami` shows current account + auth status
- Validation script shows missing directories

---

## Quick Test Workflow

### Test 1: Basic Account Switching (CLI)

```bash
# 1. Reload shell profile (get latest changes)
source ~/.bashrc

# 2. Verify profile loaded
claude-help
# Should show updated help with new commands

# 3. Check current account
claude-whoami
# Expected: "Current account: primary"

# 4. Switch to account 2
c 2
# Expected:
# - [INFO] Initializing account directory structure...
# - [OK] Account structure initialized (8 directories)
# - [OK] Environment updated: CLAUDE_CONFIG_DIR=/home/sadeq/.claude2
# - [INFO] Launching Claude Code...

# 5. Authenticate (first time only)
# Browser will open - sign in with Claude credentials

# 6. Exit Claude Code, then verify account still active
claude-whoami
# Expected:
# Current account: 2
# Location: /home/sadeq/.claude2
# Auth status: ✓ Authenticated (if you authenticated)

# 7. Switch again - should NOT prompt for auth
c 2
# Expected:
# - [OK] Account 2 is authenticated (no warning!)
# - Launches without asking for login
```

### Test 2: Environment Variable Persistence

```bash
# 1. Open new terminal tab/window

# 2. Run c 2 WITHOUT launching
c 2 --no-launch

# 3. Check environment variable
echo $CLAUDE_CONFIG_DIR
# Expected: /home/sadeq/.claude2

# 4. Run ANY command - variable should still be set
ls
echo $CLAUDE_CONFIG_DIR
# Expected: /home/sadeq/.claude2 (still set!)

# 5. Launch Claude Code manually
claude --dangerously-skip-permissions
# Should use account 2 automatically
```

### Test 3: VSCode Integration

```bash
# 1. Close all VSCode windows

# 2. Launch VSCode with account 2
code-c 2 .
# Expected:
# - [OK] Launching VSCode with Account 2
# - CLAUDE_CONFIG_DIR: /home/sadeq/.claude2
# - VSCode opens

# 3. In VSCode terminal, verify environment
echo $CLAUDE_CONFIG_DIR
# Expected: /home/sadeq/.claude2

# 4. Open Claude Code extension in VSCode
# - Should use account 2 credentials
# - Should NOT prompt for authentication (if already authenticated)

# 5. Close VSCode, launch with primary
code-primary .
# Expected:
# - [OK] Launching VSCode with primary account
# - VSCode terminal: echo $CLAUDE_CONFIG_DIR → (empty)
```

### Test 4: Directory Structure Validation

```bash
# 1. Check all accounts status
claude-status
# Expected:
# Currently active: Account 2
#
# Account 1: [! Login] | Dirs: [✓] | Files: 0 [✓]
# Account 2: [✓ Auth] | Dirs: [✓] | Files: 3 [✓]

# 2. Run full validation
bash /media/sadeq/asus1/Projects/main/.dev_tools/validate-claude-accounts.sh
# Expected:
# - Account 1: [! Login] | Dirs: [✓] | Files: 0 [✓]
# - Account 2: [✓ Auth] | Dirs: [✓] | Files: 3 [✓]
# - All safety checks passed!

# 3. Check directory structure manually
ls -la ~/.claude2/
# Expected to see:
# - ide/
# - projects/
# - session-env/
# - shell-snapshots/
# - statsig/
# - todos/
# - debug/
# - downloads/
# - .credentials.json (if authenticated)
```

### Test 5: Cross-Session Persistence

```bash
# 1. Switch to account 2 and authenticate
c 2
# (Sign in if first time)

# 2. Verify credentials file exists
ls -la ~/.claude2/.credentials.json
# Expected: File exists with recent timestamp

# 3. Close terminal completely

# 4. Open NEW terminal session

# 5. Switch to account 2 again
c 2
# Expected:
# - [OK] Account 2 is authenticated
# - NO browser authentication prompt
# - Launches immediately

# SUCCESS: Authentication persisted across sessions!
```

---

## Expected Behavior Summary

### ✅ Working (After Fix)

1. **First switch to account creates full directory structure**
2. **Environment variable set in current shell, persists across commands**
3. **Authentication persists after first login**
4. **VSCode integration works with `code-c <number> [path]`**
5. **`claude-whoami` shows current active account**
6. **`claude-status` shows all accounts with dir structure status**
7. **Switching accounts doesn't require re-authentication each time**

### ❌ Broken (Before Fix)

1. Account directories empty (no subdirectories)
2. Environment variable only set in subprocess
3. Re-authentication required every launch
4. No VSCode integration
5. No diagnostic commands

---

## Troubleshooting Test Failures

### If `claude-whoami` shows "c: command not found"

```bash
# Reload profile script
source ~/.bashrc

# Verify it loaded
type c
# Should show: c is a function
```

### If credentials don't persist

```bash
# 1. Check if .credentials.json was created
ls -la ~/.claude2/.credentials.json

# 2. If missing, check environment variable was set during authentication
echo $CLAUDE_CONFIG_DIR
# Should be: /home/sadeq/.claude2

# 3. Try authenticating again with explicit environment
c 2 --no-launch
export CLAUDE_CONFIG_DIR=~/.claude2
claude --dangerously-skip-permissions
# After successful auth, check:
ls -la ~/.claude2/.credentials.json
```

### If VSCode doesn't recognize account

```bash
# 1. Close ALL VSCode windows

# 2. Use code-c command (not regular code)
code-c 2 .

# 3. In VSCode terminal, verify environment
echo $CLAUDE_CONFIG_DIR
# Should be: /home/sadeq/.claude2

# 4. If empty, VSCode didn't inherit environment
# Solution: Close VSCode, try again with code-c
```

### If directory structure missing

```bash
# Auto-fix by switching to account
c 2 --no-launch

# Verify directories created
ls -la ~/.claude2/
# Should see 8 subdirectories

# If still missing, run validation to diagnose
bash /media/sadeq/asus1/Projects/main/.dev_tools/validate-claude-accounts.sh --verbose
```

---

## Files Modified (October 22, 2025)

1. **`.dev_tools/switch-claude-account.sh`**
   - Added `initialize_account_directory()` function
   - Auto-creates 8 required subdirectories
   - Enhanced `get_account_status()` to check directory structure
   - Added `get_current_account()` helper

2. **`.dev_tools/claude-profile.sh`**
   - Rewrote `c()` function to set environment in current shell
   - Added `claude-whoami` command
   - Added `code-c <number> [path]` VSCode integration
   - Added `code-primary [path]` for primary account VSCode
   - Updated `claude-help` with new commands

3. **`.dev_tools/validate-claude-accounts.sh`**
   - Added `test_directory_structure()` function
   - Enhanced validation output to show directory status
   - Shows: `[✓ Auth] | Dirs: [✓] | Files: N [✓]`

4. **`.dev_tools/MULTI_ACCOUNT_GUIDE.md`**
   - Completely rewritten for Linux (bash)
   - Added comprehensive troubleshooting section
   - Documented new commands (`claude-whoami`, `code-c`, etc.)
   - Added workflow examples

5. **`.dev_tools/TESTING_MULTI_ACCOUNT.md`** (new)
   - This file - testing guide

---

## Success Criteria

✅ **All 5 tests pass without issues**
✅ **Authentication persists across terminal sessions**
✅ **VSCode recognizes account when launched with `code-c`**
✅ **Directory structure auto-initializes**
✅ **`claude-whoami` shows correct current account**
✅ **No re-authentication required after first login**

---

## Next Steps

1. **Test the workflow** (run all 5 tests above)
2. **Verify VSCode integration** (Test 3)
3. **Use in daily workflow** for a few days
4. **Report any issues** you encounter

---

**Status:** ✅ Ready for testing
**Estimated testing time:** 10-15 minutes
**Platform:** Linux (bash)
