# ============================================================================
# Switch-ClaudeAccount.ps1
# Dynamic Account Switcher with Safety Protocol
# ============================================================================
#
# Purpose: Safe multi-account switching for Claude Code with auth isolation
# Author: Claude Code Multi-Account System
# Created: 2025-10-11
#
# Features:
# - Isolated authentication per account
# - Session state tracking integration
# - Safety checks (no auth file sharing)
# - Auto-creates account directories
# - Validates account structure
#
# Usage:
#   Switch-ClaudeAccount -AccountNum 5
#   Switch-ClaudeAccount -AccountNum 1 -NoLaunch
#   Switch-ClaudeAccount -Primary  # Return to primary .claude
#
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [int]$AccountNum,

    [Parameter(Mandatory=$false)]
    [switch]$Primary,

    [Parameter(Mandatory=$false)]
    [switch]$NoLaunch,

    [Parameter(Mandatory=$false)]
    [switch]$Validate
)

# Configuration
$PrimaryClaudeDir = "$env:USERPROFILE\.claude"
$SessionStateFile = "D:\Projects\main\.ai\config\session_state.json"
$MaxAccounts = 50000  # Extended to support up to 50000 accounts

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

function Test-PrimaryDirectory {
    if (-not (Test-Path $PrimaryClaudeDir)) {
        Write-Error "Primary .claude directory not found at: $PrimaryClaudeDir"
        Write-Info "This system requires a primary Claude Code installation."
        return $false
    }
    Write-Success "Primary .claude directory exists"
    return $true
}

function Test-NoAuthJunctions {
    param([string]$AccountDir)

    $authFiles = @(".credentials.json", "history.jsonl", ".claude.json")
    $junctions = @()

    foreach ($file in $authFiles) {
        $path = Join-Path $AccountDir $file
        if (Test-Path $path) {
            $item = Get-Item $path -Force
            if ($item.LinkType -eq "Junction" -or $item.LinkType -eq "SymbolicLink") {
                $junctions += $file
            }
        }
    }

    if ($junctions.Count -gt 0) {
        Write-Error "Auth file junctions detected: $($junctions -join ', ')"
        Write-Error "This violates safety protocol. Remove junctions before continuing."
        return $false
    }

    return $true
}

function Initialize-AccountDirectory {
    param([int]$AccNum)

    $accountDir = "$env:USERPROFILE\.claude$AccNum"
    $needsInit = $false

    if (-not (Test-Path $accountDir)) {
        Write-Info "Creating account directory: $accountDir"
        New-Item -ItemType Directory -Path $accountDir -Force | Out-Null
        $needsInit = $true
        Write-Success "Account directory created"
    } else {
        Write-Info "Account directory exists: $accountDir"
        # Check if subdirectories exist
        if (-not (Test-Path "$accountDir\ide") -or -not (Test-Path "$accountDir\projects")) {
            $needsInit = $true
        }
    }

    # Initialize required subdirectories
    if ($needsInit) {
        Write-Info "Initializing account directory structure..."

        # Required subdirectories for Claude Code
        $requiredDirs = @("ide", "projects", "session-env", "shell-snapshots", "statsig", "todos", "debug", "downloads")

        foreach ($dir in $requiredDirs) {
            $targetDir = Join-Path $accountDir $dir
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            }
        }

        Write-Success "Account structure initialized ($($requiredDirs.Count) directories)"
    }

    # Validate no auth junctions
    if (-not (Test-NoAuthJunctions $accountDir)) {
        return $null
    }

    return $accountDir
}

function Update-SessionState {
    param([int]$AccNum)

    if (-not (Test-Path $SessionStateFile)) {
        Write-Warning "Session state file not found: $SessionStateFile"
        return
    }

    try {
        $sessionState = Get-Content $SessionStateFile -Raw | ConvertFrom-Json

        # Update account field
        if ($AccNum -eq 0) {
            $sessionState.account = "primary"
        } else {
            $sessionState.account = "account_$AccNum"
        }

        # Update timestamp
        $sessionState.last_updated = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")

        # Save back
        $sessionState | ConvertTo-Json -Depth 10 | Set-Content $SessionStateFile -Encoding UTF8
        Write-Success "Session state updated: account_$AccNum"

    } catch {
        Write-Warning "Could not update session state: $_"
    }
}

function Get-AccountStatus {
    param([int]$AccNum)

    $accountDir = "$env:USERPROFILE\.claude$AccNum"

    if (-not (Test-Path $accountDir)) {
        return @{
            Exists = $false
            Authenticated = $false
            FileCount = 0
            DirsInitialized = $false
        }
    }

    $credFile = Join-Path $accountDir ".credentials.json"
    $authenticated = Test-Path $credFile
    $fileCount = (Get-ChildItem $accountDir -Force -ErrorAction SilentlyContinue).Count

    # Check if directories are initialized
    $dirsInitialized = (Test-Path "$accountDir\ide") -and (Test-Path "$accountDir\projects")

    return @{
        Exists = $true
        Authenticated = $authenticated
        FileCount = $fileCount
        DirsInitialized = $dirsInitialized
    }
}

# ============================================================================
# Main Logic
# ============================================================================

# Validate mode
if ($Validate) {
    Write-Info "Running account validation..."

    if (-not (Test-PrimaryDirectory)) {
        exit 1
    }

    Write-Info "Checking accounts 1-$MaxAccounts..."

    $results = @()
    1..$MaxAccounts | ForEach-Object {
        $status = Get-AccountStatus $_
        if ($status.Exists) {
            Write-Host "  Account $_`: " -NoNewline -ForegroundColor White

            if ($status.Authenticated) {
                Write-Host "[OK] Authenticated" -NoNewline -ForegroundColor Green
            } else {
                Write-Host "[!] Needs login" -NoNewline -ForegroundColor Yellow
            }

            Write-Host " | Dirs: " -NoNewline
            if ($status.DirsInitialized) {
                Write-Host "[OK]" -NoNewline -ForegroundColor Green
            } else {
                Write-Host "[X]" -NoNewline -ForegroundColor Red
            }

            Write-Host " | Files: $($status.FileCount)" -ForegroundColor Gray
            $results += $_
        }
    }

    if ($results.Count -eq 0) {
        Write-Info "No account directories found. Run switcher to create accounts."
    } else {
        Write-Success "Found $($results.Count) account(s)"
    }

    exit 0
}

# Primary mode
if ($Primary) {
    Write-Info "Switching to primary .claude directory..."

    if (-not (Test-PrimaryDirectory)) {
        exit 1
    }

    # Clear CLAUDE_CONFIG_DIR (both session and persistent)
    if ($env:CLAUDE_CONFIG_DIR) {
        Remove-Item Env:\CLAUDE_CONFIG_DIR
        [Environment]::SetEnvironmentVariable("CLAUDE_CONFIG_DIR", $null, "User")
        Write-Success "Cleared CLAUDE_CONFIG_DIR (persistent)"
    }

    Update-SessionState -AccNum 0

    Write-Success "Now using primary .claude directory"
    Write-Info "Location: $PrimaryClaudeDir"

    if (-not $NoLaunch) {
        Write-Info "Launching Claude Code..."
        & claude --dangerously-skip-permissions
    }

    exit 0
}

# Account switching mode
if (-not $AccountNum) {
    Write-Error "Missing required parameter: -AccountNum or -Primary"
    Write-Info "Usage: Switch-ClaudeAccount -AccountNum 5"
    Write-Info "       Switch-ClaudeAccount -Primary"
    Write-Info "       Switch-ClaudeAccount -Validate"
    exit 1
}

if ($AccountNum -lt 1 -or $AccountNum -gt $MaxAccounts) {
    Write-Error "Account number must be between 1 and $MaxAccounts"
    exit 1
}

Write-Info "Switching to Claude Code Account $AccountNum..."

# Validate primary directory
if (-not (Test-PrimaryDirectory)) {
    exit 1
}

# Initialize account directory
$accountDir = Initialize-AccountDirectory -AccNum $AccountNum
if (-not $accountDir) {
    Write-Error "Failed to initialize account directory"
    exit 1
}

# Set environment variable (PERSISTENT across sessions)
$env:CLAUDE_CONFIG_DIR = $accountDir
[Environment]::SetEnvironmentVariable("CLAUDE_CONFIG_DIR", $accountDir, "User")
Write-Success "Set CLAUDE_CONFIG_DIR (persistent): $accountDir"

# Update session state
Update-SessionState -AccNum $AccountNum

# Check authentication status
$status = Get-AccountStatus $AccountNum
if (-not $status.Authenticated) {
    Write-Warning "Account $AccountNum needs authentication"
    Write-Info "Claude Code will prompt for login on first use"
} else {
    Write-Success "Account $AccountNum is authenticated"
}

Write-Success "Successfully switched to Account $AccountNum"

# Launch Claude Code
if (-not $NoLaunch) {
    Write-Info "Launching Claude Code..."
    & claude --dangerously-skip-permissions
}

exit 0
