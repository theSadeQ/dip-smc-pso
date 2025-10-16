# ==============================================================================
# Wave 3 Streamlit Theme Validation Automation
# ==============================================================================
# Automates the complete validation pipeline:
# 1. Baseline screenshots (theme disabled)
# 2. Themed screenshots (theme enabled)
# 3. Visual regression analysis
# 4. Accessibility audit
# 5. Performance measurement
# 6. Comparison analysis & summary
#
# Usage: .\run_wave3_validation.ps1
# ==============================================================================

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Colors for output
function Write-Step { param($msg) Write-Host "[STEP] $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Yellow }

# Configuration
$ProjectRoot = "D:\Projects\main"
$ValidationDir = "$ProjectRoot\.codex\phase3\validation\streamlit"
$ConfigFile = "$ProjectRoot\config.yaml"
$ConfigBackup = "$ConfigFile.wave3_backup"
$StreamlitApp = "$ProjectRoot\streamlit_app.py"
$StreamlitPort = 8501
$StreamlitUrl = "http://localhost:$StreamlitPort"

# ==============================================================================
# Step 0: Prerequisites Check
# ==============================================================================
Write-Step "Checking prerequisites..."

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python: $pythonVersion"
} catch {
    Write-Error "Python not found. Install Python 3.9+ and try again."
    exit 1
}

# Check Streamlit
try {
    $streamlitVersion = streamlit --version 2>&1
    Write-Success "Streamlit: $streamlitVersion"
} catch {
    Write-Error "Streamlit not found. Run: pip install streamlit"
    exit 1
}

# Check Playwright
try {
    python -c "import playwright; print('Playwright installed')" 2>&1 | Out-Null
    Write-Success "Playwright: installed"
} catch {
    Write-Error "Playwright not found. Run: pip install playwright && python -m playwright install chromium"
    exit 1
}

# Check validation scripts
$requiredScripts = @(
    "wave3_screenshot_capture.py",
    "wave3_visual_regression.py",
    "wave3_axe_audit.py",
    "wave3_performance.py",
    "wave3_comparison_analysis.py"
)

foreach ($script in $requiredScripts) {
    if (-not (Test-Path "$ValidationDir\$script")) {
        Write-Error "Missing script: $script"
        exit 1
    }
}
Write-Success "All validation scripts found"

# ==============================================================================
# Step 1: Backup config.yaml
# ==============================================================================
Write-Step "Backing up config.yaml..."
Copy-Item -Path $ConfigFile -Destination $ConfigBackup -Force
Write-Success "Backup created: $ConfigBackup"

# ==============================================================================
# Helper Functions
# ==============================================================================
function Set-StreamlitTheme {
    param([bool]$Enable)

    $content = Get-Content -Path $ConfigFile -Raw
    if ($Enable) {
        $content = $content -replace "enable_dip_theme:\s*false", "enable_dip_theme: true"
        Write-Info "Theme ENABLED in config.yaml"
    } else {
        $content = $content -replace "enable_dip_theme:\s*true", "enable_dip_theme: false"
        Write-Info "Theme DISABLED in config.yaml"
    }
    Set-Content -Path $ConfigFile -Value $content -NoNewline
}

function Start-StreamlitServer {
    Write-Info "Starting Streamlit server on port $StreamlitPort..."

    # Start Streamlit in background
    $job = Start-Job -ScriptBlock {
        param($app, $port)
        Set-Location "D:\Projects\main"
        streamlit run $app --server.port $port --server.headless true
    } -ArgumentList $StreamlitApp, $StreamlitPort

    # Wait for server to be ready (max 60 seconds)
    $timeout = 60
    $elapsed = 0
    while ($elapsed -lt $timeout) {
        try {
            $response = Invoke-WebRequest -Uri $StreamlitUrl -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Success "Streamlit server ready at $StreamlitUrl"
                return $job
            }
        } catch {
            # Server not ready yet
        }
        Start-Sleep -Seconds 2
        $elapsed += 2
        Write-Host "." -NoNewline
    }

    Write-Error "Streamlit server failed to start after $timeout seconds"
    Stop-Job -Job $job -ErrorAction SilentlyContinue
    Remove-Job -Job $job -ErrorAction SilentlyContinue
    exit 1
}

function Stop-StreamlitServer {
    param($Job)

    if ($Job) {
        Write-Info "Stopping Streamlit server..."
        Stop-Job -Job $Job -ErrorAction SilentlyContinue
        Remove-Job -Job $Job -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        Write-Success "Streamlit server stopped"
    }
}

function Run-ValidationScript {
    param([string]$ScriptName, [string]$Description)

    Write-Step "Running: $Description"
    Set-Location $ValidationDir

    try {
        python $ScriptName
        if ($LASTEXITCODE -eq 0) {
            Write-Success "$Description completed"
            return $true
        } else {
            Write-Error "$Description failed with exit code $LASTEXITCODE"
            return $false
        }
    } catch {
        Write-Error "$Description failed: $_"
        return $false
    }
}

# ==============================================================================
# Step 2: Baseline Screenshots (theme disabled)
# ==============================================================================
Write-Step "Phase 1: Baseline Screenshots (theme disabled)"
Set-StreamlitTheme -Enable $false

$streamlitJob = Start-StreamlitServer
Start-Sleep -Seconds 3  # Give UI time to fully render

$baselineSuccess = Run-ValidationScript "wave3_screenshot_capture.py" "Baseline screenshot capture"

Stop-StreamlitServer -Job $streamlitJob

if (-not $baselineSuccess) {
    Write-Error "Baseline screenshots failed. Restoring config.yaml..."
    Copy-Item -Path $ConfigBackup -Destination $ConfigFile -Force
    exit 1
}

# ==============================================================================
# Step 3: Themed Screenshots (theme enabled)
# ==============================================================================
Write-Step "Phase 2: Themed Screenshots (theme enabled)"
Set-StreamlitTheme -Enable $true

$streamlitJob = Start-StreamlitServer
Start-Sleep -Seconds 3  # Give UI time to fully render

$themedSuccess = Run-ValidationScript "wave3_screenshot_capture.py" "Themed screenshot capture"

# Keep Streamlit running for axe audit
if (-not $themedSuccess) {
    Write-Error "Themed screenshots failed. Restoring config.yaml..."
    Stop-StreamlitServer -Job $streamlitJob
    Copy-Item -Path $ConfigBackup -Destination $ConfigFile -Force
    exit 1
}

# ==============================================================================
# Step 4: Visual Regression Analysis
# ==============================================================================
$regressionSuccess = Run-ValidationScript "wave3_visual_regression.py" "Visual regression analysis"

# ==============================================================================
# Step 5: Accessibility Audit (requires Streamlit running)
# ==============================================================================
$a11ySuccess = Run-ValidationScript "wave3_axe_audit.py" "Accessibility audit (axe-core)"

# ==============================================================================
# Step 6: Performance Measurement
# ==============================================================================
$perfSuccess = Run-ValidationScript "wave3_performance.py" "Performance measurement"

# Stop Streamlit (no longer needed)
Stop-StreamlitServer -Job $streamlitJob

# ==============================================================================
# Step 7: Comparison Analysis & Summary
# ==============================================================================
$summarySuccess = Run-ValidationScript "wave3_comparison_analysis.py" "Comparison analysis & summary"

# ==============================================================================
# Step 8: Restore config.yaml
# ==============================================================================
Write-Step "Restoring config.yaml from backup..."
Copy-Item -Path $ConfigBackup -Destination $ConfigFile -Force
Remove-Item -Path $ConfigBackup -Force
Write-Success "config.yaml restored"

# ==============================================================================
# Step 9: Results Summary
# ==============================================================================
Write-Host "`n" + "="*80
Write-Host "WAVE 3 VALIDATION RESULTS" -ForegroundColor Cyan
Write-Host "="*80

$allSuccess = $baselineSuccess -and $themedSuccess -and $regressionSuccess -and $a11ySuccess -and $perfSuccess -and $summarySuccess

Write-Host "Baseline Screenshots: " -NoNewline
if ($baselineSuccess) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "Themed Screenshots: " -NoNewline
if ($themedSuccess) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "Visual Regression: " -NoNewline
if ($regressionSuccess) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "Accessibility Audit: " -NoNewline
if ($a11ySuccess) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "Performance: " -NoNewline
if ($perfSuccess) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "Summary Generation: " -NoNewline
if ($summarySuccess) { Write-Host "PASS" -ForegroundColor Green } else { Write-Host "FAIL" -ForegroundColor Red }

Write-Host "="*80
Write-Host "Overall Status: " -NoNewline
if ($allSuccess) {
    Write-Host "PASS - All validations successful!" -ForegroundColor Green
    Write-Host "`nNext steps:"
    Write-Host "1. Review VALIDATION_SUMMARY.md in wave3/ directory"
    Write-Host "2. Proceed to Task 2 (Sphinx interaction polish)"
} else {
    Write-Host "FAIL - Some validations failed" -ForegroundColor Red
    Write-Host "`nAction required:"
    Write-Host "1. Review error messages above"
    Write-Host "2. Check individual validation reports in wave3/ directory"
    Write-Host "3. Fix issues and re-run validation"
}
Write-Host "="*80 + "`n"

exit 0
