# Example from: docs\configuration_schema_validation.md
# Index: 5
# Runnable: False
# Hash: 3ca90ca1

# example-metadata:
# runnable: false

class SimulationConfig(BaseModel):
    """Simulation configuration schema."""
    dt: float = Field(..., gt=0.0001, le=0.1, description="Integration time step (s)")
    duration: float = Field(..., gt=0.1, le=3600.0, description="Simulation duration (s)")
    initial_state: List[float] = Field(..., min_items=6, max_items=6, description="Initial system state")
    target_state: List[float] = Field(..., min_items=6, max_items=6, description="Target system state")

    @validator('dt')
    def validate_sampling_time(cls, v):
        """Validate sampling time for numerical stability."""
        # Nyquist criterion for control systems
        max_frequency = 100  # Hz, typical control bandwidth
        min_dt = 1 / (10 * max_frequency)  # 10x oversampling

        if v > 1 / (2 * max_frequency):
            raise ValueError(f"Sampling time {v}s violates Nyquist criterion")

        if v < min_dt:
            raise ValueError(f"Sampling time {v}s too small, computational overhead")

        return v

    @validator('initial_state', 'target_state')
    def validate_state_vectors(cls, v, field):
        """Validate state vector constraints."""
        theta1, theta2, x, theta1_dot, theta2_dot, x_dot = v

        # Position constraints
        if not -np.pi <= theta1 <= np.pi:
            raise ValueError(f"θ₁ must be in range [-π, π], got {theta1}")

        if not -np.pi <= theta2 <= np.pi:
            raise ValueError(f"θ₂ must be in range [-π, π], got {theta2}")

        if not -10.0 <= x <= 10.0:
            raise ValueError(f"Cart position must be in range [-10, 10]m, got {x}")

        # Velocity constraints (safety limits)
        if abs(theta1_dot) > 50.0:
            raise ValueError(f"θ̇₁ exceeds safety limit: {theta1_dot}")

        if abs(theta2_dot) > 50.0:
            raise ValueError(f"θ̇₂ exceeds safety limit: {theta2_dot}")

        if abs(x_dot) > 20.0:
            raise ValueError(f"Cart velocity exceeds safety limit: {x_dot}")

        return v

    @validator('duration')
    def validate_simulation_duration(cls, v, values):
        """Validate simulation duration constraints."""
        if 'dt' in values:
            dt = values['dt']
            num_steps = int(v / dt)

            if num_steps > 1000000:  # 1M steps
                raise ValueError("Simulation too long, may cause memory issues")

            if num_steps < 10:
                raise ValueError("Simulation too short for meaningful results")

        return v