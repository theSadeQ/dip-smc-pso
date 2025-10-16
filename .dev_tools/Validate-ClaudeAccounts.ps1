# ============================================================================
# Validate-ClaudeAccounts.ps1
# Safety Validation for Claude Code Multi-Account System
# ============================================================================
#
# Purpose: Validate account isolation and detect safety violations
# Author: Claude Code Multi-Account System
# Created: 2025-10-11
#
# Usage:
#   .\Validate-ClaudeAccounts.ps1
#   .\Validate-ClaudeAccounts.ps1 -Verbose
#   .\Validate-ClaudeAccounts.ps1 -FixIssues
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [switch]$FixIssues,

    [Parameter(Mandatory=$false)]
    [switch]$ShowDetails
)

# Configuration
$PrimaryClaudeDir = "$env:USERPROFILE\.claude"
$MaxAccounts = 50000  # Extended to support up to 50000 accounts
$AuthFiles = @(".credentials.json", "history.jsonl", ".claude.json", "settings.json")

# Safety thresholds
$MaxWarnings = 0  # Zero tolerance for auth file junctions

# Statistics
$Stats = @{
    TotalAccounts = 0
    Authenticated = 0
    NeedsLogin = 0
    Junctions = 0
    Errors = 0
    Warnings = 0
}

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
    $Stats.Warnings++
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
    $Stats.Errors++
}

function Write-VerboseInfo {
    param([string]$Message)
    if ($ShowDetails) {
        Write-Host "  [DEBUG] $Message" -ForegroundColor Gray
    }
}

function Test-AuthFileJunctions {
    param([string]$AccountDir, [int]$AccountNum)

    $violations = @()

    foreach ($file in $AuthFiles) {
        $path = Join-Path $AccountDir $file
        if (Test-Path $path) {
            $item = Get-Item $path -Force
            if ($item.LinkType -eq "Junction" -or $item.LinkType -eq "SymbolicLink") {
                $violations += @{
                    File = $file
                    Target = $item.Target
                }
                Write-Error "Account $AccountNum has junction: $file -> $($item.Target)"
            } else {
                Write-VerboseInfo "Account $AccountNum $file is a real file (safe)"
            }
        }
    }

    if ($violations.Count -gt 0) {
        $Stats.Junctions += $violations.Count
        return $false
    }

    return $true
}

function Test-AccountAuthentication {
    param([string]$AccountDir)

    $credFile = Join-Path $AccountDir ".credentials.json"
    return (Test-Path $credFile)
}

function Get-AccountFileCount {
    param([string]$AccountDir)

    return (Get-ChildItem $AccountDir -Force -ErrorAction SilentlyContinue).Count
}

function Remove-AuthJunctions {
    param([string]$AccountDir, [int]$AccountNum)

    Write-Info "Attempting to remove auth file junctions from Account $AccountNum..."

    $removed = 0
    foreach ($file in $AuthFiles) {
        $path = Join-Path $AccountDir $file
        if (Test-Path $path) {
            $item = Get-Item $path -Force
            if ($item.LinkType -eq "Junction" -or $item.LinkType -eq "SymbolicLink") {
                try {
                    # Remove junction (not the target)
                    $item.Delete()
                    Write-Success "Removed junction: $file"
                    $removed++
                } catch {
                    Write-Error "Failed to remove junction $file`: $_"
                }
            }
        }
    }

    if ($removed -gt 0) {
        Write-Success "Removed $removed junction(s) from Account $AccountNum"
        return $true
    }

    return $false
}

# ============================================================================
# Main Validation Logic
# ============================================================================

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Claude Code Account Safety Validator" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check primary directory
Write-Info "Checking primary .claude directory..."
if (-not (Test-Path $PrimaryClaudeDir)) {
    Write-Warning "Primary .claude directory not found at: $PrimaryClaudeDir"
    Write-Info "This is okay if Claude Code hasn't been used yet."
} else {
    $primaryFileCount = Get-AccountFileCount $PrimaryClaudeDir
    Write-Success "Primary .claude exists ($primaryFileCount files)"
}

# 2. Check current CLAUDE_CONFIG_DIR
Write-Info "Checking current environment..."
if ($env:CLAUDE_CONFIG_DIR) {
    Write-Info "CLAUDE_CONFIG_DIR is set: $env:CLAUDE_CONFIG_DIR"

    # Extract account number
    if ($env:CLAUDE_CONFIG_DIR -match '\\\.claude(\d+)$') {
        $currentAccount = $matches[1]
        Write-Info "Currently using Account $currentAccount"
    }
} else {
    Write-Info "CLAUDE_CONFIG_DIR not set (using primary)"
}

# 3. Scan all accounts
Write-Info "Scanning accounts 1-$MaxAccounts..."
Write-Host ""

$accountsFound = @()

1..$MaxAccounts | ForEach-Object {
    $accountNum = $_
    $accountDir = "$env:USERPROFILE\.claude$accountNum"

    if (Test-Path $accountDir) {
        $Stats.TotalAccounts++
        $accountsFound += $accountNum

        Write-Host "Account ${accountNum}:" -NoNewline -ForegroundColor White

        # Check authentication
        $authenticated = Test-AccountAuthentication $accountDir
        if ($authenticated) {
            $Stats.Authenticated++
            Write-Host " [Authenticated]" -NoNewline -ForegroundColor Green
        } else {
            $Stats.NeedsLogin++
            Write-Host " [Needs login]" -NoNewline -ForegroundColor Yellow
        }

        # Check file count
        $fileCount = Get-AccountFileCount $accountDir
        Write-Host " ($fileCount files)" -NoNewline

        # Safety check: no auth file junctions
        $safe = Test-AuthFileJunctions $accountDir $accountNum

        if ($safe) {
            Write-Host " [SAFE]" -ForegroundColor Green
        } else {
            Write-Host " [UNSAFE - HAS JUNCTIONS]" -ForegroundColor Red

            if ($FixIssues) {
                Remove-AuthJunctions $accountDir $accountNum
            }
        }
    }
}

# 4. Summary
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Validation Summary" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Total accounts found: $($Stats.TotalAccounts)" -ForegroundColor White
Write-Host "  Authenticated:      $($Stats.Authenticated)" -ForegroundColor Green
Write-Host "  Needs login:        $($Stats.NeedsLogin)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Safety checks:" -ForegroundColor White
Write-Host "  Auth junctions:     $($Stats.Junctions)" -ForegroundColor $(if ($Stats.Junctions -eq 0) { "Green" } else { "Red" })
Write-Host "  Errors:             $($Stats.Errors)" -ForegroundColor $(if ($Stats.Errors -eq 0) { "Green" } else { "Red" })
Write-Host "  Warnings:           $($Stats.Warnings)" -ForegroundColor $(if ($Stats.Warnings -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

# 5. Final verdict
if ($Stats.Errors -eq 0 -and $Stats.Warnings -le $MaxWarnings) {
    Write-Success "All safety checks passed!"
    Write-Host ""
    exit 0
} elseif ($Stats.Junctions -gt 0) {
    Write-Error "CRITICAL: Auth file junctions detected!"
    Write-Warning "This violates the safety protocol."
    Write-Info "Run with -FixIssues to automatically remove junctions."
    Write-Host ""
    exit 1
} else {
    Write-Warning "Validation completed with warnings."
    Write-Info "Review the output above for details."
    Write-Host ""
    exit 0
}
