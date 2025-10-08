# Example from: docs\mathematical_foundations\boundary_layer_derivations.md
# Index: 1
# Runnable: True
# Hash: 42ef8cde

def test_boundary_layer_continuity():
    eps = 0.01
    sigma_test = np.linspace(-2*eps, 2*eps, 1000)
    sat_values = [saturate(s, eps, method="linear") for s in sigma_test]

    # Check for discontinuities
    diffs = np.diff(sat_values)
    max_jump = np.max(np.abs(diffs))
    assert max_jump < threshold  # Should be small for continuity