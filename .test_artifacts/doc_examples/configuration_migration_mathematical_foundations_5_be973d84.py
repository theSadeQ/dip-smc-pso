# Example from: docs\factory\configuration_migration_mathematical_foundations.md
# Index: 5
# Runnable: False
# Hash: be973d84

class StabilityValidator:
    """Validate stability preservation during parameter migration."""

    @staticmethod
    def validate_classical_smc_stability(gains: List[float]) -> Dict[str, Any]:
        """Validate Classical SMC stability conditions."""

        if len(gains) != 6:
            return {'valid': False, 'reason': 'Invalid gain count'}

        k1, k2, lam1, lam2, K, kd = gains

        # Check basic positivity
        if any(g <= 0 for g in gains):
            return {'valid': False, 'reason': 'All gains must be positive'}

        # Check sliding surface stability
        # For double pendulum: sliding surface eigenvalues should be negative
        surface_eigs = [-lam1/k1, -lam2/k2]

        if any(eig >= 0 for eig in surface_eigs):
            return {'valid': False, 'reason': f'Unstable surface eigenvalues: {surface_eigs}'}

        # Check actuator reasonableness
        if K > 200:  # Very high switching gain
            return {
                'valid': True,
                'warnings': [f'High switching gain K={K} may cause excessive chattering']
            }

        # Check derivative gain ratio
        kd_ratio = kd / K
        if kd_ratio > 0.5:  # Derivative gain too large relative to switching gain
            return {
                'valid': True,
                'warnings': [f'High derivative gain ratio {kd_ratio:.2f} may degrade performance']
            }

        return {
            'valid': True,
            'surface_eigenvalues': surface_eigs,
            'estimated_convergence_rate': min(abs(eig) for eig in surface_eigs),
            'switching_magnitude': K,
            'chattering_reduction': kd
        }

    @staticmethod
    def validate_adaptive_smc_convergence(gains: List[float], adaptation_params: Dict[str, float]) -> Dict[str, Any]:
        """Validate Adaptive SMC convergence conditions."""

        if len(gains) != 5:
            return {'valid': False, 'reason': 'Invalid gain count'}

        k1, k2, lam1, lam2, gamma = gains

        # Check basic conditions
        if any(g <= 0 for g in gains):
            return {'valid': False, 'reason': 'All gains must be positive'}

        # Check adaptation stability
        leak_rate = adaptation_params.get('leak_rate', 0.01)
        K_min = adaptation_params.get('K_min', 0.1)
        K_max = adaptation_params.get('K_max', 100.0)

        # Adaptation stability condition: leak rate should be small relative to adaptation rate
        stability_margin = leak_rate / gamma
        if stability_margin > 0.2:
            return {
                'valid': True,
                'warnings': [f'High leak-to-adaptation ratio {stability_margin:.3f} may slow convergence']
            }

        # Check adaptation bounds
        if K_min >= K_max:
            return {'valid': False, 'reason': 'K_min must be less than K_max'}

        gain_ratio = K_max / K_min
        if gain_ratio > 1000:  # Very wide adaptation range
            return {
                'valid': True,
                'warnings': [f'Wide adaptation range (ratio: {gain_ratio:.1f}) may cause instability']
            }

        return {
            'valid': True,
            'adaptation_rate': gamma,
            'stability_margin': stability_margin,
            'adaptation_range': [K_min, K_max],
            'estimated_settling_time': 5.0 / min(lam1/k1, lam2/k2)  # Rough estimate
        }

    @staticmethod
    def validate_sta_smc_finite_time_convergence(gains: List[float], algorithm_params: Dict[str, float]) -> Dict[str, Any]:
        """Validate Super-Twisting finite-time convergence conditions."""

        if len(gains) != 6:
            return {'valid': False, 'reason': 'Invalid gain count'}

        K1, K2, k1, k2, lam1, lam2 = gains

        # Check basic positivity
        if any(g <= 0 for g in gains):
            return {'valid': False, 'reason': 'All gains must be positive'}

        # Check super-twisting convergence conditions
        alpha = algorithm_params.get('power_exponent', 0.5)

        if not (0 < alpha < 1):
            return {'valid': False, 'reason': f'Power exponent α={alpha} must be in (0,1)'}

        # Simplified convergence check (assumes L=1)
        L_estimate = 1.0
        min_K1 = L_estimate / alpha
        min_K2 = K1**2 / (2 * L_estimate) + L_estimate

        warnings = []
        if K1 < min_K1:
            warnings.append(f'K₁={K1:.2f} may be too small for convergence (recommended: ≥{min_K1:.2f})')

        if K2 < min_K2:
            warnings.append(f'K₂={K2:.2f} may be too small for convergence (recommended: ≥{min_K2:.2f})')

        # Estimate finite-time convergence
        convergence_time = 2 * (1 / (1 - alpha)) * (1 / min(K1, K2)**0.5)

        return {
            'valid': True,
            'warnings': warnings,
            'algorithmic_gains': [K1, K2],
            'surface_gains': [k1, k2, lam1, lam2],
            'power_exponent': alpha,
            'estimated_convergence_time': convergence_time,
            'convergence_conditions_met': len(warnings) == 0
        }

# Validation example
gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
validation = StabilityValidator.validate_classical_smc_stability(gains)
print("Stability validation:", validation)