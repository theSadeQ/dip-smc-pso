# Claude Code Multi-Account System - User Guide

**Last Updated:** October 22, 2025
**Status:** ✅ Operational (Fixed authentication persistence and VSCode integration)
**Platform:** Linux (bash)

---

## Overview

This system allows you to manage multiple Claude Code accounts on a single machine with:
- **Isolated authentication** - Each account has its own credentials
- **Persistent sessions** - Authentication state survives across terminal sessions
- **CLI support** - Switch accounts for `claude` command-line usage
- **VSCode integration** - Launch VSCode with specific accounts
- **Easy switching** - Simple commands like `c 2` to switch accounts

---

## Installation

### 1. Verify Installation

The system should already be set up if you see this message when opening a terminal:

```bash
[OK] Claude Code multi-account switcher loaded
     Type 'claude-help' for usage instructions
```

### 2. Manual Installation (if needed)

If not installed, add this line to your `~/.bashrc`:

```bash
source /media/sadeq/asus1/Projects/main/.dev_tools/claude-profile.sh
```

Then reload your shell:

```bash
source ~/.bashrc
```

---

## Quick Start

### Switching Accounts (CLI)

```bash
# Switch to account 2 and launch Claude Code CLI
c 2

# Switch to account 15 and launch
c 15

# Switch without launching (just set environment)
c 2 --no-launch

# Switch back to primary account
claude-primary
```

### Launching VSCode with Specific Account

```bash
# Open current directory with account 2
code-c 2 .

# Open specific project with account 5
code-c 5 /path/to/project

# Open with primary account
code-primary .
```

### Checking Current Account

```bash
# Show which account is currently active
claude-whoami

# Example output:
# Current account: 2
# Location: /home/sadeq/.claude2
# Auth status: ✓ Authenticated
```

### Viewing All Accounts

```bash
# Show status of all accounts
claude-status

# Example output:
# Currently active: Account 2
#
# Account 1: [✓ Auth] | Dirs: [✓] | Files: 3 [✓]
# Account 2: [✓ Auth] | Dirs: [✓] | Files: 5 [✓]
```

---

## Complete Command Reference

### Account Switching

| Command | Description | Example |
|---------|-------------|---------|
| `c <number>` | Switch to account and launch Claude CLI | `c 2` |
| `c <number> --no-launch` | Switch account without launching | `c 5 --no-launch` |
| `claude-primary` | Switch back to primary account | `claude-primary` |
| `claude-primary --no-launch` | Switch to primary without launching | `claude-primary --no-launch` |

### Information & Diagnostics

| Command | Description | Output |
|---------|-------------|--------|
| `claude-whoami` | Show current active account | Account number, location, auth status |
| `claude-status` | Show all accounts and their status | List of all accounts with auth/dir status |
| `claude-help` | Show help message | Full command reference |

### VSCode Integration

| Command | Description | Example |
|---------|-------------|---------|
| `code-c <number> [path]` | Open VSCode with specific account | `code-c 2 .` |
| `code-primary [path]` | Open VSCode with primary account | `code-primary /path/to/project` |

---

## How It Works

### Directory Structure

Each account has its own isolated directory:

```
~/.claude          # Primary account (default)
~/.claude1         # Account 1
~/.claude2         # Account 2
~/.claude3         # Account 3
...
~/.claude5000      # Account 5000 (max)
```

### Required Subdirectories

Each account directory contains:

```
.claude{N}/
├── ide/               # IDE-specific files (lock files, state)
├── projects/          # Project-specific data
├── session-env/       # Session environment data
├── shell-snapshots/   # Shell state snapshots
├── statsig/           # Analytics/stats data
├── todos/             # Todo list data
├── debug/             # Debug logs
├── downloads/         # Downloaded files
└── .credentials.json  # Authentication credentials (created after login)
```

**Note:** These directories are automatically created when you first switch to an account.

### Environment Variable

The system uses the `CLAUDE_CONFIG_DIR` environment variable to tell Claude Code which account to use:

```bash
# Primary account (default)
CLAUDE_CONFIG_DIR is not set → uses ~/.claude

# Account 2
CLAUDE_CONFIG_DIR=~/.claude2 → uses ~/.claude2
```

**Key Fix:** The environment variable is now set in your **current shell** (not a subprocess), so it persists across commands.

---

## First-Time Account Setup

### Step 1: Switch to Account

```bash
c 2
```

**Expected output:**

```
[INFO] Switching to Claude Code Account 2...
[OK] Primary .claude directory exists
[INFO] Account directory exists: /home/sadeq/.claude2
[INFO] Initializing account directory structure...
[OK] Account structure initialized (8 directories)
[OK] Set CLAUDE_CONFIG_DIR: /home/sadeq/.claude2
[WARN] Account 2 needs authentication
[INFO] Claude Code will prompt for login on first use
[OK] Successfully switched to Account 2
[OK] Environment updated: CLAUDE_CONFIG_DIR=/home/sadeq/.claude2
[INFO] Launching Claude Code...
```

### Step 2: Authenticate

Claude Code will prompt you to log in (first time only):

1. Browser will open for OAuth authentication
2. Sign in with your Claude account credentials
3. Authorize the application
4. Return to terminal

### Step 3: Verify

```bash
claude-whoami
```

**Expected output:**

```
Current account: 2
Location: /home/sadeq/.claude2
Auth status: ✓ Authenticated
```

### Step 4: Test Persistence

**Exit Claude Code** and run again:

```bash
c 2
```

**You should NOT be prompted to authenticate again!** The credentials are saved in `~/.claude2/.credentials.json`.

---

## Common Workflows

### Development Workflow (CLI + VSCode)

```bash
# Morning: Start working on project with account 2
c 2 --no-launch        # Switch account without launching CLI yet
code-c 2 .             # Open VSCode with account 2
# (Work in VSCode using Claude Code extension)

# Later: Need to use CLI for batch operations
c 2                    # Launch Claude CLI (already authenticated)
# (Use Claude Code CLI)

# End of day: Switch back to primary
claude-primary --no-launch
```

### Testing Multiple Accounts

```bash
# Test with account 1
c 1
# (Run some tests)

# Test with account 2
c 2
# (Run same tests with different account)

# Compare results
claude-status
```

### Clean Account Setup

```bash
# Create new account (first time)
c 3

# Verify directory structure
claude-status
# Should show:
# Account 3: [! Login] | Dirs: [✓] | Files: 0 [✓]

# Authenticate
# (Claude Code will prompt for login)

# Verify authentication persisted
claude-whoami
# Should show:
# Current account: 3
# Location: /home/sadeq/.claude3
# Auth status: ✓ Authenticated
```

---

## Troubleshooting

### Issue: "Claude Code still prompts for login every time"

**Diagnosis:**

```bash
# Check if credentials file exists
ls -la ~/.claude2/.credentials.json

# If file doesn't exist, authentication isn't persisting
```

**Solution 1: Verify environment variable is set**

```bash
# After running `c 2`, check:
echo $CLAUDE_CONFIG_DIR
# Should output: /home/sadeq/.claude2

# If empty, reload profile:
source ~/.bashrc
```

**Solution 2: Verify directory structure**

```bash
# Check if all required directories exist
claude-status
# Look for: Dirs: [✓]
# If you see: Dirs: [✗ N missing], run:

c 2 --no-launch  # This will auto-initialize directories
```

**Solution 3: Check file permissions**

```bash
# Credentials file should be private
chmod 600 ~/.claude2/.credentials.json

# Account directory should be accessible
chmod 755 ~/.claude2
```

### Issue: "VSCode not recognizing the account"

**Diagnosis:**

```bash
# Check if VSCode was launched with environment variable
# After running `code-c 2 .`, in VSCode terminal:
echo $CLAUDE_CONFIG_DIR
# Should output: /home/sadeq/.claude2
```

**Solution 1: Use `code-c` command**

```bash
# DON'T do this:
c 2 --no-launch
code .              # ❌ Won't inherit CLAUDE_CONFIG_DIR

# DO this:
code-c 2 .          # ✅ Launches VSCode with correct environment
```

**Solution 2: Restart VSCode**

```bash
# If VSCode was already open when you switched accounts:
# 1. Close all VSCode windows
# 2. Run: code-c 2 .
```

### Issue: "Environment variable doesn't persist across terminal sessions"

**Diagnosis:**

```bash
# In terminal 1:
c 2
echo $CLAUDE_CONFIG_DIR  # Shows /home/sadeq/.claude2

# Close terminal, open new terminal 2:
echo $CLAUDE_CONFIG_DIR  # Empty!
```

**This is EXPECTED behavior.** The environment variable is session-specific.

**Solution: Just run `c 2` again in the new terminal**

```bash
# New terminal session:
c 2 --no-launch  # Sets environment variable
echo $CLAUDE_CONFIG_DIR  # Now shows /home/sadeq/.claude2

# Authentication will still be there (credentials file persists)
```

### Issue: "Account shows [✗ N missing] directories"

**Diagnosis:**

```bash
claude-status
# Shows: Account 2: [! Login] | Dirs: [✗ 8 missing] | Files: 0 [✓]
```

**Solution: Switch to the account to auto-initialize**

```bash
c 2 --no-launch
# This will auto-create all 8 required directories

# Verify:
claude-status
# Should now show: Account 2: [! Login] | Dirs: [✓] | Files: 0 [✓]
```

### Issue: "Command `c` not found"

**Diagnosis:**

```bash
# Check if profile script is sourced:
type c
# If output is "c: command not found", profile isn't loaded
```

**Solution: Source the profile script**

```bash
# Temporary (current session only):
source /media/sadeq/asus1/Projects/main/.dev_tools/claude-profile.sh

# Permanent (add to ~/.bashrc):
echo 'source /media/sadeq/asus1/Projects/main/.dev_tools/claude-profile.sh' >> ~/.bashrc
source ~/.bashrc
```

---

## Advanced Usage

### Validation and Testing

```bash
# Run comprehensive validation
bash /media/sadeq/asus1/Projects/main/.dev_tools/validate-claude-accounts.sh --verbose

# Check for safety violations (symlinks)
bash /media/sadeq/asus1/Projects/main/.dev_tools/validate-claude-accounts.sh

# Auto-fix issues
bash /media/sadeq/asus1/Projects/main/.dev_tools/validate-claude-accounts.sh --fix-issues
```

### Direct Script Usage

```bash
# Switch using script directly (for automation)
bash /media/sadeq/asus1/Projects/main/.dev_tools/switch-claude-account.sh 2 --no-launch

# Show help
bash /media/sadeq/asus1/Projects/main/.dev_tools/switch-claude-account.sh --help
```

### Session State Integration

The system automatically updates session state in:

```
/media/sadeq/asus1/Projects/main/.ai/config/session_state.json
```

This tracks:
- Current account number
- Last update timestamp
- (Used by other project recovery tools)

---

## Safety & Security

### Authentication Isolation

✅ **Each account has its own credentials file**
- `~/.claude/.credentials.json` (primary)
- `~/.claude2/.credentials.json` (account 2)
- etc.

❌ **No symlinks allowed** - The system prevents auth file sharing via symlinks.

### Validation Checks

The system performs automatic safety checks:

1. **No auth symlinks** - Ensures `.credentials.json` is a real file, not a symlink
2. **Directory structure** - Validates all required subdirectories exist
3. **File permissions** - Checks credentials files are private (600)

Run validation anytime:

```bash
claude-status  # Quick check
bash /media/sadeq/asus1/Projects/main/.dev_tools/validate-claude-accounts.sh  # Full validation
```

---

## FAQ

### Q: How many accounts can I have?

**A:** Up to 5000 accounts (1-5000). Practically, most users need 2-5 accounts.

### Q: Can I use the same Claude account credentials for multiple local accounts?

**A:** Yes! You can authenticate with the same Claude.ai credentials on multiple local accounts (e.g., `.claude1`, `.claude2`). Each will maintain separate session state and project data.

### Q: What happens if I delete `~/.claude2/`?

**A:** The account is deleted. Next time you run `c 2`, a fresh account will be created (requires re-authentication).

### Q: Can I backup my accounts?

**A:** Yes! Just backup the directories:

```bash
# Backup account 2
tar -czf claude2-backup.tar.gz ~/.claude2/

# Restore later
tar -xzf claude2-backup.tar.gz -C ~/
```

### Q: Does this work with the Claude Code VSCode extension?

**A:** Yes! Use `code-c <number> [path]` to launch VSCode with a specific account.

### Q: Will my primary account be affected?

**A:** No. The primary `~/.claude` directory is never modified by the multi-account system. You can always return to it with `claude-primary`.

### Q: Can I use this on Windows or macOS?

**A:** The current version is **Linux-only**. Windows/macOS support would require porting the shell scripts.

---

## What Changed (October 2025 Fix)

### ❌ Old Behavior (Broken)

1. **Re-authentication on every launch**
   - Credentials weren't saving to account directories
   - Empty directories didn't have required structure

2. **Environment variable didn't persist**
   - Running `c 2` in a script set variable in subprocess only
   - Parent shell didn't inherit the variable

3. **VSCode couldn't use accounts**
   - No way to launch VSCode with specific account
   - Extension always used primary account

### ✅ New Behavior (Fixed)

1. **Persistent authentication**
   - Credentials save correctly to `~/.claude{N}/.credentials.json`
   - Directory structure auto-initializes (8 required subdirectories)
   - Authentication survives terminal restarts

2. **Environment variable persists in shell**
   - `c` function sets variable in **current shell**, not subprocess
   - Variable stays set for all subsequent commands in that terminal

3. **Full VSCode integration**
   - `code-c <number> [path]` launches VSCode with specific account
   - Extension recognizes and uses account credentials
   - `code-primary [path]` returns to primary account

---

## Support

### Issues or Questions?

1. **Check status first:**
   ```bash
   claude-status
   claude-whoami
   ```

2. **Run validation:**
   ```bash
   bash /media/sadeq/asus1/Projects/main/.dev_tools/validate-claude-accounts.sh --verbose
   ```

3. **Review this guide's troubleshooting section**

4. **Check script logs** (if available in your session)

### Related Files

- **Profile script:** `/media/sadeq/asus1/Projects/main/.dev_tools/claude-profile.sh`
- **Switch script:** `/media/sadeq/asus1/Projects/main/.dev_tools/switch-claude-account.sh`
- **Validation script:** `/media/sadeq/asus1/Projects/main/.dev_tools/validate-claude-accounts.sh`
- **This guide:** `/media/sadeq/asus1/Projects/main/.dev_tools/MULTI_ACCOUNT_GUIDE.md`

---

**Version:** 2.0 (Fixed for Linux)
**Date:** October 22, 2025
**Tested:** Linux (bash)
