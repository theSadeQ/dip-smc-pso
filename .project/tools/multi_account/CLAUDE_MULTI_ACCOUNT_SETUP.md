# Claude Multi-Account Setup (Linux)

This directory contains Linux bash equivalents of the PowerShell multi-account system for managing multiple Claude Code accounts.

## Files

- `switch-claude-account.sh` - Main account switcher script
- `claude-profile.sh` - Bash profile integration for convenient aliases
- `validate-claude-accounts.sh` - Safety validator for account isolation

## Quick Start

### 1. Setup Bash Profile Integration

Add to your `~/.bashrc` or `~/.bash_profile`:

```bash
source /media/sadeq/asus1/Projects/main/.dev_tools/claude-profile.sh
```

Then reload:
```bash
source ~/.bashrc
```

### 2. Usage

#### Quick Switch (Recommended)
```bash
c 5          # Switch to account 5 and launch Claude
c 42         # Switch to account 42 and launch Claude
c 100        # Switch to account 100 and launch Claude
```

#### Switch Without Launching
```bash
c 5 --no-launch
```

#### Return to Primary Account
```bash
claude-primary
```

#### Validate All Accounts
```bash
claude-status
```

#### Show Help
```bash
claude-help
```

### 3. Manual Usage (Without Profile)

```bash
# Switch to account
./switch-claude-account.sh 5

# Switch without launching
./switch-claude-account.sh 5 --no-launch

# Return to primary
./switch-claude-account.sh --primary

# Validate accounts
./switch-claude-account.sh --validate

# Show help
./switch-claude-account.sh --help
```

## How It Works

### Directory Structure

Each account gets its own isolated directory:
- Primary: `~/.claude`
- Account 1: `~/.claude1`
- Account 2: `~/.claude2`
- ...
- Account 5000: `~/.claude5000`

### Environment Variable

The script sets `CLAUDE_CONFIG_DIR` to point to the account directory:
```bash
export CLAUDE_CONFIG_DIR="$HOME/.claude5"
```

### Isolated Authentication

Each account maintains its own:
- `.credentials.json` - Authentication credentials
- `history.jsonl` - Command history
- `.claude.json` - Configuration
- `settings.json` - User settings

### Launch Command

By default, the script launches Claude with:
```bash
claude --dangerously-skip-permissions
```

## Safety Features

### No Symlink Sharing

The system validates that authentication files are **real files**, not symlinks. This ensures complete isolation between accounts.

### Validation

Run safety checks:
```bash
./validate-claude-accounts.sh
```

With verbose output:
```bash
./validate-claude-accounts.sh --verbose
```

Auto-fix symlink violations:
```bash
./validate-claude-accounts.sh --fix-issues
```

## Examples

### Example 1: Switch Between Multiple Accounts
```bash
# Work on account 1
c 1
# ... do some work ...
# exit Claude

# Switch to account 2
c 2
# ... do some work ...
# exit Claude

# Return to primary
claude-primary
```

### Example 2: Batch Setup Multiple Accounts
```bash
# Switch to each account to initialize directories (without launching)
for i in {1..10}; do
    ./switch-claude-account.sh $i --no-launch
done

# Validate all accounts
claude-status
```

### Example 3: Check Account Status
```bash
# See which accounts exist and their authentication status
claude-status
```

Output:
```
[INFO] Checking primary .claude directory...
[OK] Primary .claude exists (5 files)
[INFO] Checking current environment...
[INFO] CLAUDE_CONFIG_DIR not set (using primary)
[INFO] Scanning accounts 1-5000...

Account 1: [Authenticated] (4 files) [SAFE]
Account 2: [Needs login] (0 files) [SAFE]
Account 5: [Authenticated] (6 files) [SAFE]

[OK] Found 3 account(s):
  Account 1: [OK] Authenticated (4 files)
  Account 2: [!] Needs login (0 files)
  Account 5: [OK] Authenticated (6 files)
```

## Differences from PowerShell Version

| Feature | PowerShell | Bash (Linux) |
|---------|-----------|--------------|
| Directory paths | `$env:USERPROFILE\.claude` | `$HOME/.claude` |
| Max accounts | 50,000 | 5,000 |
| Link detection | Junctions/SymbolicLinks | Symlinks |
| Session state update | PowerShell JSON | jq (if available) |
| Color output | Write-Host colors | ANSI escape codes |
| Function syntax | `function Name {}` | `name() {}` |

## Requirements

### Required
- Bash 4.0+
- Claude Code CLI installed

### Optional
- `jq` - For session state tracking (install: `sudo apt install jq`)
- Colorized terminal - For colored output

## Troubleshooting

### "Primary .claude directory not found"
Run Claude Code at least once to create the primary directory:
```bash
claude
```

### "Account needs authentication"
The first time you use an account, Claude will prompt for login:
```bash
c 5  # Will show login prompt on first use
```

### Profile not loading
Make sure you added the source line to the correct file:
```bash
# Check which shell you're using
echo $SHELL

# For bash: ~/.bashrc
# For zsh: ~/.zshrc

# Reload after adding
source ~/.bashrc  # or source ~/.zshrc
```

### Permissions error
Make sure scripts are executable:
```bash
chmod +x .dev_tools/*.sh
```

## Session State Integration

If the session state file exists at `/media/sadeq/asus1/Projects/main/.ai/config/session_state.json`, the script will automatically update it with:
- Current account number
- Timestamp of last switch

This requires `jq` to be installed. If not available, the script will skip this step with a warning.

## Security Notes

### Dangerously Skip Permissions Flag

The `--dangerously-skip-permissions` flag is used to allow Claude to run without constant permission prompts. This is **intentional** for a multi-account testing/development environment.

**Only use this if:**
- You trust the code you're working with
- You're in a development/testing environment
- You understand the security implications

**Do NOT use in production environments** where untrusted code might be executed.

### Account Isolation

Each account is completely isolated:
- ✅ Separate authentication credentials
- ✅ Separate command history
- ✅ Separate settings
- ✅ No shared state between accounts

This ensures that work done in one account cannot affect other accounts.

## Advanced Usage

### Custom Account Range

To change the maximum number of accounts, edit `switch-claude-account.sh`:
```bash
MAX_ACCOUNTS=10000  # Change from 5000 to 10000
```

### Integration with Project Recovery

The session state integration works with the project recovery system in `.dev_tools/recover_project.sh`. When you switch accounts, the recovery system will know which account was last used.

### Environment Persistence

The `CLAUDE_CONFIG_DIR` environment variable persists only in the current shell session. For permanent switching:

```bash
# Add to ~/.bashrc
export CLAUDE_CONFIG_DIR="$HOME/.claude5"
```

But it's recommended to use the switcher script instead for proper session tracking.

## Contributing

When adding features:
1. Maintain compatibility with PowerShell version concepts
2. Follow bash best practices (shellcheck validation)
3. Preserve safety checks (symlink detection)
4. Update this documentation

## License

Part of the DIP-SMC-PSO project. See main repository LICENSE.
