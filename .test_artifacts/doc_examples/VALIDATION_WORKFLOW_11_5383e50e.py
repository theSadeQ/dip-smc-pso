# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 11
# Runnable: False
# Hash: 5383e50e

# example-metadata:
# runnable: false

# Ask Claude:
"Use pytest-mcp to analyze failure patterns grouped by test name"

# Expected MCP tool call:
{
  "server": "pytest-mcp",
  "tool": "get_patterns",
  "args": {
    "groupby": "test_name"
  }
}