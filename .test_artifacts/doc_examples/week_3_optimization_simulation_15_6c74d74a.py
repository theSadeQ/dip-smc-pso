# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 15
# Runnable: False
# Hash: 6c74d74a

def run(self, controller, dynamics, duration, dt):
    # Initialize state
    x = self.initial_state
    t = 0.0
    history = {'t': [], 'x': [], 'u': []}

    while t < duration:
        # Compute control
        u = controller.compute_control(x, history)

        # Integrate dynamics
        x_next = self.integrator.step(x, u, dynamics, dt)

        # Safety checks
        if self.check_divergence(x_next):
            raise SimulationDivergenceError()

        # Record history
        history['t'].append(t)
        history['x'].append(x)
        history['u'].append(u)

        # Update state
        x = x_next
        t += dt

    return SimulationResult(history)