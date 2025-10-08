# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 6
# Runnable: False
# Hash: 87ec6c04

# Ask Claude:
"Use numpy-mcp to analyze these PSO fitness values:
[150.2, 145.8, 142.1, 140.5, 139.8, 139.3, 139.1, 139.0]"

# Expected MCP tool call:
{
  "server": "numpy-mcp",
  "tool": "statistical_analysis",
  "args": {
    "data": [150.2, 145.8, 142.1, 140.5, 139.8, 139.3, 139.1, 139.0]
  }
}