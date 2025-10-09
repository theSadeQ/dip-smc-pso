#==========================================================================================\\\
#==================== .dev_tools/git-hooks/Install-Hooks.ps1 =============================\\\
#==========================================================================================\\\
#
# Git Hooks Installation Script (PowerShell)
#
# This script installs the documentation quality pre-commit hook.
#
# Usage:
#   .\\.dev_tools\\git-hooks\\Install-Hooks.ps1
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

Write-ColorOutput Blue "Installing Git Hooks for Documentation Quality..."
Write-Output ""

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-ColorOutput Red "Error: Not a git repository. Run this script from the project root."
    exit 1
}

# Create hooks directory if it doesn't exist
if (-not (Test-Path ".git\hooks")) {
    New-Item -ItemType Directory -Path ".git\hooks" | Out-Null
    Write-ColorOutput Green "Created .git\hooks directory"
}

# Install pre-commit hook (Bash version for Git Bash compatibility)
if (Test-Path ".git\hooks\pre-commit") {
    Write-ColorOutput Yellow "Warning: Existing pre-commit hook found."
    Write-ColorOutput Yellow "Creating backup: .git\hooks\pre-commit.backup"
    Move-Item -Path ".git\hooks\pre-commit" -Destination ".git\hooks\pre-commit.backup" -Force
}

Copy-Item -Path ".dev_tools\git-hooks\pre-commit" -Destination ".git\hooks\pre-commit" -Force
Write-ColorOutput Green "[OK] Installed pre-commit hook (Bash version)"

# Also install PowerShell version for native Windows support
Copy-Item -Path ".dev_tools\git-hooks\pre-commit.ps1" -Destination ".git\hooks\pre-commit.ps1" -Force
Write-ColorOutput Green "[OK] Installed pre-commit.ps1 hook (PowerShell version)"

Write-Output ""
Write-ColorOutput Blue "Git Hook Installation Complete!"
Write-Output ""
Write-Output "The pre-commit hook will now:"
Write-Output "  - Scan staged markdown files in docs/ for AI-ish patterns"
Write-Output "  - Block commits with >5 patterns per file"
Write-Output "  - Enforce CLAUDE.md Section 15: Documentation Quality Standards"
Write-Output ""
Write-ColorOutput Yellow "To bypass the hook (emergency only):"
Write-Output "  git commit --no-verify"
Write-Output ""
Write-ColorOutput Green "Test the hook with:"
Write-Output "  # Stage a documentation file"
Write-Output "  git add docs\some-file.md"
Write-Output '  git commit -m "Test commit"'
Write-Output ""
Write-ColorOutput Blue "Note: Git will use the bash version (.git\hooks\pre-commit) by default."
Write-Output "The PowerShell version is available for manual testing."
Write-Output ""
