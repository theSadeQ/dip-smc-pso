# ============================================================================
# Monitor-ClaudeTokens.ps1
# Auto-monitor OAuth tokens and alert before expiration
# ============================================================================
#
# Purpose: Continuous monitoring of Claude Code OAuth tokens
# Author: Claude Code Token Management System
# Created: 2025-11-10
#
# Usage:
#   Monitor-ClaudeTokens                    # One-time check all accounts
#   Monitor-ClaudeTokens -Watch             # Continuous monitoring
#   Monitor-ClaudeTokens -AccountNum 12     # Check specific account
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [int]$AccountNum,

    [Parameter(Mandatory=$false)]
    [switch]$Watch,

    [Parameter(Mandatory=$false)]
    [int]$IntervalMinutes = 30,

    [Parameter(Mandatory=$false)]
    [int]$WarningHours = 2
)

# Configuration
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
        return @{
            Exists = $false
            Account = $AccNum
        }
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
            MinutesLeft = $timeLeft.TotalMinutes
            IsExpired = $hoursLeft -lt 0
            NeedsRefresh = $hoursLeft -lt $WarningHours
            LastModified = (Get-Item $credFile).LastWriteTime
        }
    } catch {
        return @{
            Exists = $false
            Account = $AccNum
            Error = $_.Exception.Message
        }
    }
}

function Show-TokenStatus {
    param([hashtable]$Status)

    $acc = $Status.Account

    if (-not $Status.Exists) {
        if ($Status.Error) {
            Write-Error "Account $acc`: Parse error - $($Status.Error)"
        } else {
            Write-Info "Account $acc`: No credentials"
        }
        return
    }

    $hoursLeft = [math]::Round($Status.HoursLeft, 1)
    $expiresAt = $Status.ExpiresAt.ToString("yyyy-MM-dd HH:mm:ss")

    if ($Status.IsExpired) {
        Write-Error "Account $acc`: EXPIRED (expired at $expiresAt)"
    } elseif ($Status.NeedsRefresh) {
        Write-Warning "Account $acc`: $hoursLeft hours left (expires at $expiresAt)"
    } else {
        Write-Success "Account $acc`: $hoursLeft hours left (expires at $expiresAt)"
    }
}

function Send-ExpirationAlert {
    param([hashtable]$Status)

    $acc = $Status.Account
    $hoursLeft = [math]::Round($Status.HoursLeft, 1)
    $expiresAt = $Status.ExpiresAt.ToString("HH:mm:ss")

    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "  TOKEN EXPIRATION ALERT" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Account: $acc" -ForegroundColor Yellow
    Write-Host "Time left: $hoursLeft hours" -ForegroundColor Yellow
    Write-Host "Expires at: $expiresAt" -ForegroundColor Yellow
    Write-Host "`nAction required:" -ForegroundColor White
    Write-Host "  1. Switch to account: c $acc" -ForegroundColor Cyan
    Write-Host "  2. Run: /login" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Red

    # Windows notification (if running interactively)
    if (-not $env:TERM) {
        $wshell = New-Object -ComObject Wscript.Shell
        $wshell.Popup("Claude Code Account $acc token expires in $hoursLeft hours. Run /login to refresh.", 0, "Token Expiration Alert", 48)
    }
}

function Monitor-Accounts {
    param([int[]]$Accounts)

    $expiringSoon = @()
    $expired = @()
    $healthy = @()

    foreach ($acc in $Accounts) {
        $status = Get-TokenStatus -AccNum $acc

        if (-not $status.Exists) {
            continue
        }

        Show-TokenStatus -Status $status

        if ($status.IsExpired) {
            $expired += $status
        } elseif ($status.NeedsRefresh) {
            $expiringSoon += $status
        } else {
            $healthy += $status
        }
    }

    Write-Host "`n========================================" -ForegroundColor White
    Write-Host "Summary:" -ForegroundColor White
    Write-Host "  Healthy: $($healthy.Count)" -ForegroundColor Green
    Write-Host "  Expiring soon: $($expiringSoon.Count)" -ForegroundColor Yellow
    Write-Host "  Expired: $($expired.Count)" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor White

    # Send alerts for accounts expiring soon
    foreach ($status in $expiringSoon) {
        Send-ExpirationAlert -Status $status
    }

    # Send alerts for expired accounts
    foreach ($status in $expired) {
        Send-ExpirationAlert -Status $status
    }

    return @{
        Healthy = $healthy
        ExpiringSoon = $expiringSoon
        Expired = $expired
    }
}

# ============================================================================
# Main Logic
# ============================================================================

if ($AccountNum) {
    # Check specific account
    Write-Info "Checking account $AccountNum..."
    $status = Get-TokenStatus -AccNum $AccountNum
    Show-TokenStatus -Status $status

    if ($status.NeedsRefresh -or $status.IsExpired) {
        Send-ExpirationAlert -Status $status
    }

    exit 0
}

# Check all accounts
Write-Info "Checking all Claude Code accounts..."
Write-Host ""

if ($Watch) {
    # Continuous monitoring mode
    Write-Info "Starting continuous monitoring (interval: $IntervalMinutes minutes)"
    Write-Info "Warning threshold: $WarningHours hours"
    Write-Info "Press Ctrl+C to stop"
    Write-Host ""

    while ($true) {
        $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        Write-Host "`n========== Monitor Run: $timestamp ==========" -ForegroundColor Cyan

        Monitor-Accounts -Accounts $AllAccounts

        Write-Info "Next check in $IntervalMinutes minutes..."
        Start-Sleep -Seconds ($IntervalMinutes * 60)
    }
} else {
    # One-time check
    Monitor-Accounts -Accounts $AllAccounts
}

exit 0
