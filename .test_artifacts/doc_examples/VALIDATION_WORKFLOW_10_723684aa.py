# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 10
# Runnable: False
# Hash: 723684aa

# Ask Claude:
"Use mcp-analyzer to lint the failing test file tests/test_controllers/test_classical_smc.py"

# Expected MCP tool call:
{
  "server": "mcp-analyzer",
  "tool": "run_ruff",
  "args": {
    "file_path": "D:\\Projects\\main\\tests\\test_controllers\\test_classical_smc.py",
    "fix": false
  }
}