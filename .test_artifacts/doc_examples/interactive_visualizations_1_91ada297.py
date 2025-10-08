# Example from: docs\guides\interactive_visualizations.md
# Index: 1
# Runnable: True
# Hash: 91ada297

# In simulation script
import json

results = run_simulation(controller, duration=5.0)
chart_data = {
    "labels": results['time'].tolist(),
    "datasets": [{
        "label": "Theta1",
        "data": results['theta1'].tolist()
    }]
}

with open('docs/_data/sim_results.json', 'w') as f:
    json.dump(chart_data, f)