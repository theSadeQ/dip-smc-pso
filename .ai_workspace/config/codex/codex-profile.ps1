# ============================================================================
# codex-profile.ps1
# PowerShell Profile Integration for Codex CLI Multi-Account System
# ============================================================================
#
# Purpose: Add account switching aliases to PowerShell profile
# Author: Codex CLI Multi-Account System
# Created: 2026-02-16
#
# Installation:
#   1. Copy this file to your PowerShell profile location
#   2. Add this line to your $PROFILE:
#      . D:\Projects\main\.ai_workspace\config\codex\codex-profile.ps1
#   3. Reload profile: . $PROFILE
#
# ============================================================================

# Import the switcher function
$CodexSwitcherPath = "D:\Tools\Codex\Switch-CodexAccount.ps1"

if (Test-Path $CodexSwitcherPath) {
    # Create the main switching function
    function Switch-CodexAccount {
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

        & $CodexSwitcherPath @PSBoundParameters
    }

    # Create a smart function that handles cox {number} pattern
    # Mirrors the 'c' function for Claude Code
    function global:x {
        param(
            [Parameter(Mandatory=$true, Position=0)]
            [int]$AccountNum,

            [Parameter(Mandatory=$false)]
            [switch]$NoLaunch
        )

        if ($NoLaunch) {
            & $CodexSwitcherPath -AccountNum $AccountNum -NoLaunch
        } else {
            & $CodexSwitcherPath -AccountNum $AccountNum
        }
    }

    Write-Host "[INFO] Use 'x [number]' for accounts. Examples: 'x 1', 'x 9', 'x 49999'" -ForegroundColor Gray

    # Additional helpful aliases (mirrors claude-status, claude-primary, etc.)
    function global:codex-status {
        & $CodexSwitcherPath -Validate
    }

    function global:codex-primary {
        param([switch]$NoLaunch)

        if ($NoLaunch) {
            & $CodexSwitcherPath -Primary -NoLaunch
        } else {
            & $CodexSwitcherPath -Primary
        }
    }

    function global:codex-whoami {
        if (-not $env:CODEX_HOME) {
            Write-Host "Current account: " -NoNewline -ForegroundColor Cyan
            Write-Host "primary" -ForegroundColor White
            Write-Host "Location: $env:USERPROFILE\.codex" -ForegroundColor Gray
        }
        else {
            if ($env:CODEX_HOME -match '\.codex(\d+)$') {
                $accountNum = $Matches[1]
                Write-Host "Current account: " -NoNewline -ForegroundColor Cyan
                Write-Host $accountNum -ForegroundColor White
                Write-Host "Location: $env:CODEX_HOME" -ForegroundColor Gray

                $authFile = Join-Path $env:CODEX_HOME "auth.json"
                if (Test-Path $authFile) {
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
                Write-Host "CODEX_HOME: $env:CODEX_HOME" -ForegroundColor Gray
            }
        }
    }

    function global:code-x {
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

        & $CodexSwitcherPath -AccountNum $AccountNum -NoLaunch *>$null

        $accountDir = "$env:USERPROFILE\.codex$AccountNum"
        $env:CODEX_HOME = $accountDir

        Write-Host "[OK] Launching VSCode with Codex Account $AccountNum" -ForegroundColor Green
        Write-Host "     CODEX_HOME: $env:CODEX_HOME" -ForegroundColor Gray

        & code @Path
    }

    function global:code-x-primary {
        param(
            [Parameter(Mandatory=$false, ValueFromRemainingArguments=$true)]
            [string[]]$Path = @(".")
        )

        if ($env:CODEX_HOME) {
            Remove-Item Env:\CODEX_HOME
        }

        Write-Host "[OK] Launching VSCode with primary Codex account" -ForegroundColor Green
        Write-Host "     Using: $env:USERPROFILE\.codex" -ForegroundColor Gray

        & code @Path
    }

    function global:codex-help {
        Write-Host "Codex CLI Multi-Account Switcher" -ForegroundColor Cyan
        Write-Host "=================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Quick switch:" -ForegroundColor Yellow
        Write-Host "  x [number]            Switch to account (1-50000)" -ForegroundColor White
        Write-Host "  Example: x 15         Switches to account 15" -ForegroundColor Gray
        Write-Host "  Example: x 2          Switches to account 2" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Yellow
        Write-Host "  codex-whoami          Show current active account" -ForegroundColor White
        Write-Host "  codex-primary         Switch back to primary .codex" -ForegroundColor White
        Write-Host "  codex-status          Show all accounts and auth status" -ForegroundColor White
        Write-Host "  codex-help            Show this help message" -ForegroundColor White
        Write-Host ""
        Write-Host "VSCode Integration:" -ForegroundColor Yellow
        Write-Host "  code-x [number] [path]" -ForegroundColor White
        Write-Host "                        Launch VSCode with specific Codex account" -ForegroundColor Gray
        Write-Host "  Example: code-x 2 .   Opens current dir with account 2" -ForegroundColor Gray
        Write-Host "  code-x-primary [path]" -ForegroundColor White
        Write-Host "                        Launch VSCode with primary account" -ForegroundColor White
        Write-Host ""
        Write-Host "Options:" -ForegroundColor Yellow
        Write-Host "  x [number] -NoLaunch" -ForegroundColor White
        Write-Host "                        Switch account without launching Codex" -ForegroundColor Gray
        Write-Host "  codex-primary -NoLaunch" -ForegroundColor White
        Write-Host "                        Switch to primary without launching" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Advanced:" -ForegroundColor Yellow
        Write-Host "  Switch-CodexAccount -AccountNum 5 -NoLaunch" -ForegroundColor White
        Write-Host "  Switch-CodexAccount -Primary" -ForegroundColor White
        Write-Host "  Switch-CodexAccount -Validate" -ForegroundColor White
        Write-Host ""
    }

    Write-Host "[OK] Codex CLI multi-account switcher loaded" -ForegroundColor Green
    Write-Host "     Type 'codex-help' for usage instructions" -ForegroundColor Gray

} else {
    Write-Host "[WARN] Codex CLI switcher not found at: $CodexSwitcherPath" -ForegroundColor Yellow
}
