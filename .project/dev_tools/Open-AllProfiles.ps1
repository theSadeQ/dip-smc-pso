# ============================================================================
# Open-AllProfiles.ps1
# Opens all Chrome profiles simultaneously for initialization
# ============================================================================
#
# Purpose: Initialize all browser profiles at once (parallel approach)
# Author: Claude Code Multi-Account Automation System
# Created: 2025-11-10
#
# Usage:
#   Open-AllProfiles                        # Open all 32 profiles
#   Open-AllProfiles -AccountNums 1,5,12    # Open specific accounts
#   Open-AllProfiles -Delay 2               # Add 2-second delay between launches
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [int[]]$AccountNums,

    [Parameter(Mandatory=$false)]
    [int]$Delay = 1,

    [Parameter(Mandatory=$false)]
    [string]$Url = "https://claude.com"
)

# Configuration
$ConfigFile = "D:\Projects\main\.project\dev_tools\browser_profiles_config.json"

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
        Write-Error "Configuration not found. Run Setup-BrowserProfiles.ps1 -InitialSetup first"
        return $null
    }

    try {
        return Get-Content $ConfigFile -Raw | ConvertFrom-Json
    } catch {
        Write-Error "Failed to load configuration: $($_.Exception.Message)"
        return $null
    }
}

function Start-ChromeProfile {
    param(
        [string]$ProfileName,
        [int]$AccountNum,
        [string]$Url
    )

    $chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

    if (-not (Test-Path $chromePath)) {
        Write-Error "Chrome not found at $chromePath"
        return $false
    }

    try {
        $args = @(
            "--profile-directory=$ProfileName",
            "--no-first-run",
            "--no-default-browser-check",
            $Url
        )

        Start-Process $chromePath -ArgumentList $args -ErrorAction Stop
        Write-Success "Opened profile for account $AccountNum"
        return $true
    } catch {
        Write-Error "Failed to open profile for account $AccountNum`: $($_.Exception.Message)"
        return $false
    }
}

# ============================================================================
# Main Logic
# ============================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CHROME PROFILE BATCH LAUNCHER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Load configuration
$config = Get-ProfileConfig
if (-not $config) {
    exit 1
}

$browser = $config.Browser
$profiles = $config.Profiles

# Verify Chrome is selected
if ($browser -ne 'Chrome') {
    Write-Error "This script only supports Chrome. Your config uses: $browser"
    Write-Info "To change browser, run: .\Setup-BrowserProfiles.ps1 -InitialSetup"
    exit 1
}

# Determine which accounts to open
$targetAccounts = if ($AccountNums) {
    $AccountNums
} else {
    $profiles.PSObject.Properties.Name | ForEach-Object { [int]$_ } | Sort-Object
}

if ($targetAccounts.Count -eq 0) {
    Write-Warning "No accounts to open"
    exit 0
}

Write-Info "Opening $($targetAccounts.Count) Chrome profiles..."
Write-Info "Target URL: $Url"
Write-Info "Delay between launches: $Delay second(s)"
Write-Host ""

# Warn about resource usage
if ($targetAccounts.Count -gt 10) {
    Write-Warning "Opening $($targetAccounts.Count) profiles will use significant RAM/CPU"
    Write-Host "  Estimated RAM: $($targetAccounts.Count * 200)MB - $($targetAccounts.Count * 400)MB" -ForegroundColor Yellow
    Write-Host "  This may slow down your system temporarily" -ForegroundColor Yellow
    Write-Host ""

    $confirm = Read-Host "Continue? (y/n)"
    if ($confirm -ne 'y') {
        Write-Info "Operation cancelled"
        exit 0
    }
    Write-Host ""
}

# Launch all profiles
$opened = 0
$failed = 0

foreach ($acc in $targetAccounts) {
    $profile = $profiles.$acc

    if (-not $profile) {
        Write-Warning "Account $acc has no browser profile configured. Skipping."
        $failed++
        continue
    }

    if (Start-ChromeProfile -ProfileName $profile.ProfileName -AccountNum $acc -Url $Url) {
        $opened++
    } else {
        $failed++
    }

    # Small delay to prevent overwhelming the system
    if ($acc -ne $targetAccounts[-1]) {
        Start-Sleep -Seconds $Delay
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor White
Write-Host "  LAUNCH COMPLETE" -ForegroundColor White
Write-Host "========================================" -ForegroundColor White
Write-Host "  Opened: $opened" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor White
Write-Host ""

Write-Info "What to do next:"
Write-Host "  1. Each Chrome window will open to claude.com" -ForegroundColor White
Write-Host "  2. Log in to each profile with your Anthropic account" -ForegroundColor White
Write-Host "  3. Check 'Stay logged in' on each" -ForegroundColor White
Write-Host "  4. Close windows when done" -ForegroundColor White
Write-Host ""
Write-Info "After all profiles are authenticated, run: .\Setup-BrowserProfiles.ps1 -ValidateProfiles"
Write-Host ""

exit 0
