# ============================================================================
# Restore-ClaudeConfig.ps1
# Restore Utility for Claude Code Configuration
# ============================================================================
#
# Purpose: Restore primary .claude directory from backup
# Author: Claude Code Multi-Account System
# Created: 2025-10-11
#
# Usage:
#   .\Restore-ClaudeConfig.ps1                     # Interactive selection
#   .\Restore-ClaudeConfig.ps1 -BackupFile "path"  # Specific backup
#   .\Restore-ClaudeConfig.ps1 -ClearOverride      # Just clear CLAUDE_CONFIG_DIR
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$BackupFile,

    [Parameter(Mandatory=$false)]
    [string]$BackupDir = "D:\Projects\main\.artifacts\claude_backups",

    [Parameter(Mandatory=$false)]
    [switch]$ClearOverride,

    [Parameter(Mandatory=$false)]
    [switch]$Force
)

# Configuration
$PrimaryClaudeDir = "$env:USERPROFILE\.claude"

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

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Clear-ConfigOverride {
    Write-Info "Clearing CLAUDE_CONFIG_DIR override..."

    if ($env:CLAUDE_CONFIG_DIR) {
        Remove-Item Env:\CLAUDE_CONFIG_DIR
        Write-Success "Cleared CLAUDE_CONFIG_DIR"
        Write-Info "Now using primary .claude directory"
    } else {
        Write-Info "CLAUDE_CONFIG_DIR was not set"
    }

    return $true
}

# ============================================================================
# Main Restore Logic
# ============================================================================

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Claude Code Configuration Restore" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Mode 1: Just clear override
if ($ClearOverride) {
    Clear-ConfigOverride
    Write-Success "Configuration reset to primary .claude"
    Write-Host ""
    exit 0
}

# Mode 2: Full restore from backup

# 1. Check if backups exist
if (-not (Test-Path $BackupDir)) {
    Write-Error "Backup directory not found: $BackupDir"
    Write-Info "Run Backup-ClaudeConfig.ps1 first to create a backup."
    exit 1
}

$backups = Get-ChildItem $BackupDir -Filter ".claude_backup_*.zip" -ErrorAction SilentlyContinue |
           Sort-Object LastWriteTime -Descending

if ($backups.Count -eq 0) {
    Write-Error "No backups found in: $BackupDir"
    Write-Info "Run Backup-ClaudeConfig.ps1 first to create a backup."
    exit 1
}

Write-Success "Found $($backups.Count) backup(s)"

# 2. Select backup
if (-not $BackupFile) {
    Write-Host ""
    Write-Info "Available backups:"
    Write-Host ""

    for ($i = 0; $i -lt [Math]::Min($backups.Count, 10); $i++) {
        $backup = $backups[$i]
        $age = (Get-Date) - $backup.LastWriteTime

        $ageStr = if ($age.Days -gt 0) {
            "$($age.Days) days ago"
        } elseif ($age.Hours -gt 0) {
            "$($age.Hours) hours ago"
        } else {
            "$($age.Minutes) minutes ago"
        }

        $sizeStr = if ($backup.Length -gt 1MB) {
            "{0:N2} MB" -f ($backup.Length / 1MB)
        } else {
            "{0:N2} KB" -f ($backup.Length / 1KB)
        }

        Write-Host "  [$($i+1)] $($backup.Name)" -ForegroundColor White
        Write-Host "      $sizeStr - $ageStr" -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "  [0] Cancel" -ForegroundColor Yellow
    Write-Host ""

    do {
        $selection = Read-Host "Select backup to restore (1-$([Math]::Min($backups.Count, 10)))"

        if ($selection -eq "0") {
            Write-Info "Restore cancelled."
            exit 0
        }

        $index = [int]$selection - 1
    } while ($index -lt 0 -or $index -ge $backups.Count)

    $BackupFile = $backups[$index].FullName
}

# 3. Verify backup file exists
if (-not (Test-Path $BackupFile)) {
    Write-Error "Backup file not found: $BackupFile"
    exit 1
}

Write-Info "Selected backup: $(Split-Path $BackupFile -Leaf)"

# 4. Confirm restoration
if (-not $Force) {
    Write-Host ""
    Write-Warning "This will replace your current .claude directory!"
    Write-Warning "Current location: $PrimaryClaudeDir"
    Write-Host ""
    $confirm = Read-Host "Type 'yes' to confirm restoration"

    if ($confirm -ne "yes") {
        Write-Info "Restore cancelled."
        exit 0
    }
}

# 5. Backup current .claude (safety measure)
if (Test-Path $PrimaryClaudeDir) {
    $safetyBackup = Join-Path $BackupDir ".claude_pre_restore_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip"
    Write-Info "Creating safety backup of current .claude..."

    try {
        Add-Type -Assembly System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::CreateFromDirectory(
            $PrimaryClaudeDir,
            $safetyBackup,
            [System.IO.Compression.CompressionLevel]::Fastest,
            $false
        )
        Write-Success "Safety backup created: $(Split-Path $safetyBackup -Leaf)"
    } catch {
        Write-Warning "Could not create safety backup: $_"
    }
}

# 6. Remove current .claude
if (Test-Path $PrimaryClaudeDir) {
    Write-Info "Removing current .claude directory..."
    try {
        Remove-Item $PrimaryClaudeDir -Recurse -Force
        Write-Success "Removed current .claude"
    } catch {
        Write-Error "Failed to remove current .claude: $_"
        exit 1
    }
}

# 7. Extract backup
Write-Info "Restoring from backup..."

try {
    Add-Type -Assembly System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory($BackupFile, $PrimaryClaudeDir)
    Write-Success "Backup restored successfully!"

} catch {
    Write-Error "Failed to restore backup: $_"
    Write-Error "You may need to manually extract: $BackupFile"
    exit 1
}

# 8. Clear CLAUDE_CONFIG_DIR override
Clear-ConfigOverride

# 9. Verify restoration
if (Test-Path $PrimaryClaudeDir) {
    $fileCount = (Get-ChildItem $PrimaryClaudeDir -Recurse -File -ErrorAction SilentlyContinue).Count
    Write-Success "Restored $fileCount files to primary .claude"
} else {
    Write-Error "Restoration verification failed!"
    exit 1
}

Write-Host ""
Write-Success "Configuration restored successfully!"
Write-Info "You are now using the primary .claude directory"
Write-Host ""

exit 0
