# Example from: docs\api\optimization_module_api_reference.md
# Index: 30
# Runnable: True
# Hash: 59cecb94

from src.optimization.integration.pso_factory_bridge import EnhancedPSOFactory
from src.controllers.factory import SMCType
import pandas as pd

# Optimize all controller types
controller_types = [SMCType.CLASSICAL, SMCType.STA, SMCType.ADAPTIVE, SMCType.HYBRID]
results = []

for ctrl_type in controller_types:
    factory = EnhancedPSOFactory(
        controller_type=ctrl_type,
        config=config
    )

    result = factory.optimize(max_iterations=100)

    results.append({
        'controller': ctrl_type.value,
        'best_cost': result['best_cost'],
        'convergence_iter': result['convergence_iteration'],
        'optimization_time': result['optimization_time']
    })

# Compare results
df = pd.DataFrame(results)
df = df.sort_values('best_cost')
print("\nController Performance Ranking:")
print(df.to_string(index=False))