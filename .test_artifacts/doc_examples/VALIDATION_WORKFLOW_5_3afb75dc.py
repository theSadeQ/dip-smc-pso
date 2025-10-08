# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 5
# Runnable: False
# Hash: 3afb75dc

# Ask Claude:
"Use numpy-mcp to compute eigenvalues of system matrix A:
[[0, 1], [-2, -3]]"

# Expected MCP tool call:
{
  "server": "numpy-mcp",
  "tool": "eigen_decomposition",
  "args": {
    "matrix": [[0, 1], [-2, -3]]
  }
}