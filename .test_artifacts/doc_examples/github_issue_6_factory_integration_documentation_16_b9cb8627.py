# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 16
# Runnable: False
# Hash: b9cb8627

# example-metadata:
# runnable: false

def validate_smc_gains(smc_type: SMCType, gains: List[float]) -> bool:
    """
    Validate gains against mathematical constraints.

    Validation Rules by Controller Type:

    Classical SMC:
    - All surface gains λᵢ > 0 (stability requirement)
    - Switching gain K > 0 (reachability condition)
    - Damping gain kd ≥ 0 (non-negative constraint)

    Super-Twisting SMC:
    - K₁ > K₂ > 0 (finite-time convergence condition)
    - Surface gains > 0 (stability requirement)

    Adaptive SMC:
    - Surface gains > 0 (stability requirement)
    - 0.1 ≤ γ ≤ 20.0 (bounded adaptation constraint)

    Hybrid SMC:
    - All surface parameters > 0 (stability requirement)

    Args:
        smc_type: Controller type
        gains: Gain array to validate

    Returns:
        True if gains satisfy all mathematical constraints
    """