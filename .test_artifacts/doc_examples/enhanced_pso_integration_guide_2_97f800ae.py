# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 2
# Runnable: False
# Hash: 97f800ae

class PSOControllerWrapper:
    """
    PSO-optimized controller wrapper with comprehensive validation.

    Provides:
    - Simplified control interface for fitness evaluation
    - Automatic gain validation with controller-specific rules
    - Performance monitoring and error handling
    - Thread-safe operation for parallel PSO
    """

    def __init__(self, controller: Any, controller_type: str, validation_config: Dict[str, Any]):
        self.controller = controller
        self.controller_type = controller_type
        self.validation_config = validation_config

        # PSO-required attributes
        self.n_gains = CONTROLLER_REGISTRY[controller_type]['gain_count']
        self.max_force = getattr(controller, 'max_force', 150.0)

        # Performance tracking
        self.control_calls = 0
        self.control_failures = 0
        self.last_control_time = 0.0

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """
        Vectorized gain validation for PSO particle swarms.

        Args:
            particles: Array of shape (n_particles, n_gains)

        Returns:
            Boolean mask indicating valid particles
        """
        if particles.ndim == 1:
            particles = particles.reshape(1, -1)

        valid_mask = np.ones(particles.shape[0], dtype=bool)

        # Basic validation
        for i, gains in enumerate(particles):
            try:
                # Check gain count
                if len(gains) != self.n_gains:
                    valid_mask[i] = False
                    continue

                # Check for finite positive values
                if not all(np.isfinite(g) and g > 0 for g in gains):
                    valid_mask[i] = False
                    continue

                # Controller-specific validation
                if not self._validate_controller_specific_constraints(gains):
                    valid_mask[i] = False
                    continue

            except Exception:
                valid_mask[i] = False

        return valid_mask

    def _validate_controller_specific_constraints(self, gains: List[float]) -> bool:
        """Apply mathematical constraints for each controller type."""

        if self.controller_type == 'classical_smc':
            # Classical SMC: All gains positive, reasonable ranges
            k1, k2, lam1, lam2, K, kd = gains
            return all(g > 0 for g in gains[:5]) and kd >= 0

        elif self.controller_type == 'sta_smc':
            # Super-Twisting: Critical stability condition K1 > K2
            K1, K2 = gains[0], gains[1]
            return K1 > K2 > 0 and all(g > 0 for g in gains[2:])

        elif self.controller_type == 'adaptive_smc':
            # Adaptive SMC: Adaptation rate bounds
            k1, k2, lam1, lam2, gamma = gains
            return all(g > 0 for g in gains[:4]) and 0.1 <= gamma <= 20.0

        elif self.controller_type == 'hybrid_adaptive_sta_smc':
            # Hybrid SMC: Surface parameters positive
            return all(g > 0 for g in gains)

        return True

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """
        PSO-compatible control computation with error handling.

        Args:
            state: System state vector [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]

        Returns:
            Control output as numpy array
        """
        try:
            self.control_calls += 1
            start_time = time.time()

            # Validate input state
            if len(state) != 6:
                raise ValueError(f"Expected 6-element state, got {len(state)}")

            # Call underlying controller
            result = self.controller.compute_control(state, {}, {})

            # Extract control value
            if hasattr(result, 'u'):
                u = result.u
            elif isinstance(result, dict) and 'u' in result:
                u = result['u']
            else:
                u = result

            # Apply saturation and return as array
            u_sat = np.clip(float(u), -self.max_force, self.max_force)

            # Performance tracking
            self.last_control_time = time.time() - start_time

            return np.array([u_sat])

        except Exception as e:
            self.control_failures += 1
            # Return safe fallback control
            return np.array([0.0])