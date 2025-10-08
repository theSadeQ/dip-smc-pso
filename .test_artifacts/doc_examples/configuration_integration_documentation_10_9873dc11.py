# Example from: docs\configuration_integration_documentation.md
# Index: 10
# Runnable: True
# Hash: 9873dc11

from pydantic import BaseModel
from typing import Dict, Any

class ControllerConfig(BaseModel):
    gains: List[float]
    max_force: float
    boundary_layer: float
    dt: float

class ProjectConfig(BaseModel):
    controllers: Dict[str, ControllerConfig]
    physics: Dict[str, float]
    simulation: Dict[str, Any]

# Usage
config_data = {
    'controllers': {
        'classical_smc': {
            'gains': [20, 15, 12, 8, 35, 5],
            'max_force': 150.0,
            'boundary_layer': 0.02,
            'dt': 0.001
        }
    },
    'physics': {'m1': 0.5, 'm2': 0.5, 'M': 2.0},
    'simulation': {'duration': 5.0, 'dt': 0.001}
}

config = ProjectConfig(**config_data)
controller = create_controller('classical_smc', config=config)