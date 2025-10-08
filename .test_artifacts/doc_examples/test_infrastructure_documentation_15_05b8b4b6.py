# Example from: docs\test_infrastructure_documentation.md
# Index: 15
# Runnable: True
# Hash: 05b8b4b6

# Check tolerance settings
assert abs(computed - expected) < 1e-10  # May be too strict
assert np.allclose(computed, expected, rtol=1e-8, atol=1e-10)  # Better