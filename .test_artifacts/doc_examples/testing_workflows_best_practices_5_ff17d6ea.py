# Example from: docs\testing\testing_workflows_best_practices.md
# Index: 5
# Runnable: True
# Hash: ff17d6ea

# Level 1: Component-level tests
def test_sliding_surface_computation():
    """Test individual sliding surface computation."""
    from src.controllers.smc.core.sliding_surface import LinearSlidingSurface

    surface = LinearSlidingSurface(gains=[5, 3, 4, 2])
    state = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])

    s = surface.compute(state)
    assert isinstance(s, float)
    assert np.isfinite(s)

# Level 2: Component integration tests
def test_sliding_surface_with_controller():
    """Test sliding surface integrated with controller."""
    from src.controllers.smc.classic_smc import ClassicalSMC

    controller = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100)

    state = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])
    result = controller.compute_control(state, {}, {})

    assert 'control' in result
    assert np.isfinite(result['control'])

# Level 3: System-level integration tests
def test_controller_with_dynamics():
    """Test controller integrated with dynamics."""
    from src.controllers.smc.classic_smc import ClassicalSMC
    from src.core.dynamics import SimplifiedDynamics

    controller = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100)
    dynamics = SimplifiedDynamics({'M': 1.0, 'm1': 0.1, 'm2': 0.1, 'L1': 0.5, 'L2': 0.5, 'g': 9.81})

    state = np.array([0.0, 0.1, 0.1, 0.0, 0.0, 0.0])

    for _ in range(100):
        result = controller.compute_control(state, {}, {})
        u = result['control']
        x_dot = dynamics.dynamics(state, u)
        state = state + 0.01 * x_dot

    assert np.linalg.norm(state) < 0.5  # Partial stabilization

# Level 4: End-to-end workflow tests
def test_complete_simulation_workflow():
    """Test complete simulation from initialization to results."""
    from src.core.simulation_runner import run_simulation

    controller = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100)

    result = run_simulation(
        controller=controller,
        duration=5.0,
        dt=0.01,
        initial_state=[0.0, 0.1, 0.1, 0.0, 0.0, 0.0]
    )

    assert 'time' in result
    assert 'states' in result
    assert len(result['time']) == len(result['states'])
    assert np.linalg.norm(result['states'][-1]) < 0.05  # Full stabilization