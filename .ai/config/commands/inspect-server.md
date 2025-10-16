---
description: Launch MCP Inspector for server testing and debugging
tags: [mcp, inspector, testing]
---

# MCP Inspector Launcher

I'll help you launch the MCP Inspector to test and debug MCP servers.

## MCP Inspector Commands

### Basic Launch
```bash
npx @modelcontextprotocol/inspector
```
This opens the Inspector UI at http://localhost:6274

### Test Specific Server

**Filesystem Server**:
```bash
npx @modelcontextprotocol/inspector node "C:\Users\<USER>\AppData\Roaming\npm\node_modules\@modelcontextprotocol\server-filesystem\dist\index.js" "C:\path\to\allowed\directory"
```

**GitHub Server**:
```bash
set GITHUB_TOKEN=your_token && npx @modelcontextprotocol/inspector node "C:\Users\<USER>\AppData\Roaming\npm\node_modules\@modelcontextprotocol\server-github\dist\index.js"
```

**PostgreSQL Server**:
```bash
set POSTGRES_CONNECTION_STRING=postgresql://user:pass@localhost:5432/db && npx @modelcontextprotocol/inspector node "C:\Users\<USER>\AppData\Roaming\npm\node_modules\enhanced-postgres-mcp-server\dist\index.js"
```

**Puppeteer Server**:
```bash
npx @modelcontextprotocol/inspector node "C:\Users\<USER>\AppData\Roaming\npm\node_modules\@modelcontextprotocol\server-puppeteer\dist\index.js"
```

## Which server would you like to test?

Or would you like me to help troubleshoot a server that's not working?
