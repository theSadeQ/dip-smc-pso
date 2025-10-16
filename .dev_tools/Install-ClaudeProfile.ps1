# ============================================================================
# Install-ClaudeProfile.ps1
# Automatic Profile Integration for Claude Multi-Account System
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [switch]$Uninstall
)

$ProfilePath = $PROFILE
$SourceLine = ". D:\Projects\main\.dev_tools\claude-profile.ps1"

# ============================================================================
# Helper Functions
# ============================================================================

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

# ============================================================================
# Main Logic
# ============================================================================

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Claude Profile Installer" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if profile exists
if (-not (Test-Path $ProfilePath)) {
    Write-Info "PowerShell profile not found. Creating: $ProfilePath"
    $profileDir = Split-Path $ProfilePath -Parent
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }
    New-Item -ItemType File -Path $ProfilePath -Force | Out-Null
    Write-Success "Created PowerShell profile"
}

# Read current profile
$profileContent = Get-Content $ProfilePath -Raw -ErrorAction SilentlyContinue

# Uninstall mode
if ($Uninstall) {
    Write-Info "Uninstalling Claude profile integration..."

    if ($profileContent -like "*$SourceLine*") {
        $newContent = $profileContent -replace [regex]::Escape($SourceLine), ""
        $newContent = $newContent -replace "(?m)^\s*$(\r?\n)", ""  # Remove empty lines
        Set-Content $ProfilePath -Value $newContent.TrimEnd() -NoNewline
        Write-Success "Removed Claude profile integration"
        Write-Info "Reload profile: . `$PROFILE"
    } else {
        Write-Info "Claude profile integration not found in profile"
    }

    Write-Host ""
    exit 0
}

# Install mode
Write-Info "Installing Claude profile integration..."

# Check if already installed
if ($profileContent -like "*$SourceLine*") {
    Write-Info "Claude profile integration already installed"
    Write-Success "Nothing to do"
} else {
    # Add source line to profile
    if ($profileContent) {
        Add-Content $ProfilePath -Value "`n$SourceLine"
    } else {
        Set-Content $ProfilePath -Value $SourceLine
    }

    Write-Success "Added Claude profile integration to: $ProfilePath"
}

Write-Host ""
Write-Success "Installation complete!"
Write-Host ""
Write-Info "To activate, reload your PowerShell profile:"
Write-Host "  . `$PROFILE" -ForegroundColor White
Write-Host ""
Write-Info "After reloading, test with:"
Write-Host "  claude-help" -ForegroundColor White
Write-Host ""

exit 0
