# ============================================================================
# Authenticate-AllProfiles.ps1
# Batch authenticate all browser profiles for Claude Code
# ============================================================================
#
# Purpose: Semi-automated batch authentication of browser profiles
# Author: Claude Code Multi-Account Automation System
# Created: 2025-11-10
#
# Usage:
#   Authenticate-AllProfiles                        # Authenticate all profiles
#   Authenticate-AllProfiles -AccountNums 1,5,12    # Authenticate specific accounts
#   Authenticate-AllProfiles -OnlyExpired           # Only expired accounts
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [int[]]$AccountNums,

    [Parameter(Mandatory=$false)]
    [switch]$OnlyExpired,

    [Parameter(Mandatory=$false)]
    [int]$DelaySeconds = 45
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

function Get-ExpiredAccounts {
    $AllAccounts = @(1..28 + 100..103)
    $expired = @()

    foreach ($acc in $AllAccounts) {
        $credFile = "$env:USERPROFILE\.claude$acc\.credentials.json"
        if (Test-Path $credFile) {
            try {
                $cred = Get-Content $credFile -Raw | ConvertFrom-Json
                $expiresAt = $cred.claudeAiOauth.expiresAt
                $expireDate = [DateTimeOffset]::FromUnixTimeMilliseconds($expiresAt).LocalDateTime
                if ((Get-Date) -gt $expireDate) {
                    $expired += $acc
                }
            } catch {}
        } else {
            $expired += $acc
        }
    }

    return $expired
}

function Start-BrowserForAuth {
    param(
        [string]$BrowserName,
        [string]$ProfileName,
        [int]$AccountNum
    )

    $paths = switch ($BrowserName) {
        'Chrome' {
            @{
                Executable = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                Args = @(
                    "--profile-directory=$ProfileName",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "https://claude.com"
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
                    "https://claude.com"
                )
            }
        }
        'Firefox' {
            @{
                Executable = "C:\Program Files\Mozilla Firefox\firefox.exe"
                Args = @(
                    "-P", $ProfileName,
                    "--no-remote",
                    "https://claude.com"
                )
            }
        }
    }

    if (-not (Test-Path $paths.Executable)) {
        Write-Error "$BrowserName not found at $($paths.Executable)"
        return $false
    }

    Write-Info "Opening $BrowserName with profile for account $AccountNum..."
    Start-Process $paths.Executable -ArgumentList $paths.Args

    return $true
}

function Invoke-ProfileAuthentication {
    param([int]$AccountNum, [string]$BrowserName, [string]$ProfileName)

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  AUTHENTICATING ACCOUNT $AccountNum" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    # Open browser with profile
    if (-not (Start-BrowserForAuth -BrowserName $BrowserName -ProfileName $ProfileName -AccountNum $AccountNum)) {
        Write-Error "Failed to start browser"
        return $false
    }

    Write-Info "Browser opened with profile for account $AccountNum"
    Write-Host ""
    Write-Host "STEPS TO COMPLETE:" -ForegroundColor Yellow
    Write-Host "  1. Log in to claude.com with your Anthropic account" -ForegroundColor White
    Write-Host "  2. Check 'Stay logged in' or 'Remember me'" -ForegroundColor White
    Write-Host "  3. Verify you see the Claude dashboard" -ForegroundColor White
    Write-Host "  4. Close the browser window" -ForegroundColor White
    Write-Host "  5. Return here and press Enter" -ForegroundColor White
    Write-Host ""

    Read-Host "Press Enter after completing authentication"

    Write-Success "Account $AccountNum authentication complete"
    return $true
}

# ============================================================================
# Main Logic
# ============================================================================

$config = Get-ProfileConfig
if (-not $config) {
    exit 1
}

$browser = $config.Browser
$profiles = $config.Profiles

# Determine which accounts to authenticate
$targetAccounts = if ($AccountNums) {
    $AccountNums
} elseif ($OnlyExpired) {
    Get-ExpiredAccounts
} else {
    $profiles.PSObject.Properties.Name | ForEach-Object { [int]$_ }
}

if ($targetAccounts.Count -eq 0) {
    Write-Warning "No accounts to authenticate"
    exit 0
}

Write-Info "Authenticating $($targetAccounts.Count) accounts using $browser"
Write-Host ""
Write-Host "This will open each browser profile one at a time." -ForegroundColor Yellow
Write-Host "You'll need to log in to claude.com for each account." -ForegroundColor Yellow
Write-Host "Estimated time: $($targetAccounts.Count * 2) minutes (2 min per account)" -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Continue? (y/n)"
if ($confirm -ne 'y') {
    Write-Info "Authentication cancelled"
    exit 0
}

$authenticated = 0
$failed = 0

foreach ($acc in $targetAccounts) {
    $profile = $profiles.$acc

    if (-not $profile) {
        Write-Warning "Account $acc has no browser profile configured. Skipping."
        $failed++
        continue
    }

    if (Invoke-ProfileAuthentication -AccountNum $acc -BrowserName $browser -ProfileName $profile.ProfileName) {
        $authenticated++
    } else {
        $failed++
    }

    # Delay between accounts
    if ($acc -ne $targetAccounts[-1]) {
        Write-Info "Waiting $DelaySeconds seconds before next account..."
        Start-Sleep -Seconds $DelaySeconds
    }
}

Write-Host "`n========================================" -ForegroundColor White
Write-Host "  AUTHENTICATION COMPLETE" -ForegroundColor White
Write-Host "========================================" -ForegroundColor White
Write-Host "  Authenticated: $authenticated" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor Red
Write-Host "========================================`n" -ForegroundColor White

Write-Info "Next step: Run .\Auto-RefreshToken-Browser.ps1 to test automatic token refresh"

exit 0
