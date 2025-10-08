# Example from: docs\guides\workflows\monte-carlo-validation-quickstart.md
# Index: 1
# Runnable: False
# Hash: 668e7aa5

# example-metadata:
# runnable: false

#!/usr/bin/env python
"""Quick Monte Carlo validation: 10 trials × 2 controllers × 1 scenario."""

import numpy as np
import subprocess
import json
from pathlib import Path

# Configuration
N_TRIALS = 10  # Quick test (use 50+ for publication)
CONTROLLERS = ['classical_smc', 'sta_smc']
DURATION = 5.0  # Seconds
RESULTS_DIR = Path('monte_carlo_quick_test')
RESULTS_DIR.mkdir(exist_ok=True)

# Run trials
results = []
for controller in CONTROLLERS:
    print(f"\\nRunning {controller}...")
    for trial in range(N_TRIALS):
        seed = 1000 + trial  # Reproducible seeds

        # Run simulation
        cmd = [
            'python', 'simulate.py',
            '--controller', controller,
            '--duration', str(DURATION),
            '--seed', str(seed),
            '--no-plot'  # Suppress plotting for batch runs
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Parse output (example - adjust to actual output format)
            # Assuming simulate.py prints metrics in JSON format
            # In practice, you'd capture metrics from simulation results

            results.append({
                'controller': controller,
                'trial': trial,
                'seed': seed,
                # Placeholder metrics - replace with actual parsing
                'ise': np.random.uniform(0.1, 0.5),  # Example
                'settling_time': np.random.uniform(2.0, 4.0),  # Example
            })

            print(f"  Trial {trial+1}/{N_TRIALS} complete")

        except subprocess.CalledProcessError as e:
            print(f"  Trial {trial} failed: {e}")
            continue

# Save results
import pandas as pd
df = pd.DataFrame(results)
df.to_csv(RESULTS_DIR / 'results.csv', index=False)
print(f"\\nResults saved to: {RESULTS_DIR / 'results.csv'}")
print(df.groupby('controller')[['ise', 'settling_time']].describe())