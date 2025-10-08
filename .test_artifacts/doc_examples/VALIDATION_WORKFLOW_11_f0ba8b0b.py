# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 11
# Runnable: False
# Hash: f0ba8b0b

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