# Example from: docs\configuration_schema_validation.md
# Index: 7
# Runnable: False
# Hash: 458561a2

# example-metadata:
# runnable: false

class MasterConfig(BaseModel):
    """Master configuration schema with cross-validation."""
    system: SystemConfig
    physics: PhysicsConfig
    controllers: dict  # Dynamic controller configuration
    optimization: dict
    simulation: SimulationConfig
    hil: Optional[HILConfig] = None

    @validator('controllers')
    def validate_controller_configurations(cls, v, values):
        """Validate all controller configurations."""
        valid_controllers = {
            'classical_smc': ClassicalSMCConfig,
            'sta_smc': STASMCConfig,
            'adaptive_smc': AdaptiveSMCConfig,
            'hybrid_adaptive_sta_smc': dict  # Complex hybrid validation
        }

        for controller_name, config_data in v.items():
            if controller_name not in valid_controllers:
                raise ValueError(f"Unknown controller type: {controller_name}")

            # Validate specific controller configuration
            schema_class = valid_controllers[controller_name]
            if schema_class != dict:  # Skip complex schemas for now
                try:
                    schema_class(**config_data)
                except ValidationError as e:
                    raise ValueError(f"Controller {controller_name} validation failed: {e}")

        return v

    @validator('optimization')
    def validate_optimization_configuration(cls, v, values):
        """Validate optimization configuration with controller compatibility."""
        if 'pso' in v:
            pso_config = PSOConfig(**v['pso'])

            # Validate bounds compatibility with available controllers
            if 'controllers' in values:
                available_controllers = set(values['controllers'].keys())
                bound_controllers = set(pso_config.bounds.keys())

                missing_bounds = available_controllers - bound_controllers
                if missing_bounds:
                    raise ValueError(f"Missing PSO bounds for controllers: {missing_bounds}")

        return v

    class Config:
        """Pydantic configuration options."""
        validate_assignment = True
        arbitrary_types_allowed = True
        extra = 'forbid'  # Prevent extra fields