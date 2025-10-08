# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 5
# Runnable: False
# Hash: e6233974

def verify_lyapunov_stability(controller_type: SMCType,
                             gains: List[float]) -> bool:
    """
    Verify Lyapunov stability conditions for SMC controller.

    Uses candidate Lyapunov function V = (1/2)s² and verifies:
    V̇ ≤ -η|s| for some η > 0
    """
    if controller_type == SMCType.CLASSICAL:
        # Classical SMC: V̇ = s(-K·sign(s) + δ) ≤ -η|s|
        K = gains[4]  # Switching gain
        return K > estimate_uncertainty_bound(gains)

    elif controller_type == SMCType.SUPER_TWISTING:
        # STA: Verify K₁ > K₂ and sufficient gain margins
        K1, K2 = gains[0], gains[1]
        return K1 > K2 and K1 > estimate_lipschitz_constant()