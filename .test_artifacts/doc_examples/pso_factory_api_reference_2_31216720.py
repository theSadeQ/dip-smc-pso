# Example from: docs\factory\pso_factory_api_reference.md
# Index: 2
# Runnable: False
# Hash: 31216720

class SMCType(Enum):
    """
    Enumeration of supported SMC controller types for PSO optimization.

    Each type corresponds to a specific sliding mode control algorithm
    with distinct mathematical properties and parameter requirements.
    """

    CLASSICAL = "classical_smc"
    """
    Classical sliding mode controller with boundary layer.

    Mathematical Model:
        u = u_eq + u_sw
        u_eq = (GB)^(-1)[-Gf(x) + ṡ_ref]
        u_sw = -K·tanh(s/φ)

    Gain Parameters: [k1, k2, λ1, λ2, K, kd]
        k1, k2: Position gains for pendulum 1 and 2
        λ1, λ2: Surface gains for pendulum 1 and 2
        K: Switching gain
        kd: Damping gain

    Mathematical Constraints:
        - λ1, λ2, K > 0 (stability requirement)
        - kd ≥ 0 (non-negative damping)

    PSO Bounds: [(0.1,50), (0.1,50), (1,50), (1,50), (1,200), (0,50)]
    """

    SUPER_TWISTING = "sta_smc"
    """
    Super-twisting sliding mode controller (second-order).

    Mathematical Model:
        u̇ = -K1·sign(s) - K2·sign(ṡ)
        s = σ(x)  (sliding surface)

    Gain Parameters: [K1, K2, λ1, λ2, α1, α2]
        K1: Primary twisting gain
        K2: Secondary twisting gain
        λ1, λ2: Surface gains
        α1, α2: Higher-order surface parameters

    Mathematical Constraints:
        - K1 > K2 > 0 (finite-time convergence)
        - λ1, λ2, α1, α2 > 0 (stability)

    PSO Bounds: [(2,100), (1,99), (1,50), (1,50), (1,50), (1,50)]
    """

    ADAPTIVE = "adaptive_smc"
    """
    Adaptive sliding mode controller with online gain tuning.

    Mathematical Model:
        u = u_eq + u_sw
        K̇ = γ|s| - σK  (adaptation law)

    Gain Parameters: [k1, k2, λ1, λ2, γ]
        k1, k2: Position gains
        λ1, λ2: Surface gains
        γ: Adaptation rate

    Mathematical Constraints:
        - k1, k2, λ1, λ2 > 0 (stability)
        - 0.1 ≤ γ ≤ 20.0 (bounded adaptation)

    PSO Bounds: [(0.1,50), (0.1,50), (1,50), (1,50), (0.1,20)]
    """

    HYBRID = "hybrid_adaptive_sta_smc"
    """
    Hybrid adaptive super-twisting controller.

    Mathematical Model:
        u = u_adaptive + u_sta  (mode switching)

    Gain Parameters: [k1, k2, λ1, λ2]
        k1, k2: Surface gains for pendulum 1 and 2
        λ1, λ2: Higher-order surface gains

    Mathematical Constraints:
        - All parameters > 0 (stability)

    PSO Bounds: [(1,50), (1,50), (1,50), (1,50)]
    """

    @property
    def gain_count(self) -> int:
        """Return number of gain parameters for this controller type."""
        return {
            SMCType.CLASSICAL: 6,
            SMCType.SUPER_TWISTING: 6,
            SMCType.ADAPTIVE: 5,
            SMCType.HYBRID: 4
        }[self]

    @property
    def mathematical_constraints(self) -> Dict[str, str]:
        """Return mathematical constraints as human-readable strings."""
        return {
            SMCType.CLASSICAL: "λ1,λ2,K > 0; kd ≥ 0",
            SMCType.SUPER_TWISTING: "K1 > K2 > 0; λ1,λ2,α1,α2 > 0",
            SMCType.ADAPTIVE: "k1,k2,λ1,λ2 > 0; 0.1 ≤ γ ≤ 20.0",
            SMCType.HYBRID: "k1,k2,λ1,λ2 > 0"
        }[self]