# ============================================================================
# Install-ExtensionToProfiles.ps1
# Install browser extension to all Claude Code profiles
# ============================================================================
#
# Purpose: Automate extension installation across all browser profiles
# Author: Claude Code Multi-Account Automation System
# Created: 2025-11-10
#
# Usage:
#   Install-ExtensionToProfiles -ExtensionPath "D:\pp\Pars Premium 1.3.1 (En)"
#   Install-ExtensionToProfiles -ExtensionPath "D:\pp\Pars Premium 1.3.1 (En)" -AccountNums 1,5,12
#   Install-ExtensionToProfiles -ExtensionPath "D:\pp\Pars Premium 1.3.1 (En)" -TestProfile
#
# ============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$ExtensionPath,

    [Parameter(Mandatory=$false)]
    [int[]]$AccountNums,

    [Parameter(Mandatory=$false)]
    [switch]$TestProfile,

    [Parameter(Mandatory=$false)]
    [int]$DelaySeconds = 15
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
        Write-Error "Configuration not found: $ConfigFile"
        return $null
    }

    try {
        return Get-Content $ConfigFile -Raw | ConvertFrom-Json
    } catch {
        Write-Error "Failed to load configuration: $($_.Exception.Message)"
        return $null
    }
}

function Install-ExtensionToProfile {
    param(
        [int]$AccountNum,
        [string]$ProfileName,
        [string]$ExtPath
    )

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  INSTALLING EXTENSION TO ACCOUNT $AccountNum" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    # Launch Chrome with extension auto-load
    $chromeExe = "C:\Program Files\Google\Chrome\Application\chrome.exe"

    if (-not (Test-Path $chromeExe)) {
        Write-Error "Chrome not found at: $chromeExe"
        return $false
    }

    Write-Info "Opening Chrome with profile $ProfileName..."
    Write-Info "Extension will be loaded from: $ExtPath"

    # Chrome arguments to load extension
    $args = @(
        "--profile-directory=$ProfileName",
        "--load-extension=`"$ExtPath`"",
        "--no-first-run",
        "--no-default-browser-check",
        "chrome://extensions/"
    )

    Write-Info "Launching Chrome..."
    $process = Start-Process $chromeExe -ArgumentList $args -PassThru

    Write-Host ""
    Write-Host "STEPS TO COMPLETE:" -ForegroundColor Yellow
    Write-Host "  1. Chrome opened with extensions page" -ForegroundColor White
    Write-Host "  2. Enable 'Developer mode' (toggle in top-right)" -ForegroundColor White
    Write-Host "  3. Extension 'Pars Premium' should be loaded automatically" -ForegroundColor White
    Write-Host "  4. If not loaded, click 'Load unpacked' and select:" -ForegroundColor White
    Write-Host "     $ExtPath" -ForegroundColor Gray
    Write-Host "  5. Verify extension is enabled (blue toggle)" -ForegroundColor White
    Write-Host "  6. Close Chrome window" -ForegroundColor White
    Write-Host "  7. Return here and press Enter" -ForegroundColor White
    Write-Host ""

    Read-Host "Press Enter after extension is installed"

    # Close Chrome
    if ($process -and -not $process.HasExited) {
        Write-Info "Closing Chrome..."
        $process.CloseMainWindow() | Out-Null
        Start-Sleep -Seconds 2
        if (-not $process.HasExited) {
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        }
    }

    Write-Success "Extension installation complete for account $AccountNum"
    return $true
}

function Install-ExtensionAutomated {
    param(
        [int]$AccountNum,
        [string]$ProfileName,
        [string]$ExtPath
    )

    Write-Info "Installing extension to account $AccountNum (automated)..."

    # Get Chrome profile directory
    $profilePath = "$env:LOCALAPPDATA\Google\Chrome\User Data\$ProfileName"
    $prefsFile = Join-Path $profilePath "Preferences"

    if (-not (Test-Path $profilePath)) {
        Write-Error "Profile directory not found: $profilePath"
        return $false
    }

    # Read preferences
    if (Test-Path $prefsFile) {
        try {
            $prefs = Get-Content $prefsFile -Raw | ConvertFrom-Json

            # Enable developer mode
            if (-not $prefs.extensions) {
                $prefs | Add-Member -NotePropertyName "extensions" -NotePropertyValue @{} -Force
            }
            if (-not $prefs.extensions.ui) {
                $prefs.extensions | Add-Member -NotePropertyName "ui" -NotePropertyValue @{} -Force
            }
            $prefs.extensions.ui | Add-Member -NotePropertyName "developer_mode" -NotePropertyValue $true -Force

            # Save preferences
            $prefs | ConvertTo-Json -Depth 100 | Set-Content $prefsFile -Encoding UTF8

            Write-Success "Developer mode enabled for account $AccountNum"
        } catch {
            Write-Warning "Could not modify preferences: $($_.Exception.Message)"
        }
    }

    return $true
}

# ============================================================================
# Main Logic
# ============================================================================

# Verify extension path exists
if (-not (Test-Path $ExtensionPath)) {
    Write-Error "Extension path not found: $ExtensionPath"
    Write-Info "Please verify the path and try again"
    exit 1
}

Write-Success "Extension found: $ExtensionPath"

# Check if it's an unpacked extension directory
$manifestFile = Join-Path $ExtensionPath "manifest.json"
if (Test-Path $manifestFile) {
    $manifest = Get-Content $manifestFile -Raw | ConvertFrom-Json
    Write-Success "Extension: $($manifest.name) v$($manifest.version)"
} else {
    Write-Warning "No manifest.json found. This may not be a valid extension directory."
    $confirm = Read-Host "Continue anyway? (y/n)"
    if ($confirm -ne 'y') {
        exit 0
    }
}

# Load configuration
$config = Get-ProfileConfig
if (-not $config) {
    exit 1
}

$browser = $config.Browser
$profiles = $config.Profiles

if ($browser -ne 'Chrome') {
    Write-Error "This script only supports Chrome. Current browser: $browser"
    exit 1
}

# Determine which accounts to process
if ($TestProfile) {
    Write-Info "Test mode: Installing to account 1 only"
    $targetAccounts = @(1)
} elseif ($AccountNums) {
    $targetAccounts = $AccountNums
} else {
    $targetAccounts = $profiles.PSObject.Properties.Name | ForEach-Object { [int]$_ }
}

Write-Info "Installing extension to $($targetAccounts.Count) profile(s)"
Write-Host ""

Write-Host "INSTALLATION METHOD:" -ForegroundColor Yellow
Write-Host "  1. Semi-automated (opens Chrome, you enable extension)" -ForegroundColor White
Write-Host "  2. Fully automated (modifies preferences, requires Chrome restart)" -ForegroundColor White
Write-Host ""

$method = Read-Host "Choose method (1 or 2)"

if ($method -eq '2') {
    Write-Info "Using automated method..."

    foreach ($acc in $targetAccounts) {
        $profile = $profiles.$acc
        if ($profile) {
            Install-ExtensionAutomated -AccountNum $acc -ProfileName $profile.ProfileName -ExtPath $ExtensionPath
        }
    }

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  EXTENSION PRE-CONFIGURED" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Close ALL Chrome windows" -ForegroundColor White
    Write-Host "  2. Open Chrome with any profile" -ForegroundColor White
    Write-Host "  3. Go to chrome://extensions/" -ForegroundColor White
    Write-Host "  4. Developer mode should be enabled" -ForegroundColor White
    Write-Host "  5. Click 'Load unpacked' and select:" -ForegroundColor White
    Write-Host "     $ExtensionPath" -ForegroundColor Gray
    Write-Host ""
    Write-Info "You'll need to load the extension once, then it will be available in all profiles"

} else {
    Write-Info "Using semi-automated method..."

    $installed = 0
    $failed = 0

    foreach ($acc in $targetAccounts) {
        $profile = $profiles.$acc

        if (-not $profile) {
            Write-Warning "Account $acc has no profile configured. Skipping."
            $failed++
            continue
        }

        if (Install-ExtensionToProfile -AccountNum $acc -ProfileName $profile.ProfileName -ExtPath $ExtensionPath) {
            $installed++
        } else {
            $failed++
        }

        # Delay between profiles
        if ($acc -ne $targetAccounts[-1]) {
            Write-Info "Waiting $DelaySeconds seconds before next profile..."
            Start-Sleep -Seconds $DelaySeconds
        }
    }

    Write-Host "`n========================================" -ForegroundColor White
    Write-Host "  INSTALLATION COMPLETE" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor White
    Write-Host "  Installed: $installed" -ForegroundColor Green
    Write-Host "  Failed: $failed" -ForegroundColor Red
    Write-Host "========================================`n" -ForegroundColor White
}

Write-Success "Extension installation process complete!"
Write-Info "Next step: Run .\Authenticate-AllProfiles.ps1 to log in with extension"

exit 0
