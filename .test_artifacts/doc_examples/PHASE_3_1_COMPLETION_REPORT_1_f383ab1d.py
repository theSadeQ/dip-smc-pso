# Example from: docs\visualization\PHASE_3_1_COMPLETION_REPORT.md
# Index: 1
# Runnable: True
# Hash: f383ab1d

ITERATION_PATTERN = r'(\d+)/(\d+),\s*best_cost=([\d.e+\-]+)(?:\s|$)'
FINAL_COST_PATTERN = r'Optimization finished.*best cost:\s*([\d.]+),\s*best pos:\s*\[([\d.,\s]+)\]'
TOTAL_TIME_PATTERN = r'Optimization completed in\s*([\d.]+)s'