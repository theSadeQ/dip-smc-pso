# ============================================================================
# claude-profile.ps1
# PowerShell Profile Integration for Claude Code Multi-Account System
# ============================================================================
#
# Purpose: Add account switching aliases to PowerShell profile
# Author: Claude Code Multi-Account System
# Created: 2025-10-11
#
# Installation:
#   1. Copy this file to your PowerShell profile location
#   2. Add this line to your $PROFILE:
#      . D:\Projects\main\.dev_tools\claude-profile.ps1
#   3. Reload profile: . $PROFILE
#
# ============================================================================

# Import the switcher function
$SwitcherPath = "D:\Projects\main\.dev_tools\Switch-ClaudeAccount.ps1"

if (Test-Path $SwitcherPath) {
    # Create the main switching function
    function Switch-ClaudeAccount {
        param(
            [Parameter(Mandatory=$false)]
            [int]$AccountNum,

            [Parameter(Mandatory=$false)]
            [switch]$Primary,

            [Parameter(Mandatory=$false)]
            [switch]$NoLaunch,

            [Parameter(Mandatory=$false)]
            [switch]$Validate
        )

        & $SwitcherPath @PSBoundParameters
    }

    # Create a smart function that handles c{number} pattern
    # This avoids PowerShell's 4096 alias limit
    function global:c {
        param(
            [Parameter(Mandatory=$true, Position=0)]
            [int]$AccountNum,

            [Parameter(Mandatory=$false)]
            [switch]$NoLaunch
        )

        if ($NoLaunch) {
            & $SwitcherPath -AccountNum $AccountNum -NoLaunch
        } else {
            & $SwitcherPath -AccountNum $AccountNum
        }
    }

    Write-Host "[INFO] Use 'c [number]' for accounts. Examples: 'c 1', 'c 9', 'c 49999'" -ForegroundColor Gray

    # Additional helpful aliases
    function global:claude-status {
        & $SwitcherPath -Validate
    }

    function global:claude-primary {
        param([switch]$NoLaunch)

        if ($NoLaunch) {
            & $SwitcherPath -Primary -NoLaunch
        } else {
            & $SwitcherPath -Primary
        }
    }

    function global:claude-whoami {
        if (-not $env:CLAUDE_CONFIG_DIR) {
            Write-Host "Current account: " -NoNewline -ForegroundColor Cyan
            Write-Host "primary" -ForegroundColor White
            Write-Host "Location: $env:USERPROFILE\.claude" -ForegroundColor Gray
        }
        else {
            if ($env:CLAUDE_CONFIG_DIR -match '\.claude(\d+)$') {
                $accountNum = $Matches[1]
                Write-Host "Current account: " -NoNewline -ForegroundColor Cyan
                Write-Host $accountNum -ForegroundColor White
                Write-Host "Location: $env:CLAUDE_CONFIG_DIR" -ForegroundColor Gray

                $credFile = Join-Path $env:CLAUDE_CONFIG_DIR ".credentials.json"
                if (Test-Path $credFile) {
                    Write-Host "Auth status: " -NoNewline -ForegroundColor Gray
                    Write-Host "Authenticated" -ForegroundColor Green
                } else {
                    Write-Host "Auth status: " -NoNewline -ForegroundColor Gray
                    Write-Host "Needs login" -ForegroundColor Yellow
                }
            }
            else {
                Write-Host "Current account: " -NoNewline -ForegroundColor Cyan
                Write-Host "unknown" -ForegroundColor Yellow
                Write-Host "CLAUDE_CONFIG_DIR: $env:CLAUDE_CONFIG_DIR" -ForegroundColor Gray
            }
        }
    }

    function global:code-c {
        param(
            [Parameter(Mandatory=$true, Position=0)]
            [int]$AccountNum,

            [Parameter(Mandatory=$false, Position=1, ValueFromRemainingArguments=$true)]
            [string[]]$Path = @(".")
        )

        if ($AccountNum -lt 1 -or $AccountNum -gt 50000) {
            Write-Host "[ERROR] Account number must be between 1 and 50000" -ForegroundColor Red
            return
        }

        & $SwitcherPath -AccountNum $AccountNum -NoLaunch *>$null

        $accountDir = "$env:USERPROFILE\.claude$AccountNum"
        $env:CLAUDE_CONFIG_DIR = $accountDir

        Write-Host "[OK] Launching VSCode with Account $AccountNum" -ForegroundColor Green
        Write-Host "     CLAUDE_CONFIG_DIR: $env:CLAUDE_CONFIG_DIR" -ForegroundColor Gray

        $env:CLAUDE_CONFIG_DIR = $accountDir
        & code @Path
    }

    function global:code-primary {
        param(
            [Parameter(Mandatory=$false, ValueFromRemainingArguments=$true)]
            [string[]]$Path = @(".")
        )

        if ($env:CLAUDE_CONFIG_DIR) {
            Remove-Item Env:\CLAUDE_CONFIG_DIR
        }

        Write-Host "[OK] Launching VSCode with primary account" -ForegroundColor Green
        Write-Host "     Using: $env:USERPROFILE\.claude" -ForegroundColor Gray

        & code @Path
    }

    function global:claude-help {
        Write-Host "Claude Code Multi-Account Switcher" -ForegroundColor Cyan
        Write-Host "====================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Quick switch:" -ForegroundColor Yellow
        Write-Host "  c [number]            Switch to account (1-50000)" -ForegroundColor White
        Write-Host "  Example: c 15         Switches to account 15" -ForegroundColor Gray
        Write-Host "  Example: c 2          Switches to account 2" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Yellow
        Write-Host "  claude-whoami         Show current active account" -ForegroundColor White
        Write-Host "  claude-primary        Switch back to primary .claude" -ForegroundColor White
        Write-Host "  claude-status         Show all accounts and auth status" -ForegroundColor White
        Write-Host "  claude-help           Show this help message" -ForegroundColor White
        Write-Host ""
        Write-Host "VSCode Integration:" -ForegroundColor Yellow
        Write-Host "  code-c [number] [path]" -ForegroundColor White
        Write-Host "                        Launch VSCode with specific account" -ForegroundColor Gray
        Write-Host "  Example: code-c 2 .   Opens current dir with account 2" -ForegroundColor Gray
        Write-Host "  code-primary [path]   Launch VSCode with primary account" -ForegroundColor White
        Write-Host ""
        Write-Host "Options:" -ForegroundColor Yellow
        Write-Host "  c [number] -NoLaunch" -ForegroundColor White
        Write-Host "                        Switch account without launching Claude" -ForegroundColor Gray
        Write-Host "  claude-primary -NoLaunch" -ForegroundColor White
        Write-Host "                        Switch to primary without launching" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Advanced:" -ForegroundColor Yellow
        Write-Host "  Switch-ClaudeAccount -AccountNum 5 -NoLaunch" -ForegroundColor White
        Write-Host "  Switch-ClaudeAccount -Primary" -ForegroundColor White
        Write-Host "  Switch-ClaudeAccount -Validate" -ForegroundColor White
        Write-Host ""
    }

    Write-Host "[OK] Claude Code multi-account switcher loaded" -ForegroundColor Green
    Write-Host "     Type 'claude-help' for usage instructions" -ForegroundColor Gray

} else {
    Write-Host "[WARN] Claude Code switcher not found at: $SwitcherPath" -ForegroundColor Yellow
}
