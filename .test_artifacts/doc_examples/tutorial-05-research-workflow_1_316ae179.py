# Example from: docs\guides\tutorials\tutorial-05-research-workflow.md
# Index: 1
# Runnable: True
# Hash: 316ae179

#!/usr/bin/env python
"""
Monte Carlo robustness study: Classical vs Hybrid Adaptive STA-SMC.

Runs N trials for each controller × scenario combination with random seeds.
"""

import numpy as np
import subprocess
import json
import yaml
from pathlib import Path
from tqdm import tqdm
import pandas as pd

# Configuration
N_TRIALS = 50  # Monte Carlo sample size
CONTROLLERS = ['classical_smc', 'hybrid_adaptive_sta_smc']
SCENARIOS_FILE = 'experiments/robustness_study/scenarios.yaml'
RESULTS_DIR = Path('experiments/robustness_study/results')
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Load scenarios
with open(SCENARIOS_FILE) as f:
    scenarios_config = yaml.safe_load(f)
scenarios = scenarios_config['scenarios']

# Main experiment loop
results = []

for controller in CONTROLLERS:
    print(f"\n{'='*60}")
    print(f"Running trials for {controller}")
    print(f"{'='*60}")

    for scenario_name, scenario in scenarios.items():
        print(f"\nScenario: {scenario['name']}")

        for trial in tqdm(range(N_TRIALS), desc="Trials"):
            # Unique seed for reproducibility
            seed = hash((controller, scenario_name, trial)) % (2**31)

            # Construct simulation command
            cmd = [
                'python', 'simulate.py',
                '--ctrl', controller,
                '--seed', str(seed),
                '--override', f"dip_params.m0={scenario['parameters']['m0']}",
                '--override', f"dip_params.m1={scenario['parameters']['m1']}",
                '--override', f"dip_params.m2={scenario['parameters']['m2']}",
                '--override', f"simulation.initial_conditions={scenario['initial_conditions']}",
                '--save', f"{RESULTS_DIR}/{controller}_{scenario_name}_{trial}.json"
            ]

            # Run simulation
            try:
                subprocess.run(cmd, check=True, capture_output=True)

                # Load results
                result_file = f"{RESULTS_DIR}/{controller}_{scenario_name}_{trial}.json"
                with open(result_file) as f:
                    data = json.load(f)

                # Extract metrics
                results.append({
                    'controller': controller,
                    'scenario': scenario_name,
                    'trial': trial,
                    'seed': seed,
                    'ise': data['metrics']['ise'],
                    'itae': data['metrics']['itae'],
                    'settling_time': data['metrics']['settling_time'],
                    'overshoot': data['metrics']['overshoot'],
                    'control_effort': data['metrics']['control_effort'],
                    'm0': scenario['parameters']['m0'],
                    'm1': scenario['parameters']['m1'],
                    'm2': scenario['parameters']['m2'],
                })

            except subprocess.CalledProcessError as e:
                print(f"ERROR in trial {trial}: {e}")
                continue

# Save raw results
df = pd.DataFrame(results)
df.to_csv(f"{RESULTS_DIR}/monte_carlo_results.csv", index=False)

print(f"\n{'='*60}")
print(f"Experiment complete!")
print(f"Total trials: {len(results)}")
print(f"Results saved to: {RESULTS_DIR}/monte_carlo_results.csv")
print(f"{'='*60}")