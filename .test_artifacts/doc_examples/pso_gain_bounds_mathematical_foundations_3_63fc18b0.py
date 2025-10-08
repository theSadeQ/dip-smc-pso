# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 3
# Runnable: False
# Hash: 63fc18b0

# example-metadata:
# runnable: false

class SafetyBoundsEnforcer:
    """
    Hardware and safety constraint enforcement for PSO optimization.
    """

    def __init__(self):
        self.max_force = 150.0  # Hardware actuator limit
        self.max_angle = np.pi/4  # Safe angular range
        self.max_angular_velocity = 10.0  # rad/s

    def enforce_safety_bounds(self, gains: np.ndarray, controller_type: str) -> np.ndarray:
        """
        Enforce safety-critical bounds with hardware protection.
        """
        safe_gains = gains.copy()

        # Controller-specific safety enforcement
        if controller_type in ["classical_smc", "sta_smc"]:
            # Limit total switching gain to prevent actuator damage
            if controller_type == "classical_smc":
                K, kd = gains[4], gains[5]
                if K + kd > self.max_force:
                    scale_factor = self.max_force / (K + kd)
                    safe_gains[4] *= scale_factor
                    safe_gains[5] *= scale_factor

            elif controller_type == "sta_smc":
                K1, K2 = gains[0], gains[1]
                if K1 + K2 > self.max_force:
                    scale_factor = self.max_force / (K1 + K2)
                    safe_gains[0] *= scale_factor
                    safe_gains[1] *= scale_factor

        return safe_gains