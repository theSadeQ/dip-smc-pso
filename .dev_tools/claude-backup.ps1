#==========================================================================================\
#================================== .dev_tools/claude-backup.ps1 ==========================\
#==========================================================================================\

<#
.SYNOPSIS
    Automated Git backup script for Claude Code sessions.

.DESCRIPTION
    This script automatically stages, commits, and pushes repository changes to maintain
    frequent restore points during coding sessions. It can run on a schedule (every 1 minute)
    or be invoked manually with the -Checkpoint switch.

.PARAMETER Checkpoint
    Forces an immediate backup even if a scheduled run just occurred.

.EXAMPLE
    .\claude-backup.ps1
    Run automatic backup (scheduled mode)

.EXAMPLE
    .\claude-backup.ps1 -Checkpoint
    Force manual checkpoint immediately

.NOTES
    Repository: https://github.com/theSadeQ/dip-smc-pso.git
    Working Directory: D:\Projects\main
    Log File: .\.dev_tools\backup\backup.log
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$Checkpoint
)

# Strict error handling
$ErrorActionPreference = 'Stop'
$InformationPreference = 'Continue'

#region Configuration
$REQUIRED_REMOTE = "https://github.com/theSadeQ/dip-smc-pso.git"
$DEFAULT_REPO_ROOT = "D:\Projects\main"
$LOG_DIR = ".\.dev_tools\backup"
$LOG_FILE = Join-Path $LOG_DIR "backup.log"
$TOKEN_THRESHOLD = 2000
#endregion

#region Helper Functions

function Write-Log {
    <#
    .SYNOPSIS
        Write timestamped log entry to both console and log file.
    #>
    param(
        [string]$Message,
        [ValidateSet('Info', 'Success', 'Warning', 'Error')]
        [string]$Level = 'Info'
    )

    $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"

    # Ensure log directory exists
    if (-not (Test-Path $LOG_DIR)) {
        New-Item -Path $LOG_DIR -ItemType Directory -Force | Out-Null
    }

    # Append to log file
    Add-Content -Path $LOG_FILE -Value $logEntry -ErrorAction SilentlyContinue

    # Write to console with color
    switch ($Level) {
        'Success' { Write-Host $logEntry -ForegroundColor Green }
        'Warning' { Write-Host $logEntry -ForegroundColor Yellow }
        'Error'   { Write-Host $logEntry -ForegroundColor Red }
        default   { Write-Host $logEntry }
    }
}

function Get-RepoRoot {
    <#
    .SYNOPSIS
        Determine repository root directory.
    #>
    try {
        # Try default location first
        if (Test-Path $DEFAULT_REPO_ROOT) {
            Push-Location $DEFAULT_REPO_ROOT
            $gitRoot = git rev-parse --show-toplevel 2>&1
            Pop-Location

            if ($LASTEXITCODE -eq 0) {
                return $DEFAULT_REPO_ROOT
            }
        }

        # Fall back to current directory
        $gitRoot = git rev-parse --show-toplevel 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $gitRoot
        }

        throw "Not a git repository: $DEFAULT_REPO_ROOT"
    }
    catch {
        Write-Log "Failed to determine repository root: $_" -Level Error
        exit 1
    }
}

function Assert-RemoteUrl {
    <#
    .SYNOPSIS
        Verify and correct remote repository URL.
    #>
    param([string]$RepoRoot)

    try {
        Push-Location $RepoRoot

        # Get current remote URL
        $currentRemote = git remote get-url origin 2>&1

        if ($LASTEXITCODE -ne 0) {
            Write-Log "No remote 'origin' found. Adding remote: $REQUIRED_REMOTE" -Level Warning
            git remote add origin $REQUIRED_REMOTE

            if ($LASTEXITCODE -ne 0) {
                throw "Failed to add remote origin"
            }

            Write-Log "Remote 'origin' added successfully" -Level Success
        }
        elseif ($currentRemote -ne $REQUIRED_REMOTE) {
            Write-Log "Incorrect remote URL detected. Updating to: $REQUIRED_REMOTE" -Level Warning
            git remote set-url origin $REQUIRED_REMOTE

            if ($LASTEXITCODE -ne 0) {
                throw "Failed to update remote URL"
            }

            Write-Log "Remote URL updated successfully" -Level Success
        }
        else {
            Write-Log "Remote URL verified: $REQUIRED_REMOTE" -Level Info
        }

        Pop-Location
    }
    catch {
        Pop-Location
        Write-Log "Remote URL assertion failed: $_" -Level Error
        exit 2
    }
}

function Test-HasChanges {
    <#
    .SYNOPSIS
        Check if there are changes to commit.
    #>
    param([string]$RepoRoot)

    try {
        Push-Location $RepoRoot

        # Check for unstaged, staged, or untracked files
        $status = git status --porcelain 2>&1

        Pop-Location

        return ($status.Count -gt 0)
    }
    catch {
        Pop-Location
        Write-Log "Failed to check repository status: $_" -Level Error
        exit 3
    }
}

function Invoke-GitBackup {
    <#
    .SYNOPSIS
        Execute the backup: stage, commit, push.
    #>
    param([string]$RepoRoot)

    try {
        Push-Location $RepoRoot

        # Stage all changes
        Write-Log "Staging all changes..." -Level Info
        git add -A

        if ($LASTEXITCODE -ne 0) {
            throw "git add failed with exit code $LASTEXITCODE"
        }

        # Double-check if there are changes after staging
        $diffCached = git diff --cached --quiet 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "No changes to commit after staging. Exiting." -Level Info
            Pop-Location
            exit 0
        }

        # Generate commit message
        $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
        $commitMessage = @"
Auto-backup: $timestamp

- Staged working directory changes
- Periodic checkpoint from CI agent
- Includes files modified during this session

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"@

        # Commit changes
        Write-Log "Creating commit: Auto-backup: $timestamp" -Level Info
        git commit -m $commitMessage

        if ($LASTEXITCODE -ne 0) {
            throw "git commit failed with exit code $LASTEXITCODE"
        }

        # Push to remote
        Write-Log "Pushing to origin/main..." -Level Info
        git push origin main

        if ($LASTEXITCODE -ne 0) {
            throw "git push failed with exit code $LASTEXITCODE. Check authentication or network."
        }

        Write-Log "Backup completed successfully!" -Level Success
        Pop-Location
        exit 0
    }
    catch {
        Pop-Location
        Write-Log "Backup failed: $_" -Level Error

        # Provide actionable hints
        if ($_.Exception.Message -match "authentication|credentials") {
            Write-Log "Hint: Configure Git credential helper or use Personal Access Token" -Level Warning
        }
        elseif ($_.Exception.Message -match "lock|index.lock") {
            Write-Log "Hint: Another Git process may be running. Wait and retry." -Level Warning
        }
        elseif ($_.Exception.Message -match "network|connection") {
            Write-Log "Hint: Check network connectivity to GitHub" -Level Warning
        }

        exit 4
    }
}

function Test-TokenThreshold {
    <#
    .SYNOPSIS
        Check if CLAUDE_TOKENS_LEFT is below threshold.
    #>
    try {
        $tokensLeft = $env:CLAUDE_TOKENS_LEFT

        if ($null -ne $tokensLeft -and $tokensLeft -match '^\d+$') {
            $tokens = [int]$tokensLeft

            if ($tokens -lt $TOKEN_THRESHOLD) {
                Write-Log "Token threshold triggered ($tokens < $TOKEN_THRESHOLD). Forcing backup." -Level Warning
                return $true
            }
        }

        return $false
    }
    catch {
        # Silently ignore token check errors
        return $false
    }
}

#endregion

#region Main Execution

try {
    Write-Log "=== Claude Code Auto-Backup Script ===" -Level Info

    # Ensure Git is in PATH (fixes Task Scheduler issue)
    $gitPaths = @(
        "C:\Program Files\Git\cmd",
        "C:\Program Files (x86)\Git\cmd",
        "C:\Git\cmd"
    )
    foreach ($gitPath in $gitPaths) {
        if (Test-Path $gitPath) {
            $env:PATH = "$gitPath;$env:PATH"
            Write-Log "Added Git to PATH: $gitPath" -Level Info
            break
        }
    }

    # Ensure we're in the correct working directory (fixes Task Scheduler issue)
    if (Test-Path $DEFAULT_REPO_ROOT) {
        Set-Location $DEFAULT_REPO_ROOT
        Write-Log "Working directory set to: $DEFAULT_REPO_ROOT" -Level Info
    }

    # Determine repository root
    $repoRoot = Get-RepoRoot
    Write-Log "Repository root: $repoRoot" -Level Info

    # Verify/correct remote URL
    Assert-RemoteUrl -RepoRoot $repoRoot

    # Check for changes
    $hasChanges = Test-HasChanges -RepoRoot $repoRoot

    if (-not $hasChanges) {
        Write-Log "No changes detected. Exiting cleanly." -Level Info
        exit 0
    }

    Write-Log "Changes detected. Proceeding with backup..." -Level Info

    # Check token threshold (optional emergency backup)
    $lowTokens = Test-TokenThreshold
    if ($lowTokens) {
        Write-Log "Emergency backup triggered by low token count!" -Level Warning
    }

    # Execute backup
    Invoke-GitBackup -RepoRoot $repoRoot
}
catch {
    Write-Log "Unhandled exception: $_" -Level Error
    exit 99
}

#endregion
