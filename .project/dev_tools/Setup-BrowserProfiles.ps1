# ============================================================================
# Setup-BrowserProfiles.ps1
# Create and manage browser profiles for Claude Code OAuth automation
# ============================================================================
#
# Purpose: Automate OAuth login using dedicated browser profiles per account
# Author: Claude Code Multi-Account Automation System
# Created: 2025-11-10
#
# Strategy:
#   1. Create separate browser profile for each Claude account (1-28, 100-103)
#   2. Each profile stays logged into Anthropic automatically
#   3. OAuth redirect completes without manual intervention
#   4. Token refresh becomes fully automated
#
# Usage:
#   Setup-BrowserProfiles -Browser Chrome           # Create Chrome profiles
#   Setup-BrowserProfiles -Browser Edge             # Create Edge profiles
#   Setup-BrowserProfiles -InitialSetup             # First-time setup wizard
#   Setup-BrowserProfiles -ValidateProfiles         # Check existing profiles
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('Chrome', 'Edge', 'Firefox')]
    [string]$Browser = 'Chrome',

    [Parameter(Mandatory=$false)]
    [switch]$InitialSetup,

    [Parameter(Mandatory=$false)]
    [switch]$ValidateProfiles,

    [Parameter(Mandatory=$false)]
    [int]$AccountNum
)

# Configuration
$AllAccounts = @(1..28 + 100..103)
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

function Get-BrowserPaths {
    param([string]$BrowserName)

    switch ($BrowserName) {
        'Chrome' {
            return @{
                Executable = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                ProfileBase = "$env:LOCALAPPDATA\Google\Chrome\User Data"
                ProfilePrefix = "Claude_Account_"
            }
        }
        'Edge' {
            return @{
                Executable = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                ProfileBase = "$env:LOCALAPPDATA\Microsoft\Edge\User Data"
                ProfilePrefix = "Claude_Account_"
            }
        }
        'Firefox' {
            return @{
                Executable = "C:\Program Files\Mozilla Firefox\firefox.exe"
                ProfileBase = "$env:APPDATA\Mozilla\Firefox\Profiles"
                ProfilePrefix = "claude_account_"
            }
        }
        default {
            throw "Unsupported browser: $BrowserName"
        }
    }
}

function Test-BrowserInstalled {
    param([string]$BrowserName)

    $paths = Get-BrowserPaths -BrowserName $BrowserName

    if (Test-Path $paths.Executable) {
        Write-Success "$BrowserName is installed at: $($paths.Executable)"
        return $true
    } else {
        Write-Error "$BrowserName not found at: $($paths.Executable)"
        return $false
    }
}

function New-BrowserProfile {
    param(
        [string]$BrowserName,
        [int]$AccNum
    )

    $paths = Get-BrowserPaths -BrowserName $BrowserName
    $profileName = "$($paths.ProfilePrefix)$AccNum"
    $profilePath = Join-Path $paths.ProfileBase $profileName

    if (Test-Path $profilePath) {
        Write-Info "Profile already exists: $profileName"
        return @{
            Exists = $true
            ProfileName = $profileName
            ProfilePath = $profilePath
        }
    }

    Write-Info "Creating profile: $profileName..."

    # Create profile directory
    New-Item -ItemType Directory -Path $profilePath -Force | Out-Null

    # Initialize profile (browser will complete setup on first launch)
    Write-Success "Profile created: $profileName"

    return @{
        Exists = $true
        ProfileName = $profileName
        ProfilePath = $profilePath
        IsNew = $true
    }
}

function Start-BrowserWithProfile {
    param(
        [string]$BrowserName,
        [string]$ProfileName,
        [string]$Url = "https://claude.com"
    )

    $paths = Get-BrowserPaths -BrowserName $BrowserName

    switch ($BrowserName) {
        'Chrome' {
            $args = @(
                "--profile-directory=$ProfileName",
                "--no-first-run",
                "--no-default-browser-check",
                $Url
            )
            Start-Process $paths.Executable -ArgumentList $args
        }
        'Edge' {
            $args = @(
                "--profile-directory=$ProfileName",
                "--no-first-run",
                "--no-default-browser-check",
                $Url
            )
            Start-Process $paths.Executable -ArgumentList $args
        }
        'Firefox' {
            $args = @(
                "-P", $ProfileName,
                "--no-remote",
                $Url
            )
            Start-Process $paths.Executable -ArgumentList $args
        }
    }

    Write-Success "Launched $BrowserName with profile: $ProfileName"
}

function Save-ProfileConfig {
    param(
        [string]$BrowserName,
        [hashtable]$Profiles
    )

    # Convert hashtable with integer keys to string keys for JSON serialization
    $profilesJson = @{}
    foreach ($key in $Profiles.Keys) {
        $profilesJson[$key.ToString()] = $Profiles[$key]
    }

    $config = @{
        Browser = $BrowserName
        Profiles = $profilesJson
        LastUpdated = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
    }

    $config | ConvertTo-Json -Depth 10 | Set-Content $ConfigFile -Encoding UTF8
    Write-Success "Configuration saved: $ConfigFile"
}

function Get-ProfileConfig {
    if (-not (Test-Path $ConfigFile)) {
        return $null
    }

    try {
        $config = Get-Content $ConfigFile -Raw | ConvertFrom-Json
        return $config
    } catch {
        Write-Warning "Failed to load config: $($_.Exception.Message)"
        return $null
    }
}

function Invoke-InitialSetup {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  BROWSER PROFILE SETUP WIZARD" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    # Step 1: Choose browser
    Write-Host "Step 1: Choose your browser" -ForegroundColor Yellow
    Write-Host "  1. Google Chrome (Recommended)" -ForegroundColor White
    Write-Host "  2. Microsoft Edge" -ForegroundColor White
    Write-Host "  3. Mozilla Firefox" -ForegroundColor White
    Write-Host ""

    $browserChoice = Read-Host "Enter choice (1-3)"

    $selectedBrowser = switch ($browserChoice) {
        '1' { 'Chrome' }
        '2' { 'Edge' }
        '3' { 'Firefox' }
        default { 'Chrome' }
    }

    # Verify browser is installed
    if (-not (Test-BrowserInstalled -BrowserName $selectedBrowser)) {
        Write-Error "Please install $selectedBrowser first"
        return
    }

    # Step 2: Choose setup mode
    Write-Host "`nStep 2: Choose setup mode" -ForegroundColor Yellow
    Write-Host "  1. Create profiles for all 32 accounts (automated)" -ForegroundColor White
    Write-Host "  2. Create profiles for specific accounts (manual)" -ForegroundColor White
    Write-Host "  3. Create profiles for accounts with expired tokens" -ForegroundColor White
    Write-Host ""

    $setupChoice = Read-Host "Enter choice (1-3)"

    $targetAccounts = switch ($setupChoice) {
        '1' { $AllAccounts }
        '2' {
            $input = Read-Host "Enter account numbers (comma-separated, e.g., 1,5,12,20)"
            $input -split ',' | ForEach-Object { [int]$_.Trim() }
        }
        '3' {
            Write-Info "Checking for expired tokens..."
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
                }
            }
            Write-Info "Found $($expired.Count) expired accounts"
            $expired
        }
        default { $AllAccounts }
    }

    if ($targetAccounts.Count -eq 0) {
        Write-Error "No accounts selected"
        return
    }

    # Step 3: Create profiles
    Write-Host "`nStep 3: Creating browser profiles" -ForegroundColor Yellow
    Write-Info "Creating $($targetAccounts.Count) profiles for $selectedBrowser..."
    Write-Host ""

    $profileMap = @{}

    foreach ($acc in $targetAccounts) {
        Write-Host "Creating profile for account $acc..." -NoNewline
        $profile = New-BrowserProfile -BrowserName $selectedBrowser -AccNum $acc
        $profileMap[$acc] = $profile
        Write-Host " [DONE]" -ForegroundColor Green
    }

    # Save configuration
    Save-ProfileConfig -BrowserName $selectedBrowser -Profiles $profileMap

    # Step 4: Instructions
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  NEXT STEPS: MANUAL AUTHENTICATION" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    Write-Host "You now need to authenticate each browser profile with Anthropic:`n" -ForegroundColor White

    Write-Host "AUTOMATED APPROACH (Recommended):" -ForegroundColor Yellow
    Write-Host "  1. Run: .\Authenticate-AllProfiles.ps1" -ForegroundColor White
    Write-Host "     (This will open each profile and guide you through login)" -ForegroundColor Gray
    Write-Host ""

    Write-Host "MANUAL APPROACH:" -ForegroundColor Yellow
    Write-Host "  1. For each account, run:" -ForegroundColor White
    Write-Host "     .\Open-ProfileForAuth.ps1 -AccountNum N" -ForegroundColor Cyan
    Write-Host "  2. In the browser window that opens:" -ForegroundColor White
    Write-Host "     - Go to https://claude.com" -ForegroundColor Gray
    Write-Host "     - Log in with your Anthropic account" -ForegroundColor Gray
    Write-Host "     - Check 'Stay logged in'" -ForegroundColor Gray
    Write-Host "     - Close browser when done" -ForegroundColor Gray
    Write-Host "  3. Repeat for all $($targetAccounts.Count) accounts" -ForegroundColor White
    Write-Host ""

    Write-Host "After authentication is complete:" -ForegroundColor Yellow
    Write-Host "  - Run: .\Validate-BrowserProfiles.ps1" -ForegroundColor White
    Write-Host "  - Then use: .\Auto-RefreshToken-Browser.ps1" -ForegroundColor White
    Write-Host ""

    Write-Success "Setup complete! Browser profiles created for $($targetAccounts.Count) accounts"
}

function Invoke-ValidateProfiles {
    Write-Info "Validating browser profiles..."

    $config = Get-ProfileConfig

    if (-not $config) {
        Write-Error "No configuration found. Run -InitialSetup first."
        return
    }

    $browser = $config.Browser
    $profiles = $config.Profiles

    Write-Success "Found configuration for $($profiles.Count) accounts using $browser"
    Write-Host ""

    $valid = 0
    $invalid = 0

    foreach ($acc in $profiles.PSObject.Properties.Name) {
        $profile = $profiles.$acc
        $profilePath = $profile.ProfilePath

        if (Test-Path $profilePath) {
            $files = Get-ChildItem $profilePath -Recurse -ErrorAction SilentlyContinue
            $fileCount = $files.Count

            if ($fileCount -gt 10) {
                Write-Host "Account $acc`: " -NoNewline
                Write-Host "[OK]" -ForegroundColor Green -NoNewline
                Write-Host " Profile active ($fileCount files)" -ForegroundColor Gray
                $valid++
            } else {
                Write-Host "Account $acc`: " -NoNewline
                Write-Host "[WARN]" -ForegroundColor Yellow -NoNewline
                Write-Host " Profile exists but may not be initialized" -ForegroundColor Gray
                $invalid++
            }
        } else {
            Write-Host "Account $acc`: " -NoNewline
            Write-Host "[ERROR]" -ForegroundColor Red -NoNewline
            Write-Host " Profile not found" -ForegroundColor Gray
            $invalid++
        }
    }

    Write-Host ""
    Write-Host "========================================" -ForegroundColor White
    Write-Host "Summary:" -ForegroundColor White
    Write-Host "  Valid profiles: $valid" -ForegroundColor Green
    Write-Host "  Invalid profiles: $invalid" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor White

    if ($invalid -gt 0) {
        Write-Warning "Some profiles need initialization or re-creation"
        Write-Info "Run: .\Authenticate-AllProfiles.ps1 to initialize"
    }
}

# ============================================================================
# Main Logic
# ============================================================================

if ($InitialSetup) {
    Invoke-InitialSetup
    exit 0
}

if ($ValidateProfiles) {
    Invoke-ValidateProfiles
    exit 0
}

if ($AccountNum) {
    # Create profile for specific account
    if (-not (Test-BrowserInstalled -BrowserName $Browser)) {
        exit 1
    }

    $profile = New-BrowserProfile -BrowserName $Browser -AccNum $AccountNum

    Write-Success "Profile created for account $AccountNum"
    Write-Info "Profile path: $($profile.ProfilePath)"
    Write-Info "Next: Authenticate this profile by running:"
    Write-Host "  .\Open-ProfileForAuth.ps1 -AccountNum $AccountNum" -ForegroundColor Cyan

    exit 0
}

# Default: Show usage
Write-Info "Browser Profile Setup for Claude Code OAuth Automation"
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  .\Setup-BrowserProfiles.ps1 -InitialSetup" -ForegroundColor White
Write-Host "  .\Setup-BrowserProfiles.ps1 -ValidateProfiles" -ForegroundColor White
Write-Host "  .\Setup-BrowserProfiles.ps1 -AccountNum 12 -Browser Chrome" -ForegroundColor White
Write-Host ""
Write-Info "Run with -InitialSetup for guided wizard"

exit 0
