# Perplexity API Setup Script for PowerShell
# Run this script to set up your Perplexity API key for the current session

Write-Host "Setting up Perplexity API key..." -ForegroundColor Cyan

# Set the environment variable for current session
$env:PERPLEXITY_API_KEY = "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"

# Verify it's set
if ($env:PERPLEXITY_API_KEY) {
    Write-Host "✓ Environment variable set successfully!" -ForegroundColor Green
    Write-Host "  Key: $($env:PERPLEXITY_API_KEY.Substring(0, 15))..." -ForegroundColor Gray
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Restart Claude Code for changes to take effect" -ForegroundColor White
    Write-Host "2. After restart, test with: 'Research recent papers on SMC chattering mitigation'" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: This sets the variable for the current PowerShell session only." -ForegroundColor Magenta
    Write-Host "For permanent setup, see: .ai/config/perplexity_setup.md" -ForegroundColor Magenta
} else {
    Write-Host "✗ Failed to set environment variable" -ForegroundColor Red
    Write-Host "Please set manually or see .ai/config/perplexity_setup.md" -ForegroundColor Yellow
}
