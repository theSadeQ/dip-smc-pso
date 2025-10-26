#==========================================================================================\\\
#====================== .dev_tools/git-hooks/pre-commit.ps1 ==============================\\\
#==========================================================================================\\\
#
# Documentation Quality Pre-Commit Hook (PowerShell Version)
#
# This hook enforces CLAUDE.md Section 15: Documentation Quality Standards
# by scanning staged markdown files for AI-ish language patterns.
#
# Installation:
#   Copy-Item .dev_tools\git-hooks\pre-commit.ps1 .git\hooks\pre-commit.ps1
#   # Configure git to use PowerShell hooks (if not already configured)
#   git config core.hooksPath .git\hooks
#
# For WSL/Git Bash compatibility, also install the bash version:
#   cp .dev_tools/git-hooks/pre-commit .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Bypass (emergency only):
#   git commit --no-verify
#
#==========================================================================================\\\

# Color output functions
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Blue "[PRE-COMMIT] Running documentation quality checks..."

# Get staged markdown files in docs/
$StagedMdFiles = git diff --cached --name-only --diff-filter=ACM | Where-Object { $_ -match '^docs/.*\.md$' }

if (-not $StagedMdFiles) {
    Write-ColorOutput Green "[PRE-COMMIT] No documentation files staged. Skipping quality checks."
    exit 0
}

$FileCount = ($StagedMdFiles | Measure-Object).Count
Write-ColorOutput Blue "[PRE-COMMIT] Checking $FileCount staged documentation files..."

# Initialize counters
$TotalFiles = 0
$FailedFiles = 0
$TotalPatterns = 0
$FailedFilesList = @()

# Check if pattern detection script exists
if (-not (Test-Path "scripts\docs\detect_ai_patterns.py")) {
    Write-ColorOutput Yellow "[PRE-COMMIT] Warning: Pattern detection script not found. Skipping quality checks."
    exit 0
}

# Check each staged markdown file
foreach ($File in $StagedMdFiles) {
    $TotalFiles++

    Write-ColorOutput Blue "[PRE-COMMIT] Scanning: $File"

    # Run pattern detection on the file
    try {
        $PatternOutput = python scripts\docs\detect_ai_patterns.py --file $File 2>&1

        # Extract pattern count from output
        if ($PatternOutput -match 'Total AI-ish patterns: (\d+)') {
            $PatternCount = [int]$Matches[1]
        } else {
            $PatternCount = 0
        }

        $TotalPatterns += $PatternCount

        # Check if file exceeds threshold (5 patterns per file)
        if ($PatternCount -gt 5) {
            $FailedFiles++
            Write-ColorOutput Red "[FAIL] $File: $PatternCount patterns detected (threshold: 5)"
            $FailedFilesList += @{
                File = $File
                Count = $PatternCount
                Output = $PatternOutput
            }
        } elseif ($PatternCount -gt 0) {
            Write-ColorOutput Yellow "[WARN] $File: $PatternCount patterns detected (acceptable: ≤5)"
        } else {
            Write-ColorOutput Green "[PASS] $File: No AI-ish patterns detected"
        }
    } catch {
        Write-ColorOutput Yellow "[WARN] Error scanning $File: $_"
    }
}

# Summary
Write-Output ""
Write-ColorOutput Blue "========================================"
Write-ColorOutput Blue "Documentation Quality Check Summary"
Write-ColorOutput Blue "========================================"
Write-Output "Files scanned: $TotalFiles"
Write-Output "Total AI-ish patterns: $TotalPatterns"
Write-Output "Files exceeding threshold: $FailedFiles"

# Decide whether to block commit
if ($FailedFiles -gt 0) {
    Write-Output ""
    Write-ColorOutput Red "========================================"
    Write-ColorOutput Red "COMMIT BLOCKED: Documentation Quality Failure"
    Write-ColorOutput Red "========================================"
    Write-Output ""
    Write-ColorOutput Red "$FailedFiles file(s) exceed the AI-ish pattern threshold (>5 patterns per file)."
    Write-Output ""
    Write-ColorOutput Yellow "Please review and fix the following issues:"

    foreach ($FailedFile in $FailedFilesList) {
        Write-Output ""
        Write-ColorOutput Red "File: $($FailedFile.File) - $($FailedFile.Count) patterns"
        Write-Output $FailedFile.Output
    }

    Write-Output ""
    Write-ColorOutput Yellow "Guidance:"
    Write-Output "  1. Review CLAUDE.md Section 15: Documentation Quality Standards"
    Write-Output "  2. Consult docs\DOCUMENTATION_STYLE_GUIDE.md for professional writing guidelines"
    Write-Output "  3. Run: python scripts\docs\suggest_fixes.py --file <filename> for automated suggestions"
    Write-Output ""
    Write-ColorOutput Yellow "To bypass this check (emergency only):"
    Write-Output "  git commit --no-verify"
    Write-Output ""

    exit 1
} else {
    Write-Output ""
    Write-ColorOutput Green "========================================"
    Write-ColorOutput Green "COMMIT APPROVED: Documentation Quality Passed"
    Write-ColorOutput Green "========================================"
    Write-Output ""

    exit 0
}
