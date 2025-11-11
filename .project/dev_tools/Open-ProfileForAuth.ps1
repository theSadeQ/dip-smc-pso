# ============================================================================
# Open-ProfileForAuth.ps1
# Quick helper to open a browser profile for authentication
# ============================================================================

param(
    [Parameter(Mandatory=$true)]
    [int]$AccountNum
)

$ConfigFile = "D:\Projects\main\.project\dev_tools\browser_profiles_config.json"

if (-not (Test-Path $ConfigFile)) {
    Write-Host "[ERROR] Configuration not found. Run Setup-BrowserProfiles.ps1 -InitialSetup first" -ForegroundColor Red
    exit 1
}

$config = Get-Content $ConfigFile -Raw | ConvertFrom-Json
$browser = $config.Browser
$profile = $config.Profiles.$AccountNum

if (-not $profile) {
    Write-Host "[ERROR] Account $AccountNum has no browser profile" -ForegroundColor Red
    exit 1
}

$profileName = $profile.ProfileName

Write-Host "[INFO] Opening $browser with profile for account $AccountNum..." -ForegroundColor Cyan

switch ($browser) {
    'Chrome' {
        $exe = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        Start-Process $exe -ArgumentList "--profile-directory=$profileName", "https://claude.com"
    }
    'Edge' {
        $exe = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        Start-Process $exe -ArgumentList "--profile-directory=$profileName", "https://claude.com"
    }
}

Write-Host "[OK] Browser opened. Log in to claude.com and close when done." -ForegroundColor Green
