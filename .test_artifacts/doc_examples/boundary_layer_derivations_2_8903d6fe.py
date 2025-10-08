# Example from: docs\mathematical_foundations\boundary_layer_derivations.md
# Index: 2
# Runnable: True
# Hash: 8903d6fe

def test_boundary_conditions():
    eps = 0.01

    # At boundary points
    assert abs(saturate(eps, eps, "linear") - 1.0) < 1e-10
    assert abs(saturate(-eps, eps, "linear") + 1.0) < 1e-10

    # Inside boundary layer (linear region)
    sigma_inside = 0.5 * eps
    expected = sigma_inside / eps
    assert abs(saturate(sigma_inside, eps, "linear") - expected) < 1e-10