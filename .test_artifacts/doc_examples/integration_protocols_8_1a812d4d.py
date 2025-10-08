# Example from: docs\technical\integration_protocols.md
# Index: 8
# Runnable: False
# Hash: 1a812d4d

class HILIntegrationProtocol:
    """Hardware-in-the-loop integration protocol."""

    def __init__(self, controller_factory, communication_config: dict):
        self.factory = controller_factory
        self.comm_config = communication_config
        self.safety_limits = self._get_safety_limits()

    def create_hil_controller(
        self,
        controller_type: str,
        gains: List[float],
        safety_config: dict
    ) -> 'HILController':
        """Create HIL-compatible controller with safety features."""

        # Create base controller
        base_controller = create_controller(controller_type, gains=gains)

        # Wrap with HIL safety layer
        hil_controller = HILSafetyWrapper(
            base_controller,
            safety_config,
            self.safety_limits
        )

        return hil_controller

    def _get_safety_limits(self) -> dict:
        """Get hardware safety limits."""
        return {
            'max_force': 50.0,  # Reduced for hardware safety
            'max_angle': np.pi / 6,  # 30 degrees maximum
            'max_velocity': 10.0,  # rad/s
            'emergency_stop_conditions': [
                'angle_limit_exceeded',
                'velocity_limit_exceeded',
                'communication_failure'
            ]
        }

class HILSafetyWrapper:
    """Safety wrapper for HIL controllers."""

    def __init__(self, controller, safety_config: dict, limits: dict):
        self.controller = controller
        self.safety_config = safety_config
        self.limits = limits
        self.emergency_stop = False

    def compute_control(self, state: np.ndarray, *args, **kwargs) -> float:
        """Compute control with safety checks."""

        # Pre-control safety checks
        if self._check_emergency_conditions(state):
            self.emergency_stop = True
            return 0.0  # Emergency stop

        if self.emergency_stop:
            return 0.0  # Maintain emergency stop

        # Compute control
        try:
            control_result = self.controller.compute_control(state, *args, **kwargs)
            u = control_result.u if hasattr(control_result, 'u') else control_result

            # Post-control safety checks
            u_safe = self._apply_safety_limits(u, state)

            return u_safe

        except Exception as e:
            logger.error(f"HIL control computation failed: {e}")
            self.emergency_stop = True
            return 0.0

    def _check_emergency_conditions(self, state: np.ndarray) -> bool:
        """Check for emergency stop conditions."""
        theta1, theta2, x, dtheta1, dtheta2, dx = state

        # Angle limits
        if abs(theta1) > self.limits['max_angle']:
            logger.warning("Pendulum 1 angle limit exceeded")
            return True

        if abs(theta2) > self.limits['max_angle']:
            logger.warning("Pendulum 2 angle limit exceeded")
            return True

        # Velocity limits
        if abs(dtheta1) > self.limits['max_velocity']:
            logger.warning("Pendulum 1 velocity limit exceeded")
            return True

        if abs(dtheta2) > self.limits['max_velocity']:
            logger.warning("Pendulum 2 velocity limit exceeded")
            return True

        return False

    def _apply_safety_limits(self, control: float, state: np.ndarray) -> float:
        """Apply safety limits to control signal."""
        # Force magnitude limit
        u_limited = np.clip(control, -self.limits['max_force'], self.limits['max_force'])

        # Rate limiting (if previous control available)
        if hasattr(self, '_last_control'):
            max_rate = self.safety_config.get('max_control_rate', 100.0)  # N/s
            dt = self.safety_config.get('dt', 0.001)
            max_change = max_rate * dt

            control_change = u_limited - self._last_control
            if abs(control_change) > max_change:
                u_limited = self._last_control + np.sign(control_change) * max_change

        self._last_control = u_limited
        return u_limited