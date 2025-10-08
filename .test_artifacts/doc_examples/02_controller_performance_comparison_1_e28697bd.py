# Example from: docs\tutorials\02_controller_performance_comparison.md
# Index: 1
# Runnable: True
# Hash: e28697bd

# Export simulation results to JSON
import json
import numpy as np

results = {
    "labels": time_array.tolist(),
    "datasets": [{
        "label": "Your Controller",
        "data": theta1_array.tolist(),
        "borderColor": "rgb(75, 192, 192)"
    }]
}

with open('docs/_data/my_results.json', 'w') as f:
    json.dump(results, f)