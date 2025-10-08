# Example from: docs\numerical_stability_guide.md
# Index: 14
# Runnable: True
# Hash: 94ac3e26

# From test_matrix_regularization()
extreme_ratios = [1e-8, 2e-9, 5e-9, 1e-10]
for ratio in extreme_ratios:
    # All ratios handled without LinAlgError
    assert linalg_errors == 0