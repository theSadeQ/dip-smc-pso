# GitHub Token Setup for MCP Server

## Token Configuration

**Token Name**: `claude-code-mcp`

**Expiration**: 90 days (recommended) or longer

**Required Scopes** (check these boxes):

### Repository Access
- ✅ **repo** - Full control of private repositories
  - Includes: `repo:status`, `repo_deployment`, `public_repo`, `repo:invite`, `security_events`

### Organization Access
- ✅ **read:org** - Read org and team membership, read org projects

### User Access
- ✅ **read:user** - Read ALL user profile data
- ✅ **user:email** - Access user email addresses (read-only)

### Optional (for advanced workflows)
- ⬜ **workflow** - Update GitHub Action workflows (if you plan to manage CI/CD)
- ⬜ **read:discussion** - Read team discussions

---

## Minimum Scopes for Basic MCP Functionality

If you only need basic repository operations:
- ✅ **public_repo** (instead of full `repo` if you only work with public repos)
- ✅ **read:user**

**IMPORTANT**: The MCP server won't work without at least `public_repo` or `repo` scope.

---

## Installation Instructions

### 1. Generate Token
1. Go to: https://github.com/settings/tokens/new
2. Set **Note**: `claude-code-mcp`
3. Set **Expiration**: 90 days
4. Check scopes: `repo`, `read:org`, `read:user`
5. Click **Generate token** (green button at bottom)
6. **COPY THE TOKEN IMMEDIATELY** - it looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2. Set Environment Variable (Windows)

**Option A: PowerShell (Quick)**
```powershell
# Run PowerShell as Administrator
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'ghp_YOUR_ACTUAL_TOKEN_HERE', 'User')

# Verify it was set
[System.Environment]::GetEnvironmentVariable('GITHUB_TOKEN', 'User')
```

**Option B: GUI (Permanent)**
1. Press `Win + R` → type `sysdm.cpl` → Enter
2. **Advanced** tab → **Environment Variables** button
3. Under **User variables for sadeg**, click **New**
4. Variable name: `GITHUB_TOKEN`
5. Variable value: `ghp_YOUR_ACTUAL_TOKEN_HERE`
6. Click **OK** on all dialogs

### 3. Restart Claude Code
Close and reopen Claude Code for the environment variable to take effect.

### 4. Verify
Run `/doctor` in Claude Code - the GitHub warning should be gone.

---

## Troubleshooting

### Token Not Working
```bash
# Test token manually (PowerShell)
$env:GITHUB_TOKEN = "ghp_YOUR_TOKEN"
curl -H "Authorization: token $env:GITHUB_TOKEN" https://api.github.com/user
```

Expected response: JSON with your GitHub user info.

### MCP Server Still Warns
1. Ensure you **restarted Claude Code** after setting the environment variable
2. Verify token has correct scopes (go to https://github.com/settings/tokens)
3. Check token hasn't expired

### Permission Denied Errors
- Add the `repo` scope (not just `public_repo`)
- For private repos, ensure token has `repo` scope

---

## Security Notes

- **Never commit this token to Git** (it's in an environment variable, not in `.mcp.json`)
- If you accidentally expose it, revoke immediately at: https://github.com/settings/tokens
- Consider using a shorter expiration (30-90 days) and renewing regularly
- The token grants access to ALL your repositories with the selected scopes

---

## Token Scope Reference

| Scope | What It Allows | Needed for MCP? |
|-------|----------------|-----------------|
| `repo` | Full control of private repos | ✅ Yes (primary) |
| `public_repo` | Access public repos only | ✅ Alternative |
| `read:org` | Read org membership | ✅ Yes |
| `read:user` | Read user profile | ✅ Yes |
| `user:email` | Access email addresses | ⬜ Optional |
| `workflow` | Update GitHub Actions | ⬜ Optional |
| `gist` | Create gists | ❌ No |
| `notifications` | Access notifications | ❌ No |

---

## What the MCP Server Can Do With This Token

With `repo` + `read:org` + `read:user`:

✅ **Allowed**:
- List your repositories
- Read issues and PRs
- View commit history
- Search code in your repos
- Read repository metadata
- View branches and tags
- Read GitHub Actions workflows

❌ **NOT Allowed** (without additional scopes):
- Modify repositories (unless you add `write` scopes)
- Delete anything
- Manage organization settings
- Access billing information
- Modify GitHub Actions secrets

---

## Example: What `.mcp.json` Does

```json
"env": {
  "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
}
```

This tells the MCP server to read the `GITHUB_TOKEN` environment variable you set.

The `${}` syntax means "substitute from environment variables".
