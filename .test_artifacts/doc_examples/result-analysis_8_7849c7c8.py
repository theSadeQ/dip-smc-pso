# Example from: docs\guides\how-to\result-analysis.md
# Index: 8
# Runnable: False
# Hash: 7849c7c8

# example-metadata:
# runnable: false

# Compute Cohen's d (effect size)
mean_diff = np.mean(ise_classical_trials) - np.mean(ise_sta_trials)
pooled_std = np.sqrt(
    (np.std(ise_classical_trials)**2 + np.std(ise_sta_trials)**2) / 2
)
cohens_d = mean_diff / pooled_std

print(f"\nEffect Size (Cohen's d): {cohens_d:.4f}")
print(f"  Interpretation: ", end="")
if abs(cohens_d) < 0.2:
    print("Small effect")
elif abs(cohens_d) < 0.5:
    print("Medium effect")
else:
    print("Large effect")