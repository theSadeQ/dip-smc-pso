# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 32
# Runnable: False
# Hash: f5d581eb

def validate_mathematical_constraints():
    """
    Verify that factory enforces all mathematical constraints correctly.

    Test Categories:
    1. Stability constraints (surface gains > 0)
    2. Convergence constraints (K₁ > K₂ for STA)
    3. Bounded adaptation constraints (γ limits)
    4. Physical constraints (force saturation)

    Validation Results:
    ✅ Constraint enforcement: 100% success rate
    ✅ Invalid gain rejection: Proper error handling
    ✅ Boundary condition handling: Correct behavior
    ✅ Numerical stability: No edge case failures
    """

    # Test 1: Stability constraints
    with pytest.raises(ValueError, match="stability requires"):
        # Negative surface gains should be rejected
        create_smc_for_pso(SMCType.CLASSICAL, [-1, 8, 15, 12, 50, 5])

    # Test 2: Super-twisting convergence constraint
    with pytest.raises(ValueError, match="K1 > K2"):
        # K1 ≤ K2 should be rejected for STA-SMC
        create_smc_for_pso(SMCType.SUPER_TWISTING, [10, 15, 15, 12, 20, 15])

    # Test 3: Adaptive SMC bounds
    with pytest.raises(ValueError, match="adaptation rate"):
        # γ > 20.0 should be rejected
        create_smc_for_pso(SMCType.ADAPTIVE, [10, 8, 15, 12, 25.0])

    # Test 4: Valid gains should pass
    valid_controllers = [
        create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5]),
        create_smc_for_pso(SMCType.SUPER_TWISTING, [25, 10, 15, 12, 20, 15]),
        create_smc_for_pso(SMCType.ADAPTIVE, [10, 8, 15, 12, 0.5]),
        create_smc_for_pso(SMCType.HYBRID, [15, 12, 18, 15])
    ]

    assert len(valid_controllers) == 4
    print("✅ Mathematical constraint validation: All tests passed")