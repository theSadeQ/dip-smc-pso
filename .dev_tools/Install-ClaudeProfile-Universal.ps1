# ============================================================================
# Install-ClaudeProfile-Universal.ps1
# Universal Profile Integration (PowerShell 5.1 & 7+)
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [switch]$Uninstall
)

$SourceLine = ". D:\Projects\main\.dev_tools\claude-profile.ps1"

# Both PowerShell versions
$Profiles = @(
    "$env:USERPROFILE\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"  # PS 5.1
    "$env:USERPROFILE\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"         # PS 7+
    "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"           # PS 5.1 (no OneDrive)
    "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"                  # PS 7+ (no OneDrive)
)

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Universal Claude Profile Installer" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$installed = 0
$alreadyInstalled = 0

foreach ($ProfilePath in $Profiles) {
    $profileDir = Split-Path $ProfilePath -Parent

    # Skip if parent directory doesn't exist
    if (-not (Test-Path $profileDir)) {
        continue
    }

    # Create profile if missing
    if (-not (Test-Path $ProfilePath)) {
        New-Item -ItemType File -Path $ProfilePath -Force | Out-Null
        Write-Info "Created: $ProfilePath"
    }

    # Read current content
    $profileContent = Get-Content $ProfilePath -Raw -ErrorAction SilentlyContinue

    if ($Uninstall) {
        if ($profileContent -like "*$SourceLine*") {
            $newContent = $profileContent -replace [regex]::Escape($SourceLine), ""
            $newContent = $newContent -replace "(?m)^\s*$(\r?\n)", ""
            Set-Content $ProfilePath -Value $newContent.TrimEnd() -NoNewline
            Write-Success "Removed from: $ProfilePath"
            $installed++
        }
    } else {
        if ($profileContent -like "*$SourceLine*") {
            $alreadyInstalled++
        } else {
            if ($profileContent) {
                Add-Content $ProfilePath -Value "`n$SourceLine"
            } else {
                Set-Content $ProfilePath -Value $SourceLine
            }
            Write-Success "Installed to: $ProfilePath"
            $installed++
        }
    }
}

Write-Host ""
if ($Uninstall) {
    Write-Success "Uninstalled from $installed profile(s)"
} else {
    Write-Success "Installed to $installed profile(s)"
    if ($alreadyInstalled -gt 0) {
        Write-Info "$alreadyInstalled profile(s) already had the integration"
    }
}

Write-Host ""
Write-Info "Reload your profile:"
Write-Host "  . `$PROFILE" -ForegroundColor White
Write-Host ""

exit 0
