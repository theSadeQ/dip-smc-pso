# Example from: docs\api\factory_system_api_reference.md
# Index: 8
# Runnable: True
# Hash: b98108a9

from src.controllers.factory import create_controller
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config

# Load configuration
config = load_config("config.yaml")

# PSO optimization finds optimal gains
# (See PSO Integration section for complete optimization workflow)
optimized_gains = [25.3, 18.7, 14.2, 10.8, 42.6, 6.1]  # From PSO

# Create controller with optimized gains
controller = create_controller('classical_smc', config, gains=optimized_gains)

# Optimized controller has lower cost than defaults
baseline_cost = evaluate_controller(create_controller('classical_smc', config))
optimized_cost = evaluate_controller(controller)
print(f"Cost improvement: {((baseline_cost - optimized_cost) / baseline_cost * 100):.1f}%")