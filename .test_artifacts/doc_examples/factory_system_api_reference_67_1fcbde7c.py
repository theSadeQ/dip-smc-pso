# Example from: docs\api\factory_system_api_reference.md
# Index: 67
# Runnable: False
# Hash: 1fcbde7c

# example-metadata:
# runnable: false

"""
Example 3: Batch Controller Comparison
Demonstrates creating multiple controller types for benchmarking.
"""

from src.controllers.factory import create_controller, list_available_controllers
from src.config import load_config
import numpy as np
import pandas as pd

def simulate_trajectory(controller, initial_state, duration=2.0, dt=0.01):
    """Simulate closed-loop trajectory."""
    steps = int(duration / dt)
    state = initial_state.copy()

    trajectory = []
    controls = []

    for _ in range(steps):
        # Compute control
        result = controller.compute_control(state, 0.0, {})
        if hasattr(result, 'u'):
            u = result.u
        else:
            u = result['u'] if isinstance(result, dict) else result

        # Simple dynamics (placeholder - use actual dynamics in practice)
        state_dot = np.random.randn(6) * 0.1  # Dummy dynamics
        state = state + state_dot * dt

        trajectory.append(state.copy())
        controls.append(u)

    return np.array(trajectory), np.array(controls)

def compute_performance_metrics(trajectory, controls):
    """Compute performance metrics."""
    # ISE: Integral of squared error
    ise = np.sum(trajectory[:, :3]**2)

    # Control effort
    effort = np.sum(controls**2)

    # Settling time (simplified)
    threshold = 0.02
    settled = np.all(np.abs(trajectory[:, :3]) < threshold, axis=1)
    settling_time = np.argmax(settled) * 0.01 if np.any(settled) else float('inf')

    return {
        'ise': ise,
        'effort': effort,
        'settling_time': settling_time
    }

def main():
    # Load configuration
    config = load_config("config.yaml")

    # Initial condition
    initial_state = np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0])

    # Create all available controllers
    print("Creating controllers...")
    results = []

    for controller_type in list_available_controllers():
        try:
            print(f"  Creating {controller_type}...")
            controller = create_controller(controller_type, config)

            # Simulate
            print(f"  Simulating {controller_type}...")
            trajectory, controls = simulate_trajectory(controller, initial_state)

            # Compute metrics
            metrics = compute_performance_metrics(trajectory, controls)

            results.append({
                'controller': controller_type,
                'ise': metrics['ise'],
                'effort': metrics['effort'],
                'settling_time': metrics['settling_time'],
                'n_gains': len(controller.gains) if hasattr(controller, 'gains') else 0
            })

            print(f"  ✓ {controller_type}: ISE={metrics['ise']:.3f}")

        except Exception as e:
            print(f"  ✗ Failed to benchmark {controller_type}: {e}")

    # Display results
    print("\n" + "="*80)
    print("BENCHMARK RESULTS")
    print("="*80)

    df = pd.DataFrame(results)
    df_sorted = df.sort_values('ise')

    print(df_sorted.to_string(index=False))

    # Identify best controller
    best = df_sorted.iloc[0]
    print(f"\n🏆 Best Controller: {best['controller']}")
    print(f"   ISE: {best['ise']:.3f}")
    print(f"   Control Effort: {best['effort']:.3f}")
    print(f"   Settling Time: {best['settling_time']:.3f} s")

if __name__ == '__main__':
    main()