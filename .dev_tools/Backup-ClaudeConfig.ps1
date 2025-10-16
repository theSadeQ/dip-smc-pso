# ============================================================================
# Backup-ClaudeConfig.ps1
# Backup Utility for Claude Code Configuration
# ============================================================================
#
# Purpose: Create timestamped backup of primary .claude directory
# Author: Claude Code Multi-Account System
# Created: 2025-10-11
#
# Usage:
#   .\Backup-ClaudeConfig.ps1
#   .\Backup-ClaudeConfig.ps1 -BackupDir "D:\Backups"
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$BackupDir = "D:\Projects\main\.artifacts\claude_backups"
)

# Configuration
$PrimaryClaudeDir = "$env:USERPROFILE\.claude"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupName = ".claude_backup_$Timestamp"

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

function Get-DirectorySize {
    param([string]$Path)

    $size = (Get-ChildItem $Path -Recurse -File -ErrorAction SilentlyContinue |
             Measure-Object -Property Length -Sum).Sum

    if ($size -gt 1GB) {
        return "{0:N2} GB" -f ($size / 1GB)
    } elseif ($size -gt 1MB) {
        return "{0:N2} MB" -f ($size / 1MB)
    } elseif ($size -gt 1KB) {
        return "{0:N2} KB" -f ($size / 1KB)
    } else {
        return "$size bytes"
    }
}

# ============================================================================
# Main Backup Logic
# ============================================================================

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Claude Code Configuration Backup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check if primary .claude exists
if (-not (Test-Path $PrimaryClaudeDir)) {
    Write-Error "Primary .claude directory not found at: $PrimaryClaudeDir"
    Write-Info "Nothing to backup. Exiting."
    exit 1
}

Write-Success "Found primary .claude directory"

# 2. Get size info
$dirSize = Get-DirectorySize $PrimaryClaudeDir
$fileCount = (Get-ChildItem $PrimaryClaudeDir -Recurse -File -ErrorAction SilentlyContinue).Count
Write-Info "Size: $dirSize ($fileCount files)"

# 3. Create backup directory
if (-not (Test-Path $BackupDir)) {
    Write-Info "Creating backup directory: $BackupDir"
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

# 4. Create backup archive
$BackupZip = Join-Path $BackupDir "$BackupName.zip"
Write-Info "Creating backup archive: $BackupZip"

try {
    # Use .NET compression (faster than Compress-Archive for large files)
    Add-Type -Assembly System.IO.Compression.FileSystem

    $compressionLevel = [System.IO.Compression.CompressionLevel]::Optimal
    [System.IO.Compression.ZipFile]::CreateFromDirectory(
        $PrimaryClaudeDir,
        $BackupZip,
        $compressionLevel,
        $false  # Don't include base directory
    )

    Write-Success "Backup created successfully!"

} catch {
    Write-Error "Failed to create backup: $_"
    exit 1
}

# 5. Verify backup
if (Test-Path $BackupZip) {
    $backupSize = (Get-Item $BackupZip).Length

    if ($backupSize -gt 1MB) {
        $backupSizeStr = "{0:N2} MB" -f ($backupSize / 1MB)
    } elseif ($backupSize -gt 1KB) {
        $backupSizeStr = "{0:N2} KB" -f ($backupSize / 1KB)
    } else {
        $backupSizeStr = "$backupSize bytes"
    }

    Write-Success "Backup size: $backupSizeStr"
    Write-Info "Location: $BackupZip"
} else {
    Write-Error "Backup verification failed!"
    exit 1
}

# 6. List all backups
Write-Host ""
Write-Info "Available backups:"
Get-ChildItem $BackupDir -Filter ".claude_backup_*.zip" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 5 |
    ForEach-Object {
        $age = (Get-Date) - $_.LastWriteTime
        $ageStr = if ($age.Days -gt 0) {
            "$($age.Days) days ago"
        } elseif ($age.Hours -gt 0) {
            "$($age.Hours) hours ago"
        } else {
            "$($age.Minutes) minutes ago"
        }

        $sizeStr = if ($_.Length -gt 1MB) {
            "{0:N2} MB" -f ($_.Length / 1MB)
        } else {
            "{0:N2} KB" -f ($_.Length / 1KB)
        }

        Write-Host "  $($_.Name) - $sizeStr ($ageStr)" -ForegroundColor White
    }

Write-Host ""
Write-Success "Backup completed successfully!"
Write-Host ""

exit 0
