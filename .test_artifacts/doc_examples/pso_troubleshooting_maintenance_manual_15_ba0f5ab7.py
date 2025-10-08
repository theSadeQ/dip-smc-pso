# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 15
# Runnable: False
# Hash: ba0f5ab7

class AdaptiveSimulation:
    """Simulation with adaptive time step for efficiency."""

    def __init__(self, base_dt=0.001, max_dt=0.01, error_tolerance=1e-6):
        self.base_dt = base_dt
        self.max_dt = max_dt
        self.error_tolerance = error_tolerance

    def simulate_with_adaptive_timestep(self, controller, initial_state, duration):
        """Simulate with adaptive time step control."""

        t = 0
        state = initial_state.copy()
        dt = self.base_dt

        trajectory = {'t': [0], 'x': [state.copy()], 'u': [], 'dt': []}

        while t < duration:
            # Compute control
            u = controller.compute_control(state, dt=dt)

            # Try two time steps: dt and dt/2
            state_full = self._integrate_step(state, u, dt)
            state_half1 = self._integrate_step(state, u, dt/2)
            state_half2 = self._integrate_step(state_half1, u, dt/2)

            # Estimate error
            error = np.linalg.norm(state_full - state_half2)

            if error < self.error_tolerance:
                # Accept step and possibly increase dt
                state = state_full
                t += dt
                trajectory['t'].append(t)
                trajectory['x'].append(state.copy())
                trajectory['u'].append(u)
                trajectory['dt'].append(dt)

                # Increase time step if error is very small
                if error < self.error_tolerance / 4:
                    dt = min(self.max_dt, dt * 1.2)

            else:
                # Reduce time step and retry
                dt = max(self.base_dt, dt * 0.5)

        return trajectory

    def _integrate_step(self, state, u, dt):
        """Single integration step (placeholder)."""
        # Implement actual dynamics integration
        # This is controller and system dependent
        pass