# PowerShell vs Bash Command Comparison

Quick reference showing equivalent commands between Windows PowerShell and Linux Bash versions.

## Account Switching

| Task | PowerShell (Windows) | Bash (Linux) |
|------|---------------------|--------------|
| Switch to account 5 | `c 5` | `c 5` |
| Switch to account 42 | `c 42` | `c 42` |
| Switch to account 100 | `c 100` | `c 100` |
| Switch without launching | `c 5 -NoLaunch` | `c 5 --no-launch` |
| Return to primary | `claude-primary` | `claude-primary` |

## Validation & Status

| Task | PowerShell (Windows) | Bash (Linux) |
|------|---------------------|--------------|
| Check account status | `claude-status` | `claude-status` |
| Validate accounts | `Switch-ClaudeAccount -Validate` | `./.dev_tools/switch-claude-account.sh --validate` |
| Verbose validation | `.\Validate-ClaudeAccounts.ps1` | `./.dev_tools/validate-claude-accounts.sh --verbose` |
| Fix safety issues | `.\Validate-ClaudeAccounts.ps1 -FixIssues` | `./.dev_tools/validate-claude-accounts.sh --fix-issues` |

## Help & Information

| Task | PowerShell (Windows) | Bash (Linux) |
|------|---------------------|--------------|
| Show help | `claude-help` | `claude-help` |
| Switcher help | `Switch-ClaudeAccount -Help` | `./.dev_tools/switch-claude-account.sh --help` |
| Validator help | `Get-Help .\Validate-ClaudeAccounts.ps1` | `./.dev_tools/validate-claude-accounts.sh --help` |

## Manual Usage (No Aliases)

| Task | PowerShell (Windows) | Bash (Linux) |
|------|---------------------|--------------|
| Switch to account 5 | `.\Switch-ClaudeAccount.ps1 -AccountNum 5` | `./.dev_tools/switch-claude-account.sh 5` |
| Switch without launching | `.\Switch-ClaudeAccount.ps1 -AccountNum 5 -NoLaunch` | `./.dev_tools/switch-claude-account.sh 5 --no-launch` |
| Return to primary | `.\Switch-ClaudeAccount.ps1 -Primary` | `./.dev_tools/switch-claude-account.sh --primary` |

## Setup & Installation

| Task | PowerShell (Windows) | Bash (Linux) |
|------|---------------------|--------------|
| Install profile integration | Add to `$PROFILE`:<br>`. D:\Projects\main\.dev_tools\claude-profile.ps1` | Run installer:<br>`./.dev_tools/install-claude-aliases.sh`<br>or add to `~/.bashrc`:<br>`source /path/to/claude-profile.sh` |
| Reload profile | `. $PROFILE` | `source ~/.bashrc` |
| Check installation | `claude-help` | `claude-help` |

## File Locations

| Item | PowerShell (Windows) | Bash (Linux) |
|------|---------------------|--------------|
| Primary directory | `$env:USERPROFILE\.claude` | `$HOME/.claude` |
| Account 5 directory | `$env:USERPROFILE\.claude5` | `$HOME/.claude5` |
| Session state file | `D:\Projects\main\.ai\config\session_state.json` | `/media/sadeq/asus1/Projects/main/.ai/config/session_state.json` |
| Profile file | `$PROFILE` (PowerShell profile) | `~/.bashrc` (Bash profile) |

## Environment Variables

| Variable | PowerShell (Windows) | Bash (Linux) |
|----------|---------------------|--------------|
| Config directory | `$env:CLAUDE_CONFIG_DIR` | `$CLAUDE_CONFIG_DIR` |
| Set manually | `$env:CLAUDE_CONFIG_DIR = "path"` | `export CLAUDE_CONFIG_DIR="path"` |
| Clear variable | `Remove-Item Env:\CLAUDE_CONFIG_DIR` | `unset CLAUDE_CONFIG_DIR` |
| Check if set | `$env:CLAUDE_CONFIG_DIR` | `echo $CLAUDE_CONFIG_DIR` |

## Advanced Usage

### Initialize Multiple Accounts

**PowerShell**:
```powershell
1..10 | ForEach-Object { 
    .\Switch-ClaudeAccount.ps1 -AccountNum $_ -NoLaunch 
}
```

**Bash**:
```bash
for i in {1..10}; do
    ./.dev_tools/switch-claude-account.sh $i --no-launch
done
```

### Check Which Account is Active

**PowerShell**:
```powershell
if ($env:CLAUDE_CONFIG_DIR) {
    Write-Host "Active: $env:CLAUDE_CONFIG_DIR"
} else {
    Write-Host "Active: Primary"
}
```

**Bash**:
```bash
if [ -n "$CLAUDE_CONFIG_DIR" ]; then
    echo "Active: $CLAUDE_CONFIG_DIR"
else
    echo "Active: Primary"
fi
```

## Key Differences

| Aspect | PowerShell | Bash |
|--------|-----------|------|
| **Max accounts** | 50,000 | 5,000 (configurable) |
| **Flag syntax** | `-NoLaunch`, `-Primary` | `--no-launch`, `--primary` |
| **Path separator** | Backslash `\` | Forward slash `/` |
| **Home directory** | `$env:USERPROFILE` | `$HOME` |
| **JSON updates** | Native PowerShell | Requires `jq` |
| **Script extension** | `.ps1` | `.sh` |
| **Execution** | `.\script.ps1` | `./script.sh` |
| **Link detection** | Junctions/SymbolicLinks | Symlinks |

## Similarities

Both versions provide:
- ✅ Complete account isolation
- ✅ Safety validation
- ✅ Convenient aliases (c 5, claude-primary, etc.)
- ✅ Session state tracking
- ✅ Colored output
- ✅ Help documentation
- ✅ Same `--dangerously-skip-permissions` flag

## Migration Guide

### Moving from Windows to Linux

If you're migrating your workflow:

1. **Account numbers stay the same**: Account 5 on Windows = Account 5 on Linux
2. **Commands are nearly identical**: `c 5` works on both
3. **Only flag syntax changes**: `-NoLaunch` → `--no-launch`

### Transferring Account Data

To copy account data from Windows to Linux:

**Windows (PowerShell)**:
```powershell
# Export account 5
Compress-Archive -Path "$env:USERPROFILE\.claude5" -DestinationPath claude5.zip
```

**Linux (Bash)**:
```bash
# Import account 5
unzip claude5.zip -d $HOME/.claude5
```

## Troubleshooting Comparison

| Issue | PowerShell Solution | Bash Solution |
|-------|-------------------|---------------|
| Aliases not working | `. $PROFILE` | `source ~/.bashrc` |
| Script won't run | `Set-ExecutionPolicy RemoteSigned` | `chmod +x script.sh` |
| Line ending issues | N/A (native Windows) | `sed -i 's/\r$//' script.sh` |
| Permission denied | Run as Administrator | `sudo` or `chmod +x` |
| JSON update fails | Check PowerShell version | Install `jq`: `sudo apt install jq` |

## Cross-Platform Workflows

### Using Both Windows and Linux

If you work on both platforms:

1. Use same account numbers for same purposes
2. Sync `.claude<N>` directories between machines (optional)
3. Use same commands (minor flag syntax changes)
4. Both systems maintain isolation and safety

### Example Dual Setup

**Windows machine**:
```powershell
c 1   # Personal experiments
c 2   # Work project A
c 3   # Work project B
```

**Linux machine** (same account purposes):
```bash
c 1   # Personal experiments (same as Windows)
c 2   # Work project A (same as Windows)
c 3   # Work project B (same as Windows)
```

Optionally sync the `.claude1`, `.claude2`, `.claude3` directories between machines.

---

**See Also**:
- Full documentation: `CLAUDE_MULTI_ACCOUNT_SETUP.md`
- Quick reference: `README_CLAUDE_ACCOUNTS.md`
- Conversion details: `LINUX_CONVERSION_SUMMARY.md`
