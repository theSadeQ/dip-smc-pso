# Example from: docs\configuration_schema_validation.md
# Index: 2
# Runnable: False
# Hash: 67a8c7dc

class PhysicsConfig(BaseModel):
    """Physical system parameters schema."""
    pendulum_length_1: float = Field(..., gt=0.1, le=2.0, description="Pendulum 1 length (m)")
    pendulum_length_2: float = Field(..., gt=0.1, le=2.0, description="Pendulum 2 length (m)")
    pendulum_mass_1: float = Field(..., gt=0.01, le=10.0, description="Pendulum 1 mass (kg)")
    pendulum_mass_2: float = Field(..., gt=0.01, le=10.0, description="Pendulum 2 mass (kg)")
    cart_mass: float = Field(..., gt=0.1, le=50.0, description="Cart mass (kg)")
    gravity: float = Field(9.81, gt=0.1, le=20.0, description="Gravitational acceleration (m/s²)")

    @validator('pendulum_length_2')
    def validate_length_ratio(cls, v, values):
        """Validate pendulum length ratio for stability."""
        if 'pendulum_length_1' in values:
            ratio = v / values['pendulum_length_1']
            if not 0.3 <= ratio <= 2.0:
                raise ValueError("Pendulum length ratio must be between 0.3 and 2.0")
        return v

    @validator('pendulum_mass_2')
    def validate_mass_ratio(cls, v, values):
        """Validate pendulum mass ratio for dynamic coupling."""
        if 'pendulum_mass_1' in values:
            ratio = v / values['pendulum_mass_1']
            if not 0.1 <= ratio <= 5.0:
                raise ValueError("Pendulum mass ratio must be between 0.1 and 5.0")
        return v