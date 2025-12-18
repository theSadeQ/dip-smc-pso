# ============================================================================
# Fix-ChromeProfileNames.ps1
# Properly rename Chrome profile display names
# ============================================================================

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

Write-Info "Fixing Chrome profile names..."
Write-Host ""

# Check if Chrome is running
$chromeRunning = Get-Process -Name chrome -ErrorAction SilentlyContinue
if ($chromeRunning) {
    Write-Error "Chrome is running! Please close Chrome completely first."
    Write-Info "Run: Stop-Process -Name chrome -Force"
    exit 1
}

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
        # Read raw JSON
        $prefsJson = Get-Content $prefsFile -Raw -Encoding UTF8
        $prefs = $prefsJson | ConvertFrom-Json

        # Update profile name
        $newName = "Claude_Account_$acc"

        # Chrome uses the "name" field in the "profile" object
        if (-not $prefs.profile) {
            $prefs | Add-Member -MemberType NoteProperty -Name "profile" -Value @{} -Force
        }

        $prefs.profile.name = $newName

        # Convert back to JSON and save
        $updatedJson = $prefs | ConvertTo-Json -Depth 100 -Compress
        [System.IO.File]::WriteAllText($prefsFile, $updatedJson, [System.Text.Encoding]::UTF8)

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

Write-Info "Now open Chrome to see the new names"
