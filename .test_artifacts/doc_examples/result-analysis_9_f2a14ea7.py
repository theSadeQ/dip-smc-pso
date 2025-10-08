# Example from: docs\guides\how-to\result-analysis.md
# Index: 9
# Runnable: False
# Hash: f2a14ea7

# example-metadata:
# runnable: false

# 95% Confidence Interval for mean ISE
confidence_level = 0.95
alpha = 1 - confidence_level

# Classical SMC
ci_classical = stats.t.interval(
    confidence_level,
    len(ise_classical_trials) - 1,
    loc=np.mean(ise_classical_trials),
    scale=stats.sem(ise_classical_trials)
)

# STA-SMC
ci_sta = stats.t.interval(
    confidence_level,
    len(ise_sta_trials) - 1,
    loc=np.mean(ise_sta_trials),
    scale=stats.sem(ise_sta_trials)
)

print(f"\n95% Confidence Intervals:")
print(f"  Classical SMC: [{ci_classical[0]:.4f}, {ci_classical[1]:.4f}]")
print(f"  STA-SMC:       [{ci_sta[0]:.4f}, {ci_sta[1]:.4f}]")