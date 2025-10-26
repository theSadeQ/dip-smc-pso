# Install Claude Profile to PowerShell
Write-Host "Installing Claude Code multi-account switcher to PowerShell profile..." -ForegroundColor Cyan
Write-Host ""

# Ensure profile exists
if (-not (Test-Path $PROFILE)) {
    Write-Host "[INFO] Creating PowerShell profile at: $PROFILE" -ForegroundColor Yellow
    New-Item -Path $PROFILE -ItemType File -Force | Out-Null
}

# Check if already installed
$profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
$sourceLine = ". D:\Projects\main\.dev_tools\claude-profile.ps1"

if ($profileContent -like "*claude-profile.ps1*") {
    Write-Host "[OK] Already installed in profile!" -ForegroundColor Green
    Write-Host "     Profile location: $PROFILE" -ForegroundColor Gray
} else {
    # Add to profile
    Add-Content $PROFILE "`n# Claude Code Multi-Account Switcher"
    Add-Content $PROFILE $sourceLine

    Write-Host "[OK] Successfully added to PowerShell profile!" -ForegroundColor Green
    Write-Host "     Profile location: $PROFILE" -ForegroundColor Gray
}

Write-Host ""
Write-Host "To activate in THIS window, run:" -ForegroundColor Yellow
Write-Host "  . `$PROFILE" -ForegroundColor White
Write-Host ""
Write-Host "Or open a NEW PowerShell window and the functions will load automatically." -ForegroundColor Yellow
Write-Host ""
