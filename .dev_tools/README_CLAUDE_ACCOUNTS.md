# Claude Multi-Account System - Quick Reference

> Linux bash implementation of PowerShell multi-account switcher

## 🚀 One-Time Setup

```bash
# Install aliases to your shell profile
./.dev_tools/install-claude-aliases.sh

# Reload your shell
source ~/.bashrc   # or source ~/.zshrc for zsh
```

## 📝 Quick Commands

Once installed, you can use these commands from anywhere:

```bash
c 5              # Switch to account 5 and launch Claude
c 42             # Switch to account 42 and launch Claude
c 100            # Switch to account 100 and launch Claude
c 5 --no-launch  # Switch to account 5 WITHOUT launching

claude-primary   # Return to primary account
claude-status    # Show all accounts and their status
claude-help      # Show help message
```

## 🎯 Common Use Cases

### Use Case 1: Testing Different Configurations
```bash
# Account 1: Production settings
c 1

# Account 2: Experimental features
c 2

# Account 3: Testing new prompts
c 3
```

### Use Case 2: Separate Projects
```bash
# Account 1: Project A
c 1

# Account 2: Project B
c 2

# Account 3: Personal experiments
c 3
```

### Use Case 3: Different API Keys
```bash
# Each account can have its own API key/credentials
c 1  # Uses account 1 credentials
c 2  # Uses account 2 credentials
```

## 🔧 Manual Usage (No Aliases)

If you don't want to install aliases:

```bash
# Switch to account 5
./.dev_tools/switch-claude-account.sh 5

# Switch without launching
./.dev_tools/switch-claude-account.sh 5 --no-launch

# Return to primary
./.dev_tools/switch-claude-account.sh --primary

# Validate accounts
./.dev_tools/switch-claude-account.sh --validate
```

## 📁 How It Works

### Directory Structure
```
$HOME/
├── .claude           # Primary account
├── .claude1          # Account 1
├── .claude2          # Account 2
├── .claude3          # Account 3
├── ...
└── .claude5000       # Account 5000
```

### Each Account Contains
```
.claude1/
├── .credentials.json    # Authentication (isolated)
├── history.jsonl        # Command history (isolated)
├── .claude.json         # Config (isolated)
└── settings.json        # Settings (isolated)
```

### Environment Variable
The script sets `CLAUDE_CONFIG_DIR`:
```bash
export CLAUDE_CONFIG_DIR="$HOME/.claude5"
```

Then launches:
```bash
claude --dangerously-skip-permissions
```

## 🛡️ Safety Features

### Complete Isolation
- ✅ Each account has its own authentication
- ✅ Each account has its own history
- ✅ Each account has its own settings
- ✅ No shared state between accounts

### Safety Validation
```bash
# Check all accounts for safety violations
./.dev_tools/validate-claude-accounts.sh

# Verbose output
./.dev_tools/validate-claude-accounts.sh --verbose

# Auto-fix issues
./.dev_tools/validate-claude-accounts.sh --fix-issues
```

## 📊 Account Status

```bash
claude-status
```

Example output:
```
[INFO] Checking primary .claude directory...
[OK] Primary .claude exists (5 files)
[INFO] Scanning accounts 1-5000...

Account 1: [Authenticated] (4 files) [SAFE]
Account 2: [Needs login] (0 files) [SAFE]
Account 5: [Authenticated] (6 files) [SAFE]

[OK] Found 3 account(s)
```

## 🔍 Troubleshooting

### Aliases not working
```bash
# Make sure you reloaded your shell profile
source ~/.bashrc

# Or open a new terminal window
```

### Scripts not executable
```bash
chmod +x .dev_tools/*.sh
```

### Account needs authentication
```bash
# First time using an account, Claude will prompt for login
c 5  # Will show login prompt
```

### Line ending issues (if copying from Windows)
```bash
# Fix all scripts
sed -i 's/\r$//' .dev_tools/*.sh
chmod +x .dev_tools/*.sh
```

## 📚 Files

| File | Description |
|------|-------------|
| `switch-claude-account.sh` | Main switcher script |
| `claude-profile.sh` | Bash profile integration |
| `validate-claude-accounts.sh` | Safety validator |
| `install-claude-aliases.sh` | One-time setup installer |
| `CLAUDE_MULTI_ACCOUNT_SETUP.md` | Comprehensive documentation |
| `README_CLAUDE_ACCOUNTS.md` | This file (quick reference) |

## ⚠️ Important Notes

### Dangerously Skip Permissions
The `--dangerously-skip-permissions` flag is used to avoid constant permission prompts.

**Only use in development/testing environments where you trust the code!**

### Maximum Accounts
Default: 5000 accounts (1-5000)

To change, edit `switch-claude-account.sh`:
```bash
MAX_ACCOUNTS=10000  # Change this value
```

### Session Persistence
The `CLAUDE_CONFIG_DIR` environment variable only persists in the current shell session. Use the switcher script each time you start a new terminal.

## 🆘 Getting Help

```bash
# Show all available commands
claude-help

# Show switcher help
./.dev_tools/switch-claude-account.sh --help

# Show validator help
./.dev_tools/validate-claude-accounts.sh --help
```

## 📖 Full Documentation

For comprehensive documentation, see: `.dev_tools/CLAUDE_MULTI_ACCOUNT_SETUP.md`

## 🔗 Related

This is the Linux bash port of the PowerShell scripts:
- `Switch-ClaudeAccount.ps1`
- `claude-profile.ps1`
- `Validate-ClaudeAccounts.ps1`

All functionality has been preserved with Linux-specific adaptations.
