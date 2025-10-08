# Example from: docs\reports\pso_code_quality_beautification_assessment.md
# Index: 4
# Runnable: False
# Hash: fff4f998

# example-metadata:
# runnable: false

"""Compute sliding mode control output for double-inverted pendulum.

Args:
    state: 6-element state vector [x, θ1, θ2, ẋ, θ̇1, θ̇2]
    last_control: Previous control input for continuity
    history: Control computation history for adaptive algorithms

Returns:
    Control force in Newtons, bounded by actuator limits

Raises:
    ValueError: If state vector has incorrect dimensions

Example:
    >>> controller = ClassicalSMC(gains=[10, 5, 8, 3, 15, 2])
    >>> state = np.array([0.1, 0.05, 0.02, 0.0, 0.0, 0.0])
    >>> u = controller.compute_control(state, 0.0, {})
    >>> assert -100 <= u <= 100  # Within actuator limits
"""