# Perplexity MCP Server Setup Guide

## Quick Setup

### 1. Set Environment Variable

**Windows (PowerShell - Session Only):**
```powershell
$env:PERPLEXITY_API_KEY = "pplx-D2DWVb3Iv4..."  # Replace with your full API key
```

**Windows (CMD - Session Only):**
```cmd
set PERPLEXITY_API_KEY=pplx-D2DWVb3Iv4...  # Replace with your full API key
```

**Windows (Permanent - System Environment Variables):**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to "Advanced" tab → "Environment Variables"
3. Under "User variables", click "New"
4. Variable name: `PERPLEXITY_API_KEY`
5. Variable value: `pplx-D2DWVb3Iv4...` (your full API key from Perplexity dashboard)
6. Click OK, restart your terminal/IDE

**Linux/macOS (Session Only):**
```bash
export PERPLEXITY_API_KEY="pplx-D2DWVb3Iv4..."  # Replace with your full API key
```

**Linux/macOS (Permanent):**
```bash
# Add to ~/.bashrc or ~/.zshrc:
echo 'export PERPLEXITY_API_KEY="pplx-D2DWVb3Iv4..."' >> ~/.bashrc
source ~/.bashrc
```

### 2. Verify Environment Variable

**Windows (PowerShell):**
```powershell
echo $env:PERPLEXITY_API_KEY
```

**Windows (CMD):**
```cmd
echo %PERPLEXITY_API_KEY%
```

**Linux/macOS:**
```bash
echo $PERPLEXITY_API_KEY
```

Should output: `pplx-D2DWVb3Iv4...`

### 3. Restart Claude Code

After setting the environment variable:
1. Close Claude Code completely
2. Reopen Claude Code
3. The Perplexity MCP server will auto-load on startup

## Verification

Once setup is complete, test the integration:

```bash
# Natural language test (Claude auto-triggers Perplexity):
"What does recent research say about chattering mitigation in sliding mode control?"

# Explicit research query:
"Research papers on PSO parameter tuning for control systems"

# Literature validation:
"Validate our STA-SMC implementation against published methods"
```

## Configuration Details

**MCP Server Config**: `.mcp.json` (already configured)
**Auto-trigger Keywords**: research, literature, papers, validate theory, citations, state of the art
**Server Type**: NPM package via npx (`@perplexity-ai/mcp-server`)

## Troubleshooting

**Server Not Starting:**
```bash
# 1. Verify environment variable is set:
echo $env:PERPLEXITY_API_KEY  # PowerShell
echo %PERPLEXITY_API_KEY%     # CMD
echo $PERPLEXITY_API_KEY      # Linux/macOS

# 2. Check npx is available:
npx --version

# 3. Restart Claude Code after setting variable
```

**API Key Invalid:**
- Go to Perplexity dashboard: https://www.perplexity.ai/settings/api
- Verify key starts with `pplx-`
- Generate new key if needed
- Update environment variable

**MCP Not Triggering:**
- Use research-related keywords: "research", "literature", "papers on"
- Example: "Research recent work on adaptive SMC" (triggers automatically)

## Security Notes

- **Never commit** API keys to git
- **Do not hardcode** keys in scripts
- **Use environment variables** only
- **Rotate keys** if exposed

## Usage Patterns

**Literature Review Workflow:**
1. User: "Research papers on X"
2. Claude auto-triggers: perplexity → context7 → filesystem
3. Result: Published research + local implementation analysis

**Theory Validation:**
1. User: "Validate our controller against published methods"
2. Claude auto-triggers: perplexity → filesystem → sequential-thinking
3. Result: Literature comparison + recommendations

**Citation Discovery:**
1. User: "Find citations for chattering mitigation claims"
2. Claude auto-triggers: perplexity → context7
3. Result: Relevant papers with DOIs

## Advanced: Claude Code Settings

**MCP Enabled**: `.ai/config/settings.local.json` contains:
```json
{
  "enableAllProjectMcpServers": true
}
```

**Server Status Check:**
In Claude Code, type: `/mcp status` (if available) or check logs for startup messages.

## API Key Management

**Your API Key** (from Perplexity dashboard):
- Name: `first`
- Key: `pplx-D2DWVb3Iv4...` (partial shown)
- Last Used: Never (as of setup date)

**Rate Limits** (check Perplexity dashboard):
- Free tier: Limited requests/month
- Pro tier: Higher limits

**Best Practices:**
- Monitor usage via Perplexity dashboard
- Set up billing alerts if using paid tier
- Test with simple queries first

## Integration Status

✅ MCP server added to `.mcp.json`
✅ Auto-trigger rules added to `CLAUDE.md`
✅ Research workflow patterns defined
✅ Environment variable setup guide created

**Next**: Set environment variable → Restart Claude Code → Test with research query

## See Also

- `.mcp.json` - Full MCP server configuration
- `CLAUDE.md` Section 20.1 - Perplexity auto-trigger rules
- `docs/mcp-debugging/README.md` - MCP troubleshooting guide
- Perplexity API Docs: https://docs.perplexity.ai/
