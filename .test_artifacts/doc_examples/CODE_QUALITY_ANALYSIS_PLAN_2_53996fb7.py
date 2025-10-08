# Example from: docs\mcp-debugging\workflows\CODE_QUALITY_ANALYSIS_PLAN.md
# Index: 2
# Runnable: True
# Hash: 53996fb7

# MCP Tool Call Pattern
{
  "server": "mcp-analyzer",
  "tool": "run_vulture",
  "args": {
    "directory": "D:\\Projects\\main\\src\\controllers",
    "min_confidence": 80  # Only high-confidence findings
  }
}