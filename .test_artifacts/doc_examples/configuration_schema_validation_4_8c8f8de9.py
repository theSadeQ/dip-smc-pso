# Example from: docs\configuration_schema_validation.md
# Index: 4
# Runnable: False
# Hash: 8c8f8de9

class PSOConfig(BaseModel):
    """PSO optimization configuration schema."""
    n_particles: int = Field(..., ge=10, le=200, description="Number of particles in swarm")
    max_iterations: int = Field(..., ge=10, le=1000, description="Maximum optimization iterations")
    w: float = Field(..., gt=0.1, lt=1.0, description="Inertia weight")
    c1: float = Field(..., gt=0.0, le=4.0, description="Cognitive acceleration coefficient")
    c2: float = Field(..., gt=0.0, le=4.0, description="Social acceleration coefficient")
    bounds: dict = Field(..., description="Parameter bounds for each controller type")

    @validator('c1', 'c2')
    def validate_acceleration_coefficients(cls, v, values, field):
        """Validate PSO acceleration coefficient constraints."""
        # Get both c1 and c2 if available
        c1 = values.get('c1', v if field.name == 'c1' else None)
        c2 = values.get('c2', v if field.name == 'c2' else None)

        if c1 is not None and c2 is not None:
            # Stability condition: c1 + c2 > 4 for constriction factor
            if c1 + c2 <= 4.0:
                raise ValueError("PSO stability requires c₁ + c₂ > 4")

            # Balance condition for exploration vs exploitation
            ratio = c1 / c2 if c2 > 0 else float('inf')
            if not 0.2 <= ratio <= 5.0:
                raise ValueError("c₁/c₂ ratio should be in range [0.2, 5.0] for balanced search")

        return v

    @validator('w')
    def validate_inertia_weight(cls, v, values):
        """Validate inertia weight for convergence."""
        # Linear decreasing inertia weight strategy
        if v < 0.4:
            raise ValueError("Inertia weight too low, may cause premature convergence")
        if v >= 0.9:
            raise ValueError("Inertia weight too high, may prevent convergence")
        return v

    @validator('bounds')
    def validate_optimization_bounds(cls, v):
        """Validate optimization bounds for each controller."""
        required_controllers = ['classical_smc', 'sta_smc', 'adaptive_smc']

        for controller in required_controllers:
            if controller not in v:
                raise ValueError(f"Missing optimization bounds for controller: {controller}")

            bounds = v[controller]
            if not isinstance(bounds, list):
                raise ValueError(f"Bounds for {controller} must be a list")

            # Validate bound structure
            for i, bound_pair in enumerate(bounds):
                if len(bound_pair) != 2:
                    raise ValueError(f"Bound {i} for {controller} must have [min, max] format")

                min_val, max_val = bound_pair
                if min_val >= max_val:
                    raise ValueError(f"Invalid bound {i} for {controller}: min >= max")

                if min_val <= 0:
                    raise ValueError(f"Bound {i} minimum for {controller} must be positive")

        return v