# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 13
# Runnable: False
# Hash: 95da8e0b

# example-metadata:
# runnable: false

from dataclasses import dataclass
from typing import Optional
import yaml

@dataclass
class PSO_OptimizationConfig:
    """
    Complete configuration for PSO optimization workflows.

    Provides type-safe configuration with validation and defaults.
    """

    # Controller configuration
    controller_type: str
    controller_config: Dict[str, Any]

    # PSO algorithm parameters
    n_particles: int = 30
    max_iterations: int = 100
    c1: float = 2.0  # Cognitive component
    c2: float = 2.0  # Social component
    w: float = 0.9   # Inertia weight

    # Optimization objectives
    objectives: Dict[str, float] = None  # {'ise': 0.4, 'overshoot': 0.3, 'energy': 0.3}

    # Performance settings
    enable_parallel_evaluation: bool = True
    n_threads: int = 4
    enable_gpu_acceleration: bool = False

    # Caching and persistence
    enable_simulation_cache: bool = True
    cache_size: int = 1000
    save_intermediate_results: bool = True

    # Error handling
    max_retries: int = 3
    simulation_timeout: float = 30.0
    enable_fallback: bool = True

    # Convergence detection
    convergence_patience: int = 20
    convergence_tolerance: float = 1e-6
    enable_early_stopping: bool = True

    # Monitoring and logging
    enable_monitoring: bool = True
    log_level: str = 'INFO'
    save_optimization_history: bool = True

    def __post_init__(self):
        """Validate configuration after initialization."""

        # Set default objectives if not provided
        if self.objectives is None:
            self.objectives = {'ise': 0.5, 'overshoot': 0.3, 'settling_time': 0.2}

        # Validate objectives sum to 1.0
        if abs(sum(self.objectives.values()) - 1.0) > 1e-6:
            raise ValueError("Objective weights must sum to 1.0")

        # Validate PSO parameters
        if not (0 < self.c1 < 5 and 0 < self.c2 < 5):
            raise ValueError("PSO cognitive/social parameters must be in (0, 5)")

        if not (0 < self.w < 1):
            raise ValueError("PSO inertia weight must be in (0, 1)")

        # Validate controller type
        valid_types = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']
        if self.controller_type not in valid_types:
            raise ValueError(f"Controller type must be one of {valid_types}")

def load_pso_config_from_yaml(config_path: str) -> PSO_OptimizationConfig:
    """Load PSO configuration from YAML file with validation."""

    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)

    # Extract PSO-specific configuration
    pso_config = config_dict.get('pso_optimization', {})

    return PSO_OptimizationConfig(**pso_config)

def save_pso_config_to_yaml(config: PSO_OptimizationConfig, output_path: str) -> None:
    """Save PSO configuration to YAML file."""

    config_dict = {
        'pso_optimization': {
            'controller_type': config.controller_type,
            'controller_config': config.controller_config,
            'n_particles': config.n_particles,
            'max_iterations': config.max_iterations,
            'c1': config.c1,
            'c2': config.c2,
            'w': config.w,
            'objectives': config.objectives,
            # ... include all configuration fields
        }
    }

    with open(output_path, 'w') as f:
        yaml.dump(config_dict, f, default_flow_style=False, indent=2)