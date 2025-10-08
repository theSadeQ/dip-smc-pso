# Example from: docs\numerical_stability_guide.md
# Index: 18
# Runnable: True
# Hash: b89fc58f

# Check if over-regularization is occurring
sv_ratio = s[-1] / s[0]
print(f"SV ratio: {sv_ratio:.2e}")