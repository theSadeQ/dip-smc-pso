#!/usr/bin/env python3
"""Debug script to analyze weighted residual calculation bug."""

import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.analysis.fault_detection.fdi import FDIsystem

class LinearDynamics:
    def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
        return state + 0.01 * np.ones_like(state)

def debug_weighted_residual():
    """Debug the weighted residual calculation."""

    # Configure with weights emphasizing first state
    fdi = FDIsystem(
        residual_threshold=0.5,
        residual_states=[0, 1, 2, 3],
        residual_weights=[10.0, 1.0, 1.0, 1.0]  # High weight on first state
    )
    dynamics = LinearDynamics()

    # Initialize
    state1 = np.array([0.0, 0.0, 0.0, 0.0])
    print(f"Initial state: {state1}")

    status1, residual1 = fdi.check(0.0, state1, 0.0, 0.01, dynamics)
    print(f"First check: status={status1}, residual={residual1}")

    # Check internal state
    print(f"Last state after first check: {fdi._last_state}")

    # Small error in first state should be amplified by weight
    state2 = np.array([0.1, 0.0, 0.0, 0.0])  # Only first state has error
    print(f"Second state: {state2}")

    # Manually compute what the prediction should be
    predicted = dynamics.step(fdi._last_state, 0.0, 0.01)
    print(f"Predicted state: {predicted}")

    # Compute residual manually
    residual_vec = state2 - predicted
    print(f"Residual vector: {residual_vec}")

    # Apply weights manually
    sub = residual_vec[fdi.residual_states]
    print(f"Selected residual: {sub}")

    weighted_sub = sub * np.asarray(fdi.residual_weights, dtype=float)
    print(f"Weighted residual: {weighted_sub}")

    manual_norm = float(np.linalg.norm(weighted_sub))
    print(f"Manual norm calculation: {manual_norm}")

    # Now do the actual check
    status2, residual2 = fdi.check(0.01, state2, 0.0, 0.01, dynamics)
    print(f"Second check: status={status2}, residual={residual2}")

    print(f"Expected: > 1.0, Got: {residual2}")
    print(f"Test should pass: {residual2 > 1.0}")

def test_cleaner_scenario():
    """Test with a cleaner scenario that doesn't involve prediction interference."""

    class IdentityDynamics:
        def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
            return state  # No change - perfect prediction

    # Configure with weights emphasizing first state
    fdi = FDIsystem(
        residual_threshold=0.5,
        residual_states=[0, 1, 2, 3],
        residual_weights=[10.0, 1.0, 1.0, 1.0]  # High weight on first state
    )
    dynamics = IdentityDynamics()

    # Initialize
    state1 = np.array([0.0, 0.0, 0.0, 0.0])
    print(f"Clean test - Initial state: {state1}")

    status1, residual1 = fdi.check(0.0, state1, 0.0, 0.01, dynamics)
    print(f"First check: status={status1}, residual={residual1}")

    # Error only in first state
    state2 = np.array([0.1, 0.0, 0.0, 0.0])  # Only first state has error
    print(f"Second state: {state2}")

    # Since dynamics returns state unchanged, prediction = state1 = [0,0,0,0]
    # Residual = [0.1, 0.0, 0.0, 0.0]
    # Weighted = [1.0, 0.0, 0.0, 0.0]
    # Norm = 1.0

    status2, residual2 = fdi.check(0.01, state2, 0.0, 0.01, dynamics)
    print(f"Clean test result: status={status2}, residual={residual2}")
    print(f"Should be exactly 1.0: {residual2}")
    print(f"Test passes: {residual2 > 1.0}")

def test_fixed_test():
    """Test the corrected test case to verify the fix."""

    class LinearDynamics:
        def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
            return state + 0.01 * np.ones_like(state)

    # Configure with weights emphasizing first state
    fdi = FDIsystem(
        residual_threshold=0.5,
        residual_states=[0, 1, 2, 3],
        residual_weights=[10.0, 1.0, 1.0, 1.0]  # High weight on first state
    )
    dynamics = LinearDynamics()

    # Initialize
    state1 = np.array([0.0, 0.0, 0.0, 0.0])
    fdi.check(0.0, state1, 0.0, 0.01, dynamics)

    # Fixed test case
    state2 = np.array([0.111, 0.01, 0.01, 0.01])  # Compensated for dynamics + margin
    status, residual = fdi.check(0.01, state2, 0.0, 0.01, dynamics)

    print(f"Fixed test case:")
    print(f"  state2 = {state2}")
    print(f"  residual = {residual}")
    print(f"  passes test (> 1.0): {residual > 1.0}")

    # Manual calculation:
    predicted = np.array([0.01, 0.01, 0.01, 0.01])
    residual_vec = state2 - predicted
    print(f"  residual_vector = {residual_vec}")

    weighted = residual_vec * np.array([10.0, 1.0, 1.0, 1.0])
    print(f"  weighted = {weighted}")

    manual_norm = np.linalg.norm(weighted)
    print(f"  manual_norm = {manual_norm}")

def test_what_original_test_needed():
    """Test to understand what the original test actually needed to pass."""

    class LinearDynamics:
        def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
            return state + 0.01 * np.ones_like(state)

    # Configure with weights emphasizing first state
    fdi = FDIsystem(
        residual_threshold=0.5,
        residual_states=[0, 1, 2, 3],
        residual_weights=[10.0, 1.0, 1.0, 1.0]  # High weight on first state
    )
    dynamics = LinearDynamics()

    # Initialize
    state1 = np.array([0.0, 0.0, 0.0, 0.0])
    fdi.check(0.0, state1, 0.0, 0.01, dynamics)

    # What error would we need in first state to get residual > 1.0?
    # Current: error=0.09 -> weighted=0.9 -> norm ≈ 0.9002
    # We need: weighted_first > 1.0, so error_first > 0.1
    # But error_first = measurement - 0.01, so measurement > 0.11

    state2 = np.array([0.11, 0.0, 0.0, 0.0])  # Slightly larger error
    status, residual = fdi.check(0.01, state2, 0.0, 0.01, dynamics)

    print(f"Test with state2=[0.11, 0, 0, 0]:")
    print(f"  residual = {residual}")
    print(f"  passes test: {residual > 1.0}")

    # Let's check: error = 0.11 - 0.01 = 0.10
    # weighted = 0.10 * 10.0 = 1.0
    # But we still have the small negative errors in other components...

    state3 = np.array([0.101, 0.01, 0.01, 0.01])  # Compensate for prediction
    fdi2 = FDIsystem(
        residual_threshold=0.5,
        residual_states=[0, 1, 2, 3],
        residual_weights=[10.0, 1.0, 1.0, 1.0]
    )
    fdi2.check(0.0, state1, 0.0, 0.01, dynamics)
    status, residual = fdi2.check(0.01, state3, 0.0, 0.01, dynamics)

    print(f"Test with compensated state3=[0.101, 0.01, 0.01, 0.01]:")
    print(f"  residual = {residual}")
    print(f"  passes test: {residual > 1.0}")

if __name__ == "__main__":
    debug_weighted_residual()
    print("\n" + "="*50)
    test_cleaner_scenario()
    print("\n" + "="*50)
    test_fixed_test()
    print("\n" + "="*50)
    test_what_original_test_needed()