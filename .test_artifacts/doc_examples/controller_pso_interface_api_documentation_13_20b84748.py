# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 13
# Runnable: True
# Hash: 20b84748

from src.controllers.factory import ControllerFactory
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller factory for specific type
def create_classical_smc(gains: np.ndarray) -> ClassicalSMC:
    return ControllerFactory.create_controller('classical_smc', gains)

# Initialize PSO tuner
pso_tuner = PSOTuner(
    controller_factory=create_classical_smc,
    config=config,
    seed=42
)

# Extract bounds from configuration
bounds_config = config.pso.bounds.classical_smc
lower_bounds = np.array(bounds_config.lower)
upper_bounds = np.array(bounds_config.upper)

# Run optimization
results = pso_tuner.optimize(
    bounds=(lower_bounds, upper_bounds),
    n_particles=50,
    n_iterations=100
)

# Extract optimized gains
optimal_gains = results['best_gains']
optimal_controller = create_classical_smc(optimal_gains)