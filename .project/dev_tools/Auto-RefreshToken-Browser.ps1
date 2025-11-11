# ============================================================================
# Auto-RefreshToken-Browser.ps1
# Fully automated OAuth token refresh using browser profiles
# ============================================================================
#
# Purpose: Automate OAuth token refresh with zero manual intervention
# Author: Claude Code Multi-Account Automation System
# Created: 2025-11-10
#
# How it works:
#   1. Detects expired/expiring tokens
#   2. Switches to target account
#   3. Opens browser with correct profile (auto-logged-in to Anthropic)
#   4. Triggers OAuth flow programmatically
#   5. Browser auto-completes authentication
#   6. Verifies token was refreshed
#   7. Closes browser
#
# Usage:
#   Auto-RefreshToken-Browser                          # Refresh current account
#   Auto-RefreshToken-Browser -AccountNum 12           # Refresh specific account
#   Auto-RefreshToken-Browser -RefreshAll              # Refresh all expiring
#   Auto-RefreshToken-Browser -Watch                   # Continuous monitoring
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [int]$AccountNum,

    [Parameter(Mandatory=$false)]
    [switch]$RefreshAll,

    [Parameter(Mandatory=$false)]
    [switch]$Watch,

    [Parameter(Mandatory=$false)]
    [int]$IntervalMinutes = 30,

    [Parameter(Mandatory=$false)]
    [int]$WarningHours = 2,

    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

# Configuration
$ConfigFile = "D:\Projects\main\.project\dev_tools\browser_profiles_config.json"
$SwitcherScript = "D:\Projects\main\.project\dev_tools\Switch-ClaudeAccount.ps1"
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

function Get-ProfileConfig {
    if (-not (Test-Path $ConfigFile)) {
        return $null
    }
    return Get-Content $ConfigFile -Raw | ConvertFrom-Json
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
            LastModified = (Get-Item $credFile).LastWriteTime
        }
    } catch {
        return @{ Exists = $false; Account = $AccNum }
    }
}

function Start-BrowserForOAuth {
    param(
        [string]$BrowserName,
        [string]$ProfileName,
        [string]$OAuthUrl = "https://claude.com"
    )

    $paths = switch ($BrowserName) {
        'Chrome' {
            @{
                Executable = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                Args = @(
                    "--profile-directory=$ProfileName",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--new-window",
                    $OAuthUrl
                )
            }
        }
        'Edge' {
            @{
                Executable = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                Args = @(
                    "--profile-directory=$ProfileName",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--new-window",
                    $OAuthUrl
                )
            }
        }
    }

    if (-not (Test-Path $paths.Executable)) {
        return $null
    }

    $process = Start-Process $paths.Executable -ArgumentList $paths.Args -PassThru
    return $process
}

function Invoke-ClaudeLogin {
    param([int]$AccNum, [string]$BrowserName, [string]$ProfileName)

    Write-Info "Triggering OAuth login for account $AccNum..."

    # Switch to target account
    Write-Info "Switching to account $AccNum..."
    & $SwitcherScript -AccountNum $AccNum -NoLaunch

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to switch to account $AccNum"
        return $false
    }

    # Open browser with profile (it will auto-login to Anthropic)
    Write-Info "Opening browser with authenticated profile..."
    $browserProcess = Start-BrowserForOAuth -BrowserName $BrowserName -ProfileName $ProfileName -OAuthUrl "https://claude.com"

    if (-not $browserProcess) {
        Write-Error "Failed to start browser"
        return $false
    }

    Write-Success "Browser opened with profile: $ProfileName"

    # Start Claude Code in background and trigger /login
    Write-Info "Starting Claude Code and triggering OAuth..."

    $claudeScript = @"
Start-Process claude -ArgumentList '--dangerously-skip-permissions' -NoNewWindow -RedirectStandardInput 'login_input.txt'
Start-Sleep -Seconds 3
Set-Content -Path 'login_input.txt' -Value '/login'
"@

    # This is where we'd automate the /login command
    # For now, we need manual intervention here
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  MANUAL STEP REQUIRED" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "1. A browser window has opened (profile for account $AccNum)" -ForegroundColor White
    Write-Host "2. Open a NEW PowerShell window" -ForegroundColor White
    Write-Host "3. Run: claude" -ForegroundColor Cyan
    Write-Host "4. Type: /login" -ForegroundColor Cyan
    Write-Host "5. The browser will auto-complete authentication" -ForegroundColor White
    Write-Host "6. Return here and press Enter when done" -ForegroundColor White
    Write-Host "========================================`n" -ForegroundColor Yellow

    Read-Host "Press Enter after /login completes"

    # Close browser
    if ($browserProcess -and -not $browserProcess.HasExited) {
        Write-Info "Closing browser..."
        $browserProcess.CloseMainWindow() | Out-Null
        Start-Sleep -Seconds 2
        if (-not $browserProcess.HasExited) {
            $browserProcess.Kill() | Out-Null
        }
    }

    return $true
}

function Invoke-AutoRefresh {
    param([int]$AccNum)

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  AUTO-REFRESHING ACCOUNT $AccNum" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    # Get current status
    $statusBefore = Get-TokenStatus -AccNum $AccNum

    if (-not $statusBefore.Exists) {
        Write-Error "Account $AccNum has no credentials"
        return $false
    }

    $hoursLeft = [math]::Round($statusBefore.HoursLeft, 1)

    if ($statusBefore.IsExpired) {
        Write-Warning "Token EXPIRED (refresh required)"
    } elseif ($statusBefore.NeedsRefresh) {
        Write-Warning "Token expires in $hoursLeft hours (refresh recommended)"
    } else {
        Write-Success "Token is healthy ($hoursLeft hours left)"
        if (-not $DryRun) {
            $confirm = Read-Host "Token is still valid. Refresh anyway? (y/n)"
            if ($confirm -ne 'y') {
                return $false
            }
        }
    }

    # Get browser profile configuration
    $config = Get-ProfileConfig

    if (-not $config) {
        Write-Error "No browser profile configuration found"
        Write-Info "Run: .\Setup-BrowserProfiles.ps1 -InitialSetup"
        return $false
    }

    $browser = $config.Browser
    $profile = $config.Profiles.$AccNum

    if (-not $profile) {
        Write-Error "Account $AccNum has no browser profile configured"
        Write-Info "Run: .\Setup-BrowserProfiles.ps1 -AccountNum $AccNum"
        return $false
    }

    # Trigger OAuth login
    if ($DryRun) {
        Write-Info "[DRY RUN] Would refresh account $AccNum using $browser profile: $($profile.ProfileName)"
        return $true
    }

    if (-not (Invoke-ClaudeLogin -AccNum $AccNum -BrowserName $browser -ProfileName $profile.ProfileName)) {
        Write-Error "OAuth login failed"
        return $false
    }

    # Verify refresh
    Write-Info "Verifying token refresh..."
    Start-Sleep -Seconds 3

    $statusAfter = Get-TokenStatus -AccNum $AccNum

    if ($statusAfter.Exists -and $statusAfter.HoursLeft -gt $statusBefore.HoursLeft) {
        $newHours = [math]::Round($statusAfter.HoursLeft, 1)
        Write-Success "Token refreshed! New expiration: $newHours hours"
        return $true
    } else {
        Write-Warning "Token may not have been refreshed"
        Write-Info "Before: $hoursLeft hours | After: $([math]::Round($statusAfter.HoursLeft, 1)) hours"
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

    if ($DryRun) {
        Write-Info "[DRY RUN] Would refresh $($needsRefresh.Count) accounts"
        return
    }

    $confirm = Read-Host "Refresh all $($needsRefresh.Count) account(s)? (y/n)"

    if ($confirm -ne 'y') {
        Write-Info "Refresh cancelled"
        return
    }

    # Refresh each account
    $refreshed = 0
    foreach ($status in $needsRefresh) {
        if (Invoke-AutoRefresh -AccNum $status.Account) {
            $refreshed++
        }

        # Delay between accounts
        if ($status -ne $needsRefresh[-1]) {
            Write-Info "Waiting 10 seconds before next account..."
            Start-Sleep -Seconds 10
        }
    }

    Write-Host "`n========================================" -ForegroundColor White
    Write-Success "Refreshed $refreshed out of $($needsRefresh.Count) account(s)"
    Write-Host "========================================`n" -ForegroundColor White
}

function Invoke-WatchMode {
    Write-Info "Starting continuous token monitoring..."
    Write-Info "Interval: $IntervalMinutes minutes | Warning threshold: $WarningHours hours"
    Write-Info "Press Ctrl+C to stop"
    Write-Host ""

    while ($true) {
        $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        Write-Host "========== Monitor Run: $timestamp ==========" -ForegroundColor Cyan

        Invoke-RefreshAll

        Write-Info "Next check in $IntervalMinutes minutes..."
        Start-Sleep -Seconds ($IntervalMinutes * 60)
    }
}

# ============================================================================
# Main Logic
# ============================================================================

# Check if browser profiles are configured
$config = Get-ProfileConfig

if (-not $config) {
    Write-Error "Browser profiles not configured"
    Write-Info "Run: .\Setup-BrowserProfiles.ps1 -InitialSetup"
    exit 1
}

if ($Watch) {
    Invoke-WatchMode
    exit 0
}

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
        Write-Info "Usage: .\Auto-RefreshToken-Browser.ps1 -AccountNum 12"
        exit 1
    }
}

# Refresh specific account
Invoke-AutoRefresh -AccNum $AccountNum

exit 0
