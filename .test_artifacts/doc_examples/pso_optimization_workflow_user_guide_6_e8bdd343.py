# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 6
# Runnable: True
# Hash: e8bdd343

import concurrent.futures
import subprocess
from pathlib import Path

def optimize_controller(controller_type):
    """Optimize single controller type."""
    cmd = [
        'python', 'simulate.py',
        '--ctrl', controller_type,
        '--run-pso',
        '--save', f'{controller_type}_parallel.json'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return controller_type, result.returncode == 0, result.stdout

def parallel_optimization():
    """Run parallel PSO optimization for multiple controllers."""
    controllers = ['classical_smc', 'sta_smc', 'adaptive_smc']

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(optimize_controller, ctrl): ctrl for ctrl in controllers}

        for future in concurrent.futures.as_completed(futures):
            controller = futures[future]
            ctrl_name, success, output = future.result()

            if success:
                print(f"✓ {ctrl_name} optimization completed")
            else:
                print(f"✗ {ctrl_name} optimization failed")
                print(f"Error output: {output}")

if __name__ == "__main__":
    parallel_optimization()