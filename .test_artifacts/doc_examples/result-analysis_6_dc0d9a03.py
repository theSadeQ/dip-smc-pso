# Example from: docs\guides\how-to\result-analysis.md
# Index: 6
# Runnable: False
# Hash: dc0d9a03

# Load multiple trials
n_trials = 50
ise_classical_trials = []
ise_sta_trials = []

for i in range(n_trials):
    with open(f'results_classical_trial_{i}.json') as f:
        ise_classical_trials.append(json.load(f)['metrics']['ise'])

    with open(f'results_sta_trial_{i}.json') as f:
        ise_sta_trials.append(json.load(f)['metrics']['ise'])

# Convert to arrays
ise_classical_trials = np.array(ise_classical_trials)
ise_sta_trials = np.array(ise_sta_trials)

# Compute summary statistics
print("Classical SMC:")
print(f"  Mean ISE: {np.mean(ise_classical_trials):.4f}")
print(f"  Std ISE:  {np.std(ise_classical_trials):.4f}")
print(f"  Min ISE:  {np.min(ise_classical_trials):.4f}")
print(f"  Max ISE:  {np.max(ise_classical_trials):.4f}")

print("\nSTA-SMC:")
print(f"  Mean ISE: {np.mean(ise_sta_trials):.4f}")
print(f"  Std ISE:  {np.std(ise_sta_trials):.4f}")
print(f"  Min ISE:  {np.min(ise_sta_trials):.4f}")
print(f"  Max ISE:  {np.max(ise_sta_trials):.4f}")