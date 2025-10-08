# Example from: docs\guides\tutorials\tutorial-02-controller-comparison.md
# Index: 1
# Runnable: True
# Hash: 9604faed

import json
import numpy as np

# Load all results
results = {
    'classical': json.load(open('results_classical.json')),
    'sta': json.load(open('results_sta.json')),
    'adaptive': json.load(open('results_adaptive.json')),
    'hybrid': json.load(open('results_hybrid.json'))
}

# Compare key metrics
for name, data in results.items():
    print(f"\n{name.upper()} SMC:")
    print(f"  ISE:              {data['metrics']['ise']:.4f}")
    print(f"  ITAE:             {data['metrics']['itae']:.4f}")
    print(f"  Settling Time:    {data['metrics']['settling_time']:.2f} s")
    print(f"  Peak Overshoot:   {data['metrics']['overshoot']:.2f}%")
    print(f"  Control Effort:   {data['metrics']['control_effort']:.2f}")