# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 2
# Runnable: False
# Hash: 6007ce0f

# example-metadata:
# runnable: false

# Ask Claude:
"Use mcp-analyzer to find dead code in src/utils/validation/"

# Expected MCP tool call:
{
  "server": "mcp-analyzer",
  "tool": "run_vulture",
  "args": {
    "directory": "D:\\Projects\\main\\src\\utils\\validation",
    "min_confidence": 80
  }
}