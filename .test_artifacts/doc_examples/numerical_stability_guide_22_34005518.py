# Example from: docs\numerical_stability_guide.md
# Index: 22
# Runnable: True
# Hash: 34005518

# Include edge cases in tests
test_matrices = [
    np.diag([1.0, 1e-8, 1e-10]),  # Extreme conditioning
    np.eye(3) * 1e-15,             # Near-zero elements
    np.random.randn(3, 3) * 1e12   # Large magnitudes
]