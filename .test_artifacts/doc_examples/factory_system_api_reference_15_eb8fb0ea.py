# Example from: docs\api\factory_system_api_reference.md
# Index: 15
# Runnable: True
# Hash: eb8fb0ea

from src.controllers.factory import list_available_controllers, create_controller
import pandas as pd

# Benchmark all available controllers
results = []
for controller_type in list_available_controllers():
    controller = create_controller(controller_type)
    cost, time = evaluate_controller(controller)
    results.append({
        'controller': controller_type,
        'cost': cost,
        'computation_time': time
    })

# Display results
df = pd.DataFrame(results)
print(df.sort_values('cost'))