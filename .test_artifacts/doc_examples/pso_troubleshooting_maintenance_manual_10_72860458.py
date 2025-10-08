# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 10
# Runnable: False
# Hash: 72860458

# example-metadata:
# runnable: false

class OptimizedPSOConfig:
    """Optimized PSO configurations for different scenarios."""

    @staticmethod
    def fast_exploration():
        """Configuration for rapid initial exploration."""
        return {
            'n_particles': 30,
            'n_iterations': 50,
            'cognitive_weight': 2.5,
            'social_weight': 0.5,
            'inertia_weight': 0.9,
            'velocity_clamp': [0.2, 0.8]
        }

    @staticmethod
    def precision_optimization():
        """Configuration for high-precision results."""
        return {
            'n_particles': 100,
            'n_iterations': 300,
            'cognitive_weight': 1.49445,
            'social_weight': 1.49445,
            'inertia_weight': 0.729,
            'w_schedule': [0.9, 0.4],
            'tolerance': 1e-8
        }

    @staticmethod
    def balanced_performance():
        """Configuration balancing speed and quality."""
        return {
            'n_particles': 50,
            'n_iterations': 150,
            'cognitive_weight': 1.8,
            'social_weight': 1.2,
            'inertia_weight': 0.8,
            'w_schedule': [0.8, 0.3],
            'velocity_clamp': [0.1, 0.5]
        }

# Usage
def optimize_with_config(controller_type, config_type='balanced'):
    """Optimize controller with specific PSO configuration."""
    from src.optimization.algorithms.pso_optimizer import PSOTuner

    config_map = {
        'fast': OptimizedPSOConfig.fast_exploration(),
        'precision': OptimizedPSOConfig.precision_optimization(),
        'balanced': OptimizedPSOConfig.balanced_performance()
    }

    pso_config = config_map[config_type]

    # Apply configuration and run optimization
    # ... implementation details