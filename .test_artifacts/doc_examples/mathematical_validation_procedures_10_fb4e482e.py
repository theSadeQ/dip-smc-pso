# Example from: docs\mathematical_validation_procedures.md
# Index: 10
# Runnable: True
# Hash: fb4e482e

from hypothesis import given, strategies as st, assume
import hypothesis.extra.numpy as hnp

@given(
    state=hnp.arrays(dtype=np.float64, shape=(6,), elements=st.floats(-10.0, 10.0, allow_nan=False)),
    gains=hnp.arrays(dtype=np.float64, shape=(6,), elements=st.floats(0.1, 100.0))
)
def test_lyapunov_stability_property(state: np.ndarray, gains: np.ndarray):
    """
    Property-based test for Lyapunov stability condition.

    Mathematical Property: V̇(s) = s·ṡ < 0 for all s ≠ 0
    """
    # Assume physical constraints
    assume(all(g > 0 for g in gains))  # Positive gains required
    assume(np.linalg.norm(state) < 5.0)  # Reasonable state magnitude

    # Create controller with given gains
    controller = ClassicalSMC(gains=gains.tolist())
    target = np.zeros(6)

    # Compute sliding surface
    sliding_surface = controller.compute_sliding_surface(state, target)

    # Skip if on sliding surface
    assume(abs(sliding_surface) > 1e-6)

    # Compute surface derivative
    surface_derivative = controller.compute_surface_derivative(state, target)

    # Lyapunov stability condition
    lyapunov_derivative = sliding_surface * surface_derivative

    # Mathematical property: V̇ < 0 for s ≠ 0
    assert lyapunov_derivative < 0, f"Lyapunov condition violated: V̇ = {lyapunov_derivative}"

@given(
    bounds=st.lists(
        st.tuples(st.floats(0.1, 10.0), st.floats(10.1, 100.0)),
        min_size=4, max_size=8
    ),
    c1=st.floats(0.1, 2.0),
    c2=st.floats(0.1, 2.0)
)
def test_pso_convergence_property(bounds: List[Tuple[float, float]], c1: float, c2: float):
    """
    Property-based test for PSO convergence conditions.

    Mathematical Property: φ = c1 + c2 > 4 ensures convergence
    """
    phi = c1 + c2
    assume(phi > 4.0)  # Convergence condition

    # Calculate constriction factor
    chi = 2 / abs(2 - phi - np.sqrt(phi**2 - 4*phi))

    # Constriction factor should be positive and less than 1
    assert 0 < chi < 1, f"Invalid constriction factor: χ = {chi}"

    # Test PSO with these parameters
    pso = PSOOptimizer(c1=c1, c2=c2, w=chi)

    # Use simple quadratic test function
    def quadratic_function(x):
        return np.sum(x**2)

    result = pso.optimize(quadratic_function, bounds, max_iterations=50)

    # Should converge to approximately zero for quadratic function
    assert result.best_cost < 1e-2, f"PSO failed to converge: final cost = {result.best_cost}"

@given(
    dt=st.floats(1e-4, 1e-2),
    simulation_time=st.floats(1.0, 10.0)
)
def test_numerical_integration_energy_conservation(dt: float, simulation_time: float):
    """
    Property-based test for energy conservation in numerical integration.

    Mathematical Property: E(t) = constant for Hamiltonian systems
    """
    assume(simulation_time / dt < 10000)  # Reasonable number of steps

    # Create conservative test system (simple pendulum)
    def pendulum_dynamics(t, state):
        theta, theta_dot = state
        g, L = 9.81, 1.0
        return np.array([theta_dot, -(g/L) * np.sin(theta)])

    # Initial condition
    initial_state = np.array([0.1, 0.0])  # Small angle, no initial velocity

    # Integrate using RK4
    integrator = RK4Integrator()
    t, states = integrator.integrate(
        dynamics=pendulum_dynamics,
        initial_state=initial_state,
        time_span=(0, simulation_time),
        dt=dt
    )

    # Calculate energy at each time step
    g, L = 9.81, 1.0
    energies = []

    for state in states:
        theta, theta_dot = state
        kinetic = 0.5 * theta_dot**2
        potential = g/L * (1 - np.cos(theta))
        total_energy = kinetic + potential
        energies.append(total_energy)

    energies = np.array(energies)
    initial_energy = energies[0]

    # Energy should be conserved (within numerical tolerance)
    max_energy_error = np.max(np.abs(energies - initial_energy))
    relative_energy_error = max_energy_error / initial_energy

    # Energy conservation tolerance depends on dt and simulation time
    tolerance = min(1e-6, dt**2 * simulation_time * 100)

    assert relative_energy_error < tolerance, f"Energy not conserved: relative error = {relative_energy_error}"