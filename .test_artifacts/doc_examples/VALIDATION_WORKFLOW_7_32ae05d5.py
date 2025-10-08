# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 7
# Runnable: False
# Hash: 32ae05d5

# example-metadata:
# runnable: false

# Ask Claude:
"Use pandas-mcp to calculate average fitness by controller type from the PSO results"

# Expected MCP tool call:
{
  "server": "pandas-mcp",
  "tool": "run_pandas_code",
  "args": {
    "code": "import pandas as pd\ndf = pd.DataFrame(pso_data)\nresult = df.groupby('controller_type')['best_fitness'].agg(['mean', 'std', 'min', 'max'])"
  }
}