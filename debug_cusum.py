#=======================================================================================\\\
#==================================== debug_cusum.py ====================================\\\
#=======================================================================================\\\

#!/usr/bin/env python3
"""Debug script to analyze CUSUM drift detection issue."""

import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.analysis.fault_detection.fdi import FDIsystem

class DriftingDynamics:
    def __init__(self):
        self.drift = 0.0

    def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
        self.drift += 0.001  # Slowly increasing drift
        return state + self.drift * np.ones_like(state)

def debug_cusum():
    """Debug CUSUM drift detection."""

    fdi = FDIsystem(
        residual_threshold=0.05,  # Lower threshold so drift creates positive deviations
        persistence_counter=100,  # High persistence to rely on CUSUM
        cusum_enabled=True,
        cusum_threshold=2.0,
        adaptive=False  # Use fixed reference
    )
    dynamics = DriftingDynamics()

    state = np.array([0.1, 0.0, 0.0, 0.0])

    print("Debugging CUSUM drift detection...")
    print("Target: CUSUM should accumulate drift and trigger fault")
    print()

    for i in range(50):  # First 50 steps
        t = 0.01 * i

        # Measurement stays the same, but dynamics drift
        predicted = dynamics.step(fdi._last_state if fdi._last_state is not None else state, 0.0, 0.01)
        status, residual = fdi.check(t, state, 0.0, 0.01, dynamics)

        if i < 5 or i % 10 == 0 or status == "FAULT":
            print(f"Step {i:3d}: t={t:.3f}, drift={dynamics.drift:.4f}")
            print(f"  predicted: {predicted}")
            print(f"  measured:  {state}")
            print(f"  residual:  {residual:.6f}")
            print(f"  cusum:     {fdi._cusum:.6f}")
            print(f"  status:    {status}")

            if i > 0:
                # Manual calculation
                residual_vec = state - predicted
                residual_norm_manual = np.linalg.norm(residual_vec)
                ref = fdi.residual_threshold  # Since adaptive=False
                deviation = residual_norm_manual - ref
                print(f"  Manual: norm={residual_norm_manual:.6f}, ref={ref:.3f}, deviation={deviation:.6f}")
            print()

        if status == "FAULT":
            print(f"FAULT detected at step {i}")
            break
    else:
        print("No fault detected in 50 steps")
        print(f"Final CUSUM: {fdi._cusum:.6f} (threshold: {fdi.cusum_threshold})")

if __name__ == "__main__":
    debug_cusum()