# Example from: docs\architecture\controller_system_architecture.md
# Index: 17
# Runnable: False
# Hash: 8aaf9d88

# example-metadata:
# runnable: false

class SafetyManager:
    """Comprehensive safety management for control systems."""

    def __init__(self, safety_config: Dict[str, Any]):
        self.safety_limits = safety_config['limits']
        self.emergency_procedures = safety_config['emergency_procedures']

    def validate_control_safety(
        self,
        control_action: float,
        system_state: np.ndarray,
        controller_type: str
    ) -> SafetyValidationResult:
        """Validate control action against safety constraints."""

        safety_violations = []

        # Check control force limits
        if abs(control_action) > self.safety_limits['max_force']:
            safety_violations.append(
                SafetyViolation(
                    type='control_force_limit',
                    severity='critical',
                    value=control_action,
                    limit=self.safety_limits['max_force']
                )
            )

        # Check system state limits
        angles = system_state[:2]  # θ₁, θ₂
        if np.any(np.abs(angles) > self.safety_limits['max_angle']):
            safety_violations.append(
                SafetyViolation(
                    type='angle_limit',
                    severity='warning',
                    value=angles,
                    limit=self.safety_limits['max_angle']
                )
            )

        # Determine safety status
        if any(v.severity == 'critical' for v in safety_violations):
            safety_status = 'unsafe'
            recommended_action = 'emergency_stop'
        elif safety_violations:
            safety_status = 'warning'
            recommended_action = 'apply_safety_filter'
        else:
            safety_status = 'safe'
            recommended_action = 'proceed'

        return SafetyValidationResult(
            status=safety_status,
            violations=safety_violations,
            recommended_action=recommended_action
        )

    def apply_safety_filter(
        self,
        control_action: float,
        system_state: np.ndarray
    ) -> float:
        """Apply safety filter to control action."""

        # Clamp control force to safe limits
        safe_control = np.clip(
            control_action,
            -self.safety_limits['max_force'],
            self.safety_limits['max_force']
        )

        # Additional state-dependent safety modifications
        angles = system_state[:2]
        if np.any(np.abs(angles) > self.safety_limits['warning_angle']):
            # Reduce control authority near angle limits
            safety_factor = 0.7
            safe_control *= safety_factor

        return safe_control