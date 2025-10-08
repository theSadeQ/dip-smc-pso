# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 1
# Runnable: False
# Hash: 4fe27ffc

# example-metadata:
# runnable: false

# Ask Claude via MCP:
"Use mcp-analyzer to run RUFF linting on src/controllers/classical_smc.py"

# Expected MCP tool call:
{
  "server": "mcp-analyzer",
  "tool": "run_ruff",
  "args": {
    "file_path": "D:\\Projects\\main\\src\\controllers\\classical_smc.py",
    "fix": false
  }
}