# Example from: docs\configuration_schema_validation.md
# Index: 3
# Runnable: False
# Hash: da5836ad

# example-metadata:
# runnable: false

class ClassicalSMCConfig(BaseModel):
    """Classical SMC controller configuration schema."""
    gains: List[float] = Field(..., min_items=6, max_items=6, description="SMC gains [λ₁, λ₂, x, θ̇₁, θ̇₂, ẋ]")
    saturation_limit: float = Field(..., gt=0.1, le=100.0, description="Control saturation limit")
    boundary_layer_thickness: float = Field(0.01, gt=0.001, le=1.0, description="Boundary layer thickness")

    @validator('gains')
    def validate_smc_gains(cls, v):
        """Validate SMC gain constraints for stability."""
        lambda1, lambda2, x_gain, theta1_dot_gain, theta2_dot_gain, x_dot_gain = v

        # Sliding surface gains must be positive
        if lambda1 <= 0 or lambda2 <= 0:
            raise ValueError("Sliding surface gains λ₁, λ₂ must be positive")

        # Stability margin requirements
        if lambda1 < 0.5 or lambda1 > 50.0:
            raise ValueError("λ₁ must be in range [0.5, 50.0] for stability")

        if lambda2 < 0.5 or lambda2 > 50.0:
            raise ValueError("λ₂ must be in range [0.5, 50.0] for stability")

        # Gain ratios for balanced control
        ratio_lambda = lambda1 / lambda2
        if not 0.2 <= ratio_lambda <= 5.0:
            raise ValueError("λ₁/λ₂ ratio must be in range [0.2, 5.0]")

        return v

    @validator('saturation_limit')
    def validate_saturation_safety(cls, v, values):
        """Validate saturation limit for hardware safety."""
        if v > 50.0:
            raise ValueError("Saturation limit exceeds hardware safety threshold")
        return v

class STASMCConfig(BaseModel):
    """Super-Twisting Algorithm SMC configuration schema."""
    alpha1: float = Field(..., gt=0.1, le=20.0, description="STA parameter α₁")
    alpha2: float = Field(..., gt=0.1, le=20.0, description="STA parameter α₂")
    saturation_limit: float = Field(..., gt=0.1, le=100.0, description="Control saturation limit")

    @validator('alpha2')
    def validate_sta_stability_condition(cls, v, values):
        """Validate STA stability conditions."""
        if 'alpha1' in values:
            alpha1 = values['alpha1']

            # Stability condition: α₂ > α₁²/4
            if v <= alpha1**2 / 4:
                raise ValueError(f"STA stability requires α₂ > α₁²/4, got α₂={v}, α₁²/4={alpha1**2/4}")

            # Convergence condition
            if alpha1 > 2 * np.sqrt(v):
                raise ValueError("STA convergence condition violated: α₁ ≤ 2√α₂")

        return v

class AdaptiveSMCConfig(BaseModel):
    """Adaptive SMC configuration schema."""
    initial_gains: List[float] = Field(..., min_items=6, max_items=6, description="Initial parameter estimates")
    adaptation_rate: float = Field(..., gt=0.001, le=10.0, description="Parameter adaptation rate γ")
    parameter_bounds: List[float] = Field(..., min_items=2, max_items=2, description="[min, max] parameter bounds")

    @validator('parameter_bounds')
    def validate_parameter_bounds(cls, v):
        """Validate parameter bound constraints."""
        min_bound, max_bound = v

        if min_bound <= 0:
            raise ValueError("Minimum parameter bound must be positive")

        if max_bound <= min_bound:
            raise ValueError("Maximum bound must be greater than minimum bound")

        if max_bound / min_bound > 1000:
            raise ValueError("Parameter bound ratio exceeds numerical stability limit")

        return v

    @validator('initial_gains')
    def validate_initial_gains_bounds(cls, v, values):
        """Validate initial gains within parameter bounds."""
        if 'parameter_bounds' in values:
            min_bound, max_bound = values['parameter_bounds']
            for gain in v:
                if not min_bound <= gain <= max_bound:
                    raise ValueError(f"Initial gain {gain} outside bounds [{min_bound}, {max_bound}]")
        return v