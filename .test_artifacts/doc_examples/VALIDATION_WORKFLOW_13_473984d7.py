# Example from: docs\mcp-debugging\workflows\VALIDATION_WORKFLOW.md
# Index: 13
# Runnable: True
# Hash: 473984d7

run_pandas_code({
  code: "df = pd.DataFrame(pso_data); result = df['gbest_fitness'].diff().mean()"
})
# Output: Average improvement per iteration: 0.0012 (very slow!)