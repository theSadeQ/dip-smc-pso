# Example from: docs\factory\pso_factory_api_reference.md
# Index: 12
# Runnable: False
# Hash: 478f800d

def validate_mathematical_constraints(smc_type: SMCType,
                                    gains: List[float],
                                    tolerance: float = 1e-8
                                    ) -> Tuple[bool, List[str]]:
    """
    Validate mathematical constraints for SMC gains.

    Args:
        smc_type: Controller type
        gains: Gain values to validate
        tolerance: Numerical tolerance for constraint checking

    Returns:
        Tuple of (is_valid, list_of_constraint_violations)
    """
    violations = []

    if smc_type == SMCType.CLASSICAL:
        k1, k2, lam1, lam2, K, kd = gains

        if k1 <= tolerance:
            violations.append(f"k1 = {k1:.6f} must be > {tolerance}")
        if k2 <= tolerance:
            violations.append(f"k2 = {k2:.6f} must be > {tolerance}")
        if lam1 <= tolerance:
            violations.append(f"λ1 = {lam1:.6f} must be > {tolerance}")
        if lam2 <= tolerance:
            violations.append(f"λ2 = {lam2:.6f} must be > {tolerance}")
        if K <= tolerance:
            violations.append(f"K = {K:.6f} must be > {tolerance}")
        if kd < -tolerance:
            violations.append(f"kd = {kd:.6f} must be ≥ 0")

    elif smc_type == SMCType.SUPER_TWISTING:
        K1, K2, lam1, lam2, alpha1, alpha2 = gains

        if K1 <= K2 + tolerance:
            violations.append(f"K1 = {K1:.6f} must be > K2 = {K2:.6f}")
        if K2 <= tolerance:
            violations.append(f"K2 = {K2:.6f} must be > {tolerance}")
        if any(g <= tolerance for g in [lam1, lam2, alpha1, alpha2]):
            violations.append("All surface parameters must be positive")

    elif smc_type == SMCType.ADAPTIVE:
        k1, k2, lam1, lam2, gamma = gains

        if any(g <= tolerance for g in [k1, k2, lam1, lam2]):
            violations.append("All surface gains must be positive")
        if not (0.1 <= gamma <= 20.0):
            violations.append(f"γ = {gamma:.6f} must be in [0.1, 20.0]")

    elif smc_type == SMCType.HYBRID:
        if any(g <= tolerance for g in gains):
            violations.append("All hybrid gains must be positive")

    return len(violations) == 0, violations

def estimate_stability_properties(smc_type: SMCType,
                                gains: List[float]
                                ) -> Dict[str, float]:
    """
    Estimate stability properties from gains.

    Returns:
        Dictionary with estimated properties:
            - convergence_rate: Estimated convergence rate
            - stability_margin: Stability margin estimate
            - bandwidth: Estimated closed-loop bandwidth
            - settling_time: Estimated settling time
    """
    if smc_type == SMCType.CLASSICAL:
        k1, k2, lam1, lam2, K, kd = gains

        min_surface_gain = min(lam1, lam2)
        convergence_rate = min_surface_gain
        bandwidth = min_surface_gain
        settling_time = 4.0 / min_surface_gain if min_surface_gain > 0 else float('inf')
        stability_margin = K / (K + 10.0)  # Rough estimate

    elif smc_type == SMCType.SUPER_TWISTING:
        K1, K2, lam1, lam2, alpha1, alpha2 = gains

        convergence_rate = min(K1, K2)
        bandwidth = min(lam1, lam2)
        settling_time = 2.0 / convergence_rate if convergence_rate > 0 else float('inf')
        stability_margin = (K1 - K2) / K1 if K1 > 0 else 0

    elif smc_type == SMCType.ADAPTIVE:
        k1, k2, lam1, lam2, gamma = gains

        surface_bandwidth = min(lam1, lam2)
        adaptation_bandwidth = gamma
        convergence_rate = min(surface_bandwidth, adaptation_bandwidth)
        bandwidth = surface_bandwidth
        settling_time = 4.0 / convergence_rate if convergence_rate > 0 else float('inf')
        stability_margin = min(1.0, (20.0 - gamma) / 20.0)

    elif smc_type == SMCType.HYBRID:
        k1, k2, lam1, lam2 = gains

        convergence_rate = min(gains)
        bandwidth = convergence_rate
        settling_time = 4.0 / convergence_rate if convergence_rate > 0 else float('inf')
        stability_margin = min(gains) / max(gains) if max(gains) > 0 else 0

    return {
        'convergence_rate': convergence_rate,
        'stability_margin': stability_margin,
        'bandwidth': bandwidth,
        'settling_time': settling_time
    }