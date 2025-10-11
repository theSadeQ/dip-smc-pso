# Diagnostic script for Claude directories
Write-Host "=== Claude Directory Diagnostic ===" -ForegroundColor Cyan

# Check CLAUDE_CONFIG_DIR
Write-Host "`nCurrent CLAUDE_CONFIG_DIR: " -NoNewline
if ($env:CLAUDE_CONFIG_DIR) {
    Write-Host $env:CLAUDE_CONFIG_DIR -ForegroundColor Yellow
} else {
    Write-Host "Not set" -ForegroundColor Green
}

# Check for primary .claude
Write-Host "`nPrimary .claude directory:"
if (Test-Path "$env:USERPROFILE\.claude") {
    Write-Host "EXISTS at $env:USERPROFILE\.claude" -ForegroundColor Green
    Get-ChildItem "$env:USERPROFILE\.claude" -Force | Select-Object Name, Mode, LinkType, Length
} else {
    Write-Host "DOES NOT EXIST" -ForegroundColor Yellow
}

# Check for numbered .claude directories
Write-Host "`n=== Numbered .claude Directories ===" -ForegroundColor Cyan
$found = $false
1..35 | ForEach-Object {
    $dir = "$env:USERPROFILE\.claude$_"
    if (Test-Path $dir) {
        $found = $true
        $count = (Get-ChildItem $dir -Force -ErrorAction SilentlyContinue).Count
        Write-Host "Account ${_}: $count files" -ForegroundColor Green

        # Check for junctions
        $junctions = Get-ChildItem $dir -Force -ErrorAction SilentlyContinue | Where-Object { $_.LinkType -eq 'Junction' }
        if ($junctions) {
            $junctions | ForEach-Object {
                Write-Host "  Junction: $($_.Name) -> $($_.Target)" -ForegroundColor Yellow
            }
        }
    }
}

if (-not $found) {
    Write-Host "No numbered .claude directories found" -ForegroundColor Yellow
}

Write-Host "`n=== Recommendation ===" -ForegroundColor Cyan
if ($env:CLAUDE_CONFIG_DIR) {
    Write-Host "You have CLAUDE_CONFIG_DIR set. Run this to clear it:" -ForegroundColor Yellow
    Write-Host '  Remove-Item Env:\CLAUDE_CONFIG_DIR' -ForegroundColor White
}
