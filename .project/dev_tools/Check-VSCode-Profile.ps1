# ============================================================================
# Check-VSCode-Profile.ps1
# Detect which PowerShell VS Code is using and fix profile
# ============================================================================

Write-Host ""
Write-Host "=== VS Code PowerShell Diagnostics ===" -ForegroundColor Cyan
Write-Host ""

# Detect PowerShell version
$psVersion = $PSVersionTable.PSVersion
Write-Host "PowerShell Version: $psVersion" -ForegroundColor Yellow
Write-Host "PowerShell Edition: $($PSVersionTable.PSEdition)" -ForegroundColor Yellow
Write-Host ""

# Show all possible profile locations
Write-Host "Profile Locations:" -ForegroundColor Yellow
Write-Host "  Current: $PROFILE" -ForegroundColor White

# Check if profile exists
if (Test-Path $PROFILE) {
    Write-Host "  [OK] Profile exists" -ForegroundColor Green

    # Check if our integration is there
    $content = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
    if ($content -like "*claude-profile.ps1*") {
        Write-Host "  [OK] Claude integration found" -ForegroundColor Green
    } else {
        Write-Host "  [!] Claude integration NOT found" -ForegroundColor Red
        Write-Host "  [FIX] Adding integration..." -ForegroundColor Cyan

        $SourceLine = ". D:\Projects\main\.dev_tools\claude-profile.ps1"
        Add-Content $PROFILE -Value "`n$SourceLine"
        Write-Host "  [OK] Integration added" -ForegroundColor Green
    }
} else {
    Write-Host "  [!] Profile does NOT exist" -ForegroundColor Red
    Write-Host "  [FIX] Creating profile..." -ForegroundColor Cyan

    # Create directory
    $profileDir = Split-Path $PROFILE -Parent
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    # Create profile with integration
    $SourceLine = ". D:\Projects\main\.dev_tools\claude-profile.ps1"
    Set-Content $PROFILE -Value $SourceLine
    Write-Host "  [OK] Profile created with integration" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Testing Integration ===" -ForegroundColor Cyan
Write-Host ""

# Test by loading the profile
try {
    . $PROFILE
    Write-Host "[OK] Profile loaded successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Try these commands:" -ForegroundColor Yellow
    Write-Host "  claude-help" -ForegroundColor White
    Write-Host "  c 9" -ForegroundColor White
} catch {
    Write-Host "[ERROR] Failed to load profile: $_" -ForegroundColor Red
}

Write-Host ""
