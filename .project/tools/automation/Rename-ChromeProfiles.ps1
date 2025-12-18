# ============================================================================
# Rename-ChromeProfiles.ps1
# Rename Chrome profile display names
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$NamePrefix = "Claude_Account_"
)

$ConfigFile = "D:\Projects\main\.project\dev_tools\browser_profiles_config.json"

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Load configuration
if (-not (Test-Path $ConfigFile)) {
    Write-Error "Configuration not found"
    exit 1
}

$config = Get-Content $ConfigFile -Raw | ConvertFrom-Json
$profiles = $config.Profiles

Write-Info "Renaming Chrome profiles..."
Write-Host ""

$renamed = 0
$failed = 0

foreach ($acc in $profiles.PSObject.Properties.Name) {
    $profile = $profiles.$acc
    $profilePath = $profile.ProfilePath
    $prefsFile = Join-Path $profilePath "Preferences"

    if (-not (Test-Path $prefsFile)) {
        Write-Info "Account $acc`: Skipping (not initialized)"
        continue
    }

    try {
        # Read preferences
        $prefs = Get-Content $prefsFile -Raw | ConvertFrom-Json

        # Update profile name
        $newName = "$NamePrefix$acc"
        $prefs.profile.name = $newName

        # Save preferences
        $prefs | ConvertTo-Json -Depth 100 | Set-Content $prefsFile -Encoding UTF8

        Write-Success "Account $acc`: Renamed to '$newName'"
        $renamed++
    } catch {
        Write-Error "Account $acc`: Failed - $($_.Exception.Message)"
        $failed++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor White
Write-Host "  RENAME COMPLETE" -ForegroundColor White
Write-Host "========================================" -ForegroundColor White
Write-Host "  Renamed: $renamed" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor White
Write-Host ""

Write-Info "Close Chrome completely and reopen to see the new names"
