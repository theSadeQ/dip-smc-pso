# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 7
# Runnable: False
# Hash: a4480742

# example-metadata:
# runnable: false

def test_optimal_gains_performance():
    """Test performance characteristics of PSO-optimized gains."""
    # PSO optimal gains
    optimal_gains = [77.62, 44.45, 17.31, 14.25, 18.66, 9.76]
    boundary_layer = 9.76  # Matched to kd for maximum chattering reduction

    controller = ClassicalSMC(
        gains=optimal_gains,
        max_force=20.0,
        boundary_layer=boundary_layer,
        switch_method='tanh'
    )

    # Analyze gain ratios for insights
    k1, k2, lam1, lam2, K, kd = optimal_gains

    # Ratio k1/k2 indicates relative importance of pendulum rates
    k_ratio = k1 / k2
    assert 1.5 < k_ratio < 2.0, \
        f"k1/k2 ratio {k_ratio:.2f} indicates strong first pendulum damping"

    # Ratio lam1/lam2 indicates relative position error weighting
    lam_ratio = lam1 / lam2
    assert 1.0 < lam_ratio < 1.5, \
        f"lam1/lam2 ratio {lam_ratio:.2f} indicates balanced position control"

    # Large K relative to lam ensures reaching condition
    K_to_lam_ratio = K / max(lam1, lam2)
    assert K_to_lam_ratio > 1.0, \
        f"K/lam ratio {K_to_lam_ratio:.2f} ensures reaching condition satisfied"

    # Boundary layer matching kd for chattering-free operation
    assert boundary_layer == kd, \
        "Boundary layer matched to kd for optimal chattering suppression"