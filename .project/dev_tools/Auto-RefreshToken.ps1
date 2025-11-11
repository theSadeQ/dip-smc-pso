# ============================================================================
# Auto-RefreshToken.ps1
# Automated token refresh helper for Claude Code
# ============================================================================
#
# Purpose: Semi-automated token refresh workflow
# Author: Claude Code Token Management System
# Created: 2025-11-10
#
# Usage:
#   Auto-RefreshToken                           # Refresh current account
#   Auto-RefreshToken -AccountNum 12            # Refresh specific account
#   Auto-RefreshToken -RefreshAll               # Refresh all expiring accounts
#
# Note: Cannot fully automate login (requires browser OAuth flow)
#       This script automates everything EXCEPT the actual /login command
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [int]$AccountNum,

    [Parameter(Mandatory=$false)]
    [switch]$RefreshAll,

    [Parameter(Mandatory=$false)]
    [int]$WarningHours = 2
)

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SwitcherScript = Join-Path $ScriptDir "Switch-ClaudeAccount.ps1"
$AllAccounts = @(1..28 + 100..103)

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Get-TokenStatus {
    param([int]$AccNum)

    $credFile = "$env:USERPROFILE\.claude$AccNum\.credentials.json"

    if (-not (Test-Path $credFile)) {
        return @{ Exists = $false; Account = $AccNum }
    }

    try {
        $cred = Get-Content $credFile -Raw | ConvertFrom-Json
        $expiresAt = $cred.claudeAiOauth.expiresAt
        $expireDate = [DateTimeOffset]::FromUnixTimeMilliseconds($expiresAt).LocalDateTime
        $now = Get-Date
        $timeLeft = $expireDate - $now
        $hoursLeft = $timeLeft.TotalHours

        return @{
            Exists = $true
            Account = $AccNum
            ExpiresAt = $expireDate
            HoursLeft = $hoursLeft
            IsExpired = $hoursLeft -lt 0
            NeedsRefresh = $hoursLeft -lt $WarningHours
        }
    } catch {
        return @{ Exists = $false; Account = $AccNum }
    }
}

function Invoke-TokenRefresh {
    param([int]$AccNum)

    Write-Info "Refreshing token for account $AccNum..."

    # Get current status
    $status = Get-TokenStatus -AccNum $AccNum

    if (-not $status.Exists) {
        Write-Error "Account $AccNum has no credentials file"
        return $false
    }

    $hoursLeft = [math]::Round($status.HoursLeft, 1)

    if ($status.IsExpired) {
        Write-Warning "Token EXPIRED (needs immediate refresh)"
    } elseif ($status.NeedsRefresh) {
        Write-Warning "Token expires in $hoursLeft hours (refresh recommended)"
    } else {
        Write-Success "Token is healthy ($hoursLeft hours left)"
        $confirm = Read-Host "Token is still valid. Refresh anyway? (y/n)"
        if ($confirm -ne 'y') {
            return $false
        }
    }

    # Switch to account
    Write-Info "Switching to account $AccNum..."
    & $SwitcherScript -AccountNum $AccNum -NoLaunch

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to switch to account $AccNum"
        return $false
    }

    # Instructions for manual login
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  MANUAL LOGIN REQUIRED" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Next steps:" -ForegroundColor White
    Write-Host "  1. Open a NEW terminal window" -ForegroundColor Yellow
    Write-Host "  2. Run: claude" -ForegroundColor Yellow
    Write-Host "  3. Type: /login" -ForegroundColor Yellow
    Write-Host "  4. Complete the browser OAuth flow" -ForegroundColor Yellow
    Write-Host "  5. Return here and press Enter" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Cyan

    Read-Host "Press Enter after completing /login in Claude Code"

    # Verify refresh
    Start-Sleep -Seconds 2
    $newStatus = Get-TokenStatus -AccNum $AccNum

    if ($newStatus.Exists) {
        $newHoursLeft = [math]::Round($newStatus.HoursLeft, 1)

        if ($newStatus.HoursLeft -gt $status.HoursLeft) {
            Write-Success "Token refreshed successfully! New expiration: $newHoursLeft hours"
            return $true
        } else {
            Write-Warning "Token may not have been refreshed (still $newHoursLeft hours left)"
            return $false
        }
    } else {
        Write-Error "Failed to verify token refresh"
        return $false
    }
}

function Invoke-RefreshAll {
    Write-Info "Checking all accounts for expiring tokens..."

    $needsRefresh = @()

    foreach ($acc in $AllAccounts) {
        $status = Get-TokenStatus -AccNum $acc

        if ($status.Exists -and ($status.IsExpired -or $status.NeedsRefresh)) {
            $needsRefresh += $status
        }
    }

    if ($needsRefresh.Count -eq 0) {
        Write-Success "All accounts have healthy tokens!"
        return
    }

    Write-Warning "Found $($needsRefresh.Count) account(s) needing refresh:"
    foreach ($status in $needsRefresh) {
        $hoursLeft = [math]::Round($status.HoursLeft, 1)
        Write-Host "  - Account $($status.Account): $hoursLeft hours left" -ForegroundColor Yellow
    }

    Write-Host ""
    $confirm = Read-Host "Refresh all $($needsRefresh.Count) account(s)? (y/n)"

    if ($confirm -ne 'y') {
        Write-Info "Refresh cancelled"
        return
    }

    # Refresh each account
    $refreshed = 0
    foreach ($status in $needsRefresh) {
        Write-Host "`n========== Refreshing Account $($status.Account) ==========" -ForegroundColor Cyan

        if (Invoke-TokenRefresh -AccNum $status.Account) {
            $refreshed++
        }
    }

    Write-Host "`n========================================" -ForegroundColor White
    Write-Success "Refreshed $refreshed out of $($needsRefresh.Count) account(s)"
    Write-Host "========================================`n" -ForegroundColor White
}

# ============================================================================
# Main Logic
# ============================================================================

if ($RefreshAll) {
    Invoke-RefreshAll
    exit 0
}

# Get current or specified account
if (-not $AccountNum) {
    $configDir = [Environment]::GetEnvironmentVariable("CLAUDE_CONFIG_DIR", "User")

    if ($configDir -and $configDir -match '\.claude(\d+)$') {
        $AccountNum = [int]$Matches[1]
        Write-Info "Using current account: $AccountNum"
    } else {
        Write-Error "No account specified and CLAUDE_CONFIG_DIR not set"
        Write-Info "Usage: Auto-RefreshToken -AccountNum 12"
        exit 1
    }
}

# Refresh specific account
Invoke-TokenRefresh -AccNum $AccountNum

exit 0
