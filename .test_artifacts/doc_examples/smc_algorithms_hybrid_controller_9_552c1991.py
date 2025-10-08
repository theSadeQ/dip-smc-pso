# Example from: docs\reference\controllers\smc_algorithms_hybrid_controller.md
# Index: 9
# Runnable: True
# Hash: 552c1991

from src.controllers.factory import create_all_smc_controllers

gains_dict = {
    "classical": [10, 8, 15, 12, 50, 5],
    "adaptive": [10, 8, 15, 12, 25],
    "sta": [25, 10, 15, 12, 20, 15],
    "hybrid": [15, 12, 18, 15]
}

controllers = create_all_smc_controllers(gains_dict, max_force=100.0)

# Benchmark all controllers
from src.benchmarks import run_comprehensive_comparison
comparison = run_comprehensive_comparison(
    controllers=controllers,
    scenarios='standard',
    metrics='all'
)

comparison.generate_report('controller_comparison.pdf')