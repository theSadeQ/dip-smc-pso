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

    Write-Host "[INFO] Use 'c <number>' for accounts. Examples: 'c 1', 'c 9', 'c 49999'" -ForegroundColor Gray

    # Additional helpful aliases
    function global:claude-status {
        & $SwitcherPath -Validate
    }

    function global:claude-primary {
        & $SwitcherPath -Primary
    }

    function global:claude-help {
        Write-Host "Claude Code Multi-Account Switcher" -ForegroundColor Cyan
        Write-Host "====================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Quick switch:" -ForegroundColor Yellow
        Write-Host "  c <number>            Switch to account (1-50000)" -ForegroundColor White
        Write-Host "  Example: c 15         # Switches to account 15" -ForegroundColor Gray
        Write-Host "  Example: c 49999      # Switches to account 49999" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Yellow
        Write-Host "  claude-primary        Switch back to primary .claude" -ForegroundColor White
        Write-Host "  claude-status         Show all accounts and auth status" -ForegroundColor White
        Write-Host "  claude-help           Show this help message" -ForegroundColor White
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
