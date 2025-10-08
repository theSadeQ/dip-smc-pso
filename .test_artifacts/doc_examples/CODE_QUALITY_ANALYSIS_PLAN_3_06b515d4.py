# Example from: docs\mcp-debugging\workflows\CODE_QUALITY_ANALYSIS_PLAN.md
# Index: 3
# Runnable: True
# Hash: 06b515d4

# MCP Tool Call Pattern (after manual review of auto-fix candidates)
{
  "server": "mcp-analyzer",
  "tool": "run_ruff",
  "args": {
    "file_path": "D:\\Projects\\main\\src\\controllers\\classical_smc.py",
    "fix": true  # Apply automatic fixes
  }
}