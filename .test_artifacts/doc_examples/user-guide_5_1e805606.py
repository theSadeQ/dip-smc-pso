# Example from: docs\guides\user-guide.md
# Index: 5
# Runnable: False
# Hash: 1e805606

# example-metadata:
# runnable: false

# batch_experiment.py
import subprocess
import json

controllers = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']
initial_conditions = [
    [0, 0, 0.1, 0, 0.15, 0],
    [0, 0, 0.2, 0, 0.25, 0],
    [0, 0, 0.3, 0, 0.35, 0]
]

results = {}

for ctrl in controllers:
    results[ctrl] = []
    for i, ic in enumerate(initial_conditions):
        print(f"Running {ctrl} with IC {i+1}/3...")

        # Run simulation
        cmd = [
            'python', 'simulate.py',
            '--ctrl', ctrl,
            '--override', f'simulation.initial_conditions={ic}',
            '--save', f'results_{ctrl}_ic{i}.json'
        ]
        subprocess.run(cmd)

        # Load results
        data = json.load(open(f'results_{ctrl}_ic{i}.json'))
        results[ctrl].append(data['metrics'])

# Analyze batch results
for ctrl in controllers:
    avg_ise = sum(r['ise'] for r in results[ctrl]) / len(results[ctrl])
    print(f"{ctrl:20s} Average ISE: {avg_ise:.4f}")