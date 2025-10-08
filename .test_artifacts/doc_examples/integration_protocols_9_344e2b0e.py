# Example from: docs\technical\integration_protocols.md
# Index: 9
# Runnable: True
# Hash: 344e2b0e

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Union

class IntegrationConfig(BaseModel):
    """Unified configuration for cross-domain integration."""

    # Controller configuration
    controller: Dict[str, Any] = Field(
        description="Controller-specific configuration"
    )

    # Plant model configuration
    plant_model: Dict[str, Any] = Field(
        description="Plant model configuration"
    )

    # Simulation configuration
    simulation: Dict[str, Any] = Field(
        default_factory=dict,
        description="Simulation engine configuration"
    )

    # Optimization configuration
    optimization: Optional[Dict[str, Any]] = Field(
        default=None,
        description="PSO optimization configuration"
    )

    # HIL configuration
    hil: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Hardware-in-the-loop configuration"
    )

    # Integration settings
    integration: Dict[str, Any] = Field(
        default_factory=lambda: {
            'real_time_mode': False,
            'safety_enabled': True,
            'logging_level': 'INFO'
        },
        description="Integration protocol settings"
    )

    class Config:
        schema_extra = {
            "example": {
                "controller": {
                    "type": "classical_smc",
                    "gains": [5.0, 5.0, 5.0, 0.5, 0.5, 0.5],
                    "max_force": 150.0
                },
                "plant_model": {
                    "type": "simplified_dip",
                    "m1": 0.5,
                    "m2": 0.5,
                    "l1": 0.5,
                    "l2": 0.5
                },
                "simulation": {
                    "dt": 0.001,
                    "t_final": 10.0,
                    "integration_method": "rk4"
                },
                "optimization": {
                    "algorithm": "pso",
                    "n_particles": 30,
                    "n_iterations": 100
                }
            }
        }

class ConfigurationValidator:
    """Validator for integration configurations."""

    @staticmethod
    def validate_integration_config(config: IntegrationConfig) -> bool:
        """Validate cross-domain configuration consistency."""

        # Validate controller-plant compatibility
        controller_type = config.controller.get('type')
        plant_type = config.plant_model.get('type')

        if not ConfigurationValidator._check_controller_plant_compatibility(
            controller_type, plant_type
        ):
            raise ValueError(
                f"Controller {controller_type} not compatible with plant {plant_type}"
            )

        # Validate real-time constraints
        if config.integration.get('real_time_mode', False):
            dt = config.simulation.get('dt', 0.001)
            if dt < 0.0001:  # 100μs minimum for real-time
                raise ValueError("Real-time mode requires dt ≥ 100μs")

        # Validate HIL safety requirements
        if config.hil is not None:
            max_force = config.controller.get('max_force', 150.0)
            hil_max_force = config.hil.get('max_safe_force', 50.0)
            if max_force > hil_max_force:
                logger.warning(
                    f"Controller max_force ({max_force}) exceeds HIL safety limit ({hil_max_force})"
                )

        return True

    @staticmethod
    def _check_controller_plant_compatibility(controller_type: str, plant_type: str) -> bool:
        """Check if controller and plant types are compatible."""
        # Define compatibility matrix
        compatibility_matrix = {
            'classical_smc': ['simplified_dip', 'full_dip'],
            'sta_smc': ['simplified_dip', 'full_dip', 'low_rank_dip'],
            'adaptive_smc': ['simplified_dip', 'full_dip'],
            'hybrid_adaptive_sta_smc': ['simplified_dip', 'full_dip']
        }

        compatible_plants = compatibility_matrix.get(controller_type, [])
        return plant_type in compatible_plants