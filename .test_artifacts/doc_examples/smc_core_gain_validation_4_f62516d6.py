# Example from: docs\reference\controllers\smc_core_gain_validation.md
# Index: 4
# Runnable: False
# Hash: f62516d6

# example-metadata:
# runnable: false

# Model uncertainty bound
Delta_max = 20.0  # N (maximum disturbance/uncertainty)

# Compute robustness margin
margin_percent = 100 * (K - Delta_max) / K

print(f"Switching gain K:      {K:.1f} N")
print(f"Uncertainty Δ_max:     {Delta_max:.1f} N")
print(f"Robustness margin:     {margin_percent:.1f}%")

if margin_percent < 20:
    print("Warning: Insufficient robustness margin (< 20%)")
    K_recommended = Delta_max / 0.8  # 20% margin
    print(f"Recommended K:         {K_recommended:.1f} N")