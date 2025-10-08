# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 3
# Runnable: False
# Hash: ce0ee108

# example-metadata:
# runnable: false

# Ask Claude:
"Use mcp-analyzer to auto-fix RUFF issues in classical_smc.py"

# Expected MCP tool call:
{
  "server": "mcp-analyzer",
  "tool": "run_ruff",
  "args": {
    "file_path": "D:\\Projects\\main\\src\\controllers\\classical_smc.py",
    "fix": true
  }
}