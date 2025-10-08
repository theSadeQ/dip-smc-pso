# Example from: docs\numerical_stability_guide.md
# Index: 17
# Runnable: True
# Hash: ddc3bc07

# Check if adaptive mode is enabled
print(regularizer.use_fixed)  # Should be False

# Check condition number
cond_num = np.linalg.cond(M)
print(f"Condition number: {cond_num:.2e}")