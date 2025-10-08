# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 8
# Runnable: False
# Hash: dca504b8

# example-metadata:
# runnable: false

# Ask Claude:
"Use pandas-mcp to create a bar chart comparing average fitness by controller type"

# Expected MCP tool call:
{
  "server": "pandas-mcp",
  "tool": "generate_chartjs",
  "args": {
    "data": {
      "columns": [
        {"name": "Controller", "type": "string", "examples": ["classical_smc", "adaptive_smc", "hybrid_adaptive", "sta_smc"]},
        {"name": "Average Fitness", "type": "number", "examples": [142.3, 138.7, 136.2, 140.5]}
      ]
    },
    "chart_types": ["bar"],
    "title": "PSO Performance by Controller Type"
  }
}