# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 8
# Runnable: False
# Hash: 3cb3db9b

# Instead of batch_size=10000
batch_size = 1000
n_chunks = 10

all_results = []
for chunk in range(n_chunks):
    chunk_results = simulate(initial_states[chunk*batch_size:(chunk+1)*batch_size], ...)
    all_results.append(chunk_results)

results = np.concatenate(all_results, axis=0)