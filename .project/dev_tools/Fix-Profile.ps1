# ============================================================================
# Fix-Profile.ps1
# Automatically detect and fix PowerShell profile issues
# ============================================================================

Write-Host ""
Write-Host "=== PowerShell Profile Diagnostics ===" -ForegroundColor Cyan
Write-Host ""

# Detect PowerShell version
$psVersion = $PSVersionTable.PSVersion.Major
Write-Host "PowerShell Version: $psVersion" -ForegroundColor Yellow

# Show current profile path
Write-Host "Profile Path: $PROFILE" -ForegroundColor Yellow
Write-Host ""

# Check if profile exists
if (Test-Path $PROFILE) {
    Write-Host "[OK] Profile file exists" -ForegroundColor Green
} else {
    Write-Host "[!] Profile file does NOT exist" -ForegroundColor Red
    Write-Host "[INFO] Creating profile file..." -ForegroundColor Cyan

    # Create parent directory if needed
    $profileDir = Split-Path $PROFILE -Parent
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
        Write-Host "[OK] Created directory: $profileDir" -ForegroundColor Green
    }

    # Create empty profile
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
    Write-Host "[OK] Created profile: $PROFILE" -ForegroundColor Green
}

# Add claude-profile.ps1 source line
$SourceLine = ". D:\Projects\main\.dev_tools\claude-profile.ps1"
$profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue

if ($profileContent -like "*$SourceLine*") {
    Write-Host "[OK] Claude profile integration already installed" -ForegroundColor Green
} else {
    Write-Host "[INFO] Adding Claude profile integration..." -ForegroundColor Cyan
    if ($profileContent) {
        Add-Content $PROFILE -Value "`n$SourceLine"
    } else {
        Set-Content $PROFILE -Value $SourceLine
    }
    Write-Host "[OK] Added Claude profile integration" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Reload your profile:" -ForegroundColor Yellow
Write-Host "   . `$PROFILE" -ForegroundColor White
Write-Host ""
Write-Host "2. Test with:" -ForegroundColor Yellow
Write-Host "   claude-help" -ForegroundColor White
Write-Host "   c 9" -ForegroundColor White
Write-Host ""

exit 0
