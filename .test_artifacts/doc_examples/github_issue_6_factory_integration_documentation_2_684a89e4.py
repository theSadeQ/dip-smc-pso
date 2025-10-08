# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 2
# Runnable: True
# Hash: 684a89e4

def validate_smc_gains(smc_type: SMCType, gains: List[float]) -> bool:
    """
    Validate SMC gains based on control theory constraints.

    Mathematical Constraints:
    - Classical SMC: All surface gains λᵢ > 0 for stability
    - Super-Twisting: K₁ > K₂ > 0 for finite-time convergence
    - Adaptive SMC: 0.1 ≤ γ ≤ 20.0 for bounded adaptation
    - Hybrid SMC: Surface parameters > 0 for stability
    """