#==========================================================================================\\\
#==================== tests/test_analysis/fault_detection/test_fdi.py ==================\\\
#==========================================================================================\\\

"""
Basic tests for the fault detection and isolation (FDI) system.

These tests exercise the ``FDIsystem`` class in isolation, without
running a full simulation.  We use simple deterministic dynamics
models so that we can predict the residual sequence exactly.  The
goals of this suite are to verify that:

* The FDI system trips only after the residual norm exceeds the
  configured threshold for a specified number of consecutive samples.
* The persistence counter resets on a good measurement and no fault
  is declared if violations are intermittent.
* No false alarms occur when all residuals remain below the threshold.

We avoid importing the full project at module import time by inserting
the project’s ``src`` directory onto ``sys.path`` before importing
``fault_detection.fdi``.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
from typing import Any

from src.analysis.fault_detection.fdi import FDIsystem, DynamicsProtocol


class ZeroDynamics:
    """A simple dynamics model that always predicts the zero state.

    The ``step`` method ignores its inputs and returns a zero state of
    appropriate dimension.  This causes the FDI residual to depend only
    on the measurement value.  Using this model ensures that the
    residual norm remains constant across successive calls when the
    measurements are constant.
    """

    def __init__(self, dim: int = 1) -> None:
        self.dim = int(dim)

    def step(self, state: npt.NDArray[np.floating], u: float, dt: float) -> npt.NDArray[np.floating]:
        """Step the zero dynamics model."""
        return np.zeros(self.dim, dtype=np.float64)


def test_fdi_trips_after_persistence() -> None:
    """FDI should trip only after the residual exceeds the threshold consecutively."""
    # Configure FDI with a low threshold and short persistence counter
    fdi = FDIsystem(residual_threshold=1.0, persistence_counter=3, residual_states=[0])
    dyn = ZeroDynamics(dim=1)

    # The first call sets the internal _last_state and returns OK with zero residual
    status, resid = fdi.check(0.0, np.array([0.0]), 0.0, 0.1, dyn)
    assert status == "OK"
    assert resid == 0.0
    assert fdi.tripped_at is None

    # Provide three measurements with a large residual norm.  Because
    # ``ZeroDynamics.step`` returns 0, the residual is simply the measurement.
    for i in range(3):
        t = (i + 1) * 0.1
        status, resid = fdi.check(t, np.array([2.0]), 0.0, 0.1, dyn)
        if i < 2:
            assert status == "OK", "FDI should not trip before persistence counter is reached"
        else:
            assert status == "FAULT", "FDI should trip on the third consecutive violation"

    # The trip time should be recorded and be >= 0.1 (first violation time)
    assert fdi.tripped_at is not None
    assert fdi.tripped_at >= 0.1


def test_fdi_resets_counter_on_good_measurement() -> None:
    """After a good measurement the violation counter should reset."""
    fdi = FDIsystem(residual_threshold=1.0, persistence_counter=3, residual_states=[0])
    dyn = ZeroDynamics(dim=1)

    # Initialize the last state
    fdi.check(0.0, np.array([0.0]), 0.0, 0.1, dyn)
    # Two consecutive violations
    fdi.check(0.1, np.array([2.0]), 0.0, 0.1, dyn)
    fdi.check(0.2, np.array([2.0]), 0.0, 0.1, dyn)
    # A good measurement resets the counter
    status, resid = fdi.check(0.3, np.array([0.0]), 0.0, 0.1, dyn)
    assert status == "OK"
    # Subsequent high residuals should count from zero again and not trip immediately
    status, resid = fdi.check(0.4, np.array([2.0]), 0.0, 0.1, dyn)
    assert status == "OK", "Counter should have been reset after the good measurement"
    assert fdi.tripped_at is None


def test_fdi_no_false_alarm() -> None:
    """When residuals stay below threshold no fault should be reported."""
    fdi = FDIsystem(residual_threshold=1.0, persistence_counter=3, residual_states=[0])
    dyn = ZeroDynamics(dim=1)
    # Initialize
    fdi.check(0.0, np.array([0.0]), 0.0, 0.1, dyn)
    # Provide small residuals; never exceed threshold
    for k in range(10):
        t = (k + 1) * 0.1
        status, resid = fdi.check(t, np.array([0.5]), 0.0, 0.1, dyn)
        assert status == "OK"
        assert resid < fdi.residual_threshold
    assert fdi.tripped_at is None


def test_fdi_dt_validation() -> None:
    """FDI.check should raise a ValueError when dt ≤ 0."""
    fdi = FDIsystem(residual_threshold=1.0, persistence_counter=1, residual_states=[0])
    dyn = ZeroDynamics(dim=1)
    # Initialise last state
    fdi.check(0.0, np.array([0.0]), 0.0, 0.1, dyn)
    import pytest
    # Zero dt
    with pytest.raises(ValueError):
        fdi.check(0.1, np.array([0.1]), 0.0, 0.0, dyn)
    # Negative dt
    with pytest.raises(ValueError):
        fdi.check(0.2, np.array([0.2]), 0.0, -0.1, dyn)


def test_residual_with_weights() -> None:
    """Test that residual weights properly amplify specific state errors."""

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

    # Create state with error that compensates for prediction and produces weighted residual > 1.0
    # Prediction will be [0.01, 0.01, 0.01, 0.01]
    # To get weighted first component > 1.0: need residual[0] > 0.1
    # So state[0] needs to be > 0.01 + 0.1 = 0.11
    state2 = np.array([0.111, 0.01, 0.01, 0.01])  # Compensated for dynamics + margin
    status, residual = fdi.check(0.01, state2, 0.0, 0.01, dynamics)

    # The weighted residual should be > 1.0
    assert residual > 1.0, f"Expected residual > 1.0, got {residual}"


def test_cusum_drift_detection() -> None:
    """Test CUSUM detection of slow drift."""

    class ConstantDynamics:
        def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
            return state  # No change prediction

    # Configure with CUSUM enabled
    fdi = FDIsystem(
        residual_threshold=1.0,  # High threshold so persistence won't trigger
        persistence_counter=100,  # Very high so it won't trigger
        cusum_enabled=True,
        cusum_threshold=2.0,
        residual_states=[0]
    )
    dynamics = ConstantDynamics()

    # Initialize
    fdi.check(0.0, np.array([0.0]), 0.0, 0.01, dynamics)

    # Simulate small drift that accumulates
    for i in range(10):
        t = (i + 1) * 0.01
        # Small consistent error above threshold
        state = np.array([0.3])  # Creates residual of 0.3, deviation = 0.3 - 1.0 = -0.7 (clipped to 0)
        status, residual = fdi.check(t, state, 0.0, 0.01, dynamics)
        if status == "FAULT":
            break
    else:
        # Try with positive drift
        fdi.reset()
        fdi.check(0.0, np.array([0.0]), 0.0, 0.01, dynamics)

        for i in range(10):
            t = (i + 1) * 0.01
            # Error above reference threshold
            state = np.array([1.5])  # Creates residual of 1.5, deviation = 1.5 - 1.0 = 0.5
            status, residual = fdi.check(t, state, 0.0, 0.01, dynamics)
            if status == "FAULT":
                break

        assert status == "FAULT", "CUSUM should detect slow drift"


def test_cusum_reset_behavior() -> None:
    """Test that CUSUM accumulates properly and can be reset."""

    class ConstantDynamics:
        def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
            return state  # No change prediction

    # Configure with CUSUM enabled
    fdi = FDIsystem(
        residual_threshold=1.0,
        cusum_enabled=True,
        cusum_threshold=5.0,
        residual_states=[0]
    )
    dynamics = ConstantDynamics()

    # Initialize
    fdi.check(0.0, np.array([0.0]), 0.0, 0.01, dynamics)

    # Check that CUSUM starts at 0
    assert fdi._cusum == 0.0, f"CUSUM should start at 0.0, got {fdi._cusum}"

    # Add some positive deviation
    state = np.array([2.0])  # Creates residual of 2.0, deviation = 2.0 - 1.0 = 1.0
    fdi.check(0.01, state, 0.0, 0.01, dynamics)

    # CUSUM should accumulate
    assert fdi._cusum > 0.0, f"CUSUM should accumulate, got {fdi._cusum}"
    first_cusum = fdi._cusum

    # Add another positive deviation
    fdi.check(0.02, state, 0.0, 0.01, dynamics)

    # CUSUM should continue to accumulate
    assert fdi._cusum > first_cusum, f"CUSUM should continue accumulating, got {fdi._cusum} vs {first_cusum}"

    # Reset and verify
    fdi.reset()
    assert fdi._cusum == 0.0, f"CUSUM should reset to 0.0, got {fdi._cusum}"


def test_history_recording() -> None:
    """Test that history properly records all measurements."""

    class ConstantDynamics:
        def step(self, state: np.ndarray, u: float, dt: float) -> np.ndarray:
            return state  # No change prediction

    fdi = FDIsystem(residual_threshold=1.0, residual_states=[0])
    dynamics = ConstantDynamics()

    # Check multiple measurements
    for i in range(10):
        t = i * 0.01
        state = np.array([0.1 * i])
        fdi.check(t, state, 0.0, 0.01, dynamics)

    # Should have 10 entries (including the first one)
    assert len(fdi.times) == 10, f"Expected 10 time entries, got {len(fdi.times)}"
    assert len(fdi.residuals) == 10, f"Expected 10 residual entries, got {len(fdi.residuals)}"

    # First entry should be at time 0 with residual 0
    assert fdi.times[0] == 0.0, f"First time should be 0.0, got {fdi.times[0]}"
    assert fdi.residuals[0] == 0.0, f"First residual should be 0.0, got {fdi.residuals[0]}"