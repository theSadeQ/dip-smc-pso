# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 9
# Runnable: False
# Hash: 8ba14e0a

# Ask Claude:
"Use pytest-mcp to list the last 5 test failures"

# Expected MCP tool call:
{
  "server": "pytest-mcp",
  "tool": "list_failures",
  "args": {
    "last": 5
  }
}