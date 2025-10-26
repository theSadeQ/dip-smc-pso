# ==============================================================================
# PowerShell Initialization - Automatic Recovery on Terminal Startup
# ==============================================================================
# Add this to your PowerShell profile ($PROFILE) for automatic recovery prompts:
#
#   if (Test-Path "D:\Projects\main\.dev_tools\shell_init.ps1") {
#       . "D:\Projects\main\.dev_tools\shell_init.ps1"
#   }
#
# Features:
#   - Detects if you're in the project directory
#   - Prompts for recovery if git commits detected since last session
#   - Silent if no recovery needed
# ==============================================================================

# Only run if in the project directory
if ($PWD.Path -like "*\Projects\main*") {
    try {
        $ProjectRoot = git rev-parse --show-toplevel 2>$null
        if ($ProjectRoot -and (Test-Path "$ProjectRoot\.dev_tools\recover_project.sh")) {
            $StateFile = "$ProjectRoot\.ai\config\project_state.json"
            $LastRecoveryFile = "$ProjectRoot\.ai\config\.last_recovery"

            # Check if recovery needed (new commits since last recovery)
            $CurrentCommit = git rev-parse HEAD 2>$null
            $LastRecovery = ""

            if (Test-Path $LastRecoveryFile) {
                $LastRecovery = Get-Content $LastRecoveryFile -ErrorAction SilentlyContinue
            }

            # Recovery needed if:
            #   1. Never recovered before, OR
            #   2. New commits since last recovery
            if ([string]::IsNullOrEmpty($LastRecovery) -or ($CurrentCommit -ne $LastRecovery)) {
                Write-Host ""
                Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                Write-Host "[INFO] New commits detected - recovery available"
                Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                Write-Host ""
                Write-Host "Run: bash .dev_tools/recover_project.sh"
                Write-Host "      (30-second context restoration)"
                Write-Host ""

                # Optional: Auto-recover on startup (uncomment to enable)
                # bash "$ProjectRoot\.dev_tools\recover_project.sh"
                # $CurrentCommit | Out-File -FilePath $LastRecoveryFile -Encoding utf8
            }
        }
    }
    catch {
        # Silently ignore errors (not in a git repo, etc.)
    }
}
