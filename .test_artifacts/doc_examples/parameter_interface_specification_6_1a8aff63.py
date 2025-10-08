# Example from: docs\factory\parameter_interface_specification.md
# Index: 6
# Runnable: False
# Hash: 1a8aff63

# example-metadata:
# runnable: false

class ParameterValidator:
    """Comprehensive parameter validation for SMC controllers."""

    @staticmethod
    def validate_gain_structure(
        gains: List[float],
        controller_type: str,
        controller_info: Dict[str, Any]
    ) -> None:
        """Validate gain array structure and constraints."""

        # 1. Length validation
        expected_count = controller_info['gain_count']
        if len(gains) != expected_count:
            raise ValueError(
                f"Controller '{controller_type}' requires {expected_count} gains, "
                f"got {len(gains)}. Expected structure: {controller_info.get('gain_names', [])}"
            )

        # 2. Numerical validation
        for i, gain in enumerate(gains):
            if not isinstance(gain, (int, float)):
                raise TypeError(f"Gain[{i}] must be numeric, got {type(gain)}")

            if not np.isfinite(gain):
                raise ValueError(f"Gain[{i}] must be finite, got {gain}")

        # 3. Physical constraint validation
        ParameterValidator._validate_physical_constraints(gains, controller_type)

    @staticmethod
    def _validate_physical_constraints(gains: List[float], controller_type: str) -> None:
        """Validate controller-specific physical constraints."""

        if controller_type == 'classical_smc':
            # All gains must be positive for stability
            if any(g <= 0 for g in gains):
                raise ValueError("Classical SMC: All gains must be positive for stability")

            # Specific constraint: K (switching gain) should be significant
            K = gains[4]  # K is 5th element
            if K < 1.0:
                warnings.warn(f"Classical SMC: K={K} may be too small for effective switching")

        elif controller_type == 'adaptive_smc':
            # Surface gains must be positive
            if any(g <= 0 for g in gains[:4]):
                raise ValueError("Adaptive SMC: Surface gains k1, k2, λ1, λ2 must be positive")

            # Gamma (adaptation rate) constraints
            gamma = gains[4]
            if gamma <= 0:
                raise ValueError("Adaptive SMC: Adaptation rate γ must be positive")
            if gamma > 10.0:
                warnings.warn(f"Adaptive SMC: γ={gamma} may cause adaptation instability")

        elif controller_type == 'sta_smc':
            # All gains positive for STA stability
            if any(g <= 0 for g in gains):
                raise ValueError("STA-SMC: All gains must be positive")

            # STA-specific constraint: K1 > K2 typically
            K1, K2 = gains[0], gains[1]
            if K1 <= K2:
                warnings.warn("STA-SMC: Typically K1 > K2 for proper STA operation")

        elif controller_type == 'hybrid_adaptive_sta_smc':
            # Only surface gains for hybrid controller
            if any(g <= 0 for g in gains):
                raise ValueError("Hybrid SMC: All surface gains must be positive")