# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 15
# Runnable: True
# Hash: 3db3b9f4

class TestSimplifiedDynamics:
    """Test simplified double-inverted pendulum dynamics."""

    def test_initialization(self, physics_cfg):
        """Test dynamics initialization with physics configuration."""
        dynamics = SimplifiedDynamics(physics_cfg)

        assert dynamics.M == physics_cfg.M
        assert dynamics.m1 == physics_cfg.m1
        assert dynamics.m2 == physics_cfg.m2
        assert dynamics.L1 == physics_cfg.L1
        assert dynamics.L2 == physics_cfg.L2
        assert dynamics.g == physics_cfg.g

    def test_dynamics_output_shape(self, dynamics_simplified):
        """Test that dynamics returns correct output shape."""
        state = np.array([0.0, 0.0, 0.1, 0.1, 0.0, 0.0])
        control = 10.0

        state_dot = dynamics_simplified.dynamics(state, control)

        assert state_dot.shape == (6,)
        assert np.all(np.isfinite(state_dot))

    def test_equilibrium_dynamics(self, dynamics_simplified):
        """Test dynamics at equilibrium with zero control."""
        equilibrium = np.zeros(6)
        control = 0.0

        state_dot = dynamics_simplified.dynamics(equilibrium, control)

        # At equilibrium with zero control, derivatives should be near zero
        assert np.linalg.norm(state_dot) < 1e-6

    def test_energy_conservation(self, dynamics_simplified):
        """Test energy conservation for conservative dynamics."""
        from src.utils.analysis.energy import compute_total_energy

        state = np.array([0.0, 0.0, 0.1, 0.1, 0.0, 0.0])
        control = 0.0  # No external input

        # Integrate for short time
        dt = 0.01
        t_span = np.arange(0, 1.0, dt)
        states = [state]

        for _ in t_span[1:]:
            state_dot = dynamics_simplified.dynamics(states[-1], control)
            states.append(states[-1] + dt * state_dot)

        states = np.array(states)

        # Compute energy at each timestep
        energies = [compute_total_energy(s, dynamics_simplified) for s in states]

        # Energy should be approximately conserved (no friction)
        energy_drift = np.max(np.abs(np.diff(energies)))
        assert energy_drift < 0.01  # Small drift due to Euler integration