# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 4
# Runnable: False
# Hash: 1a2bad50

# Ask Claude:
"Use numpy-mcp to calculate the condition number of the inertia matrix:
[[1.5, 0.2], [0.2, 0.8]]"

# Expected MCP tool call:
{
  "server": "numpy-mcp",
  "tool": "statistical_analysis",
  "args": {
    "matrix": [[1.5, 0.2], [0.2, 0.8]]
  }
}