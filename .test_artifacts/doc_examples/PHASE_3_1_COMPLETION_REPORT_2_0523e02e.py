# Example from: docs\visualization\PHASE_3_1_COMPLETION_REPORT.md
# Index: 2
# Runnable: False
# Hash: 0523e02e

# 1. Parse log → list of dictionaries
data_rows = [{'iteration': i, 'cost': c, 'timestamp': ts}, ...]

# 2. Create DataFrame
df = pd.DataFrame(data_rows)

# 3. Sort and calculate derived metrics
df = df.sort_values('iteration').reset_index(drop=True)
df['improvement'] = df['cost'].shift(1) - df['cost']

# 4. Compute convergence thresholds
target_90 = initial_cost - 0.90 * (initial_cost - best_cost)
iters_90 = df[df['cost'] <= target_90]['iteration'].min()