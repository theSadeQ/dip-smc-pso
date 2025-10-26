"""
simulation_template.py - Physics Simulation Template

Template for creating physics simulations with numerical integration.
Demonstrates a generic dynamical system structure.

Author: [Your Name]
Date: [Date]
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


class Simulation:
    """
    Base class for physics simulations.

    Inherit from this class and override the derivatives() method
    to implement your specific system dynamics.
    """

    def __init__(self, **params):
        """
        Initialize simulation with parameters.

        Args:
            **params: Keyword arguments for system parameters
        """
        self.params = params

    def derivatives(self, t, state):
        """
        Calculate time derivatives of the state vector.

        OVERRIDE THIS METHOD for your specific system.

        Args:
            t: Current time
            state: Current state vector

        Returns:
            State derivatives (dstate/dt)
        """
        raise NotImplementedError("Override this method in your subclass")

    def simulate(self, initial_state, t_span, dt):
        """
        Run the simulation.

        Args:
            initial_state: Initial state vector
            t_span: (t_start, t_end) tuple
            dt: Time step for output

        Returns:
            t: Time array
            states: State history (shape: [n_steps, n_states])
        """
        t_eval = np.arange(t_span[0], t_span[1], dt)

        solution = solve_ivp(
            self.derivatives,
            t_span,
            initial_state,
            t_eval=t_eval,
            method='RK45'
        )

        return solution.t, solution.y.T  # Transpose for easier indexing

    def plot_results(self, t, states):
        """
        Plot simulation results.

        OVERRIDE OR EXTEND THIS METHOD for custom plots.

        Args:
            t: Time array
            states: State history
        """
        n_states = states.shape[1]

        fig, axes = plt.subplots(n_states, 1, figsize=(10, 3 * n_states))

        if n_states == 1:
            axes = [axes]

        for i, ax in enumerate(axes):
            ax.plot(t, states[:, i], linewidth=2)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel(f"State {i}")
            ax.set_title(f"State Variable {i}")
            ax.grid(True)

        plt.tight_layout()
        plt.show()


# Example: Simple Harmonic Oscillator
class HarmonicOscillator(Simulation):
    """
    Example: Mass-spring system.

    Equation: d²x/dt² = -(k/m) * x
    State: [x, v] where v = dx/dt
    """

    def __init__(self, mass=1.0, spring_constant=10.0):
        """
        Initialize oscillator.

        Args:
            mass: Mass (kg)
            spring_constant: Spring constant k (N/m)
        """
        super().__init__(mass=mass, k=spring_constant)

    def derivatives(self, t, state):
        """Calculate derivatives for harmonic oscillator."""
        x, v = state
        m = self.params['mass']
        k = self.params['k']

        # dx/dt = v
        # dv/dt = -(k/m) * x
        return [v, -(k / m) * x]

    def plot_results(self, t, states):
        """Custom plot for oscillator."""
        x = states[:, 0]
        v = states[:, 1]

        fig, axes = plt.subplots(2, 1, figsize=(10, 8))

        # Position vs time
        axes[0].plot(t, x, 'b-', linewidth=2)
        axes[0].set_xlabel("Time (s)")
        axes[0].set_ylabel("Position (m)")
        axes[0].set_title("Harmonic Oscillator: Position")
        axes[0].grid(True)

        # Phase space
        axes[1].plot(x, v, 'r-', linewidth=1.5)
        axes[1].plot(x[0], v[0], 'go', markersize=10, label='Start')
        axes[1].plot(x[-1], v[-1], 'ro', markersize=10, label='End')
        axes[1].set_xlabel("Position (m)")
        axes[1].set_ylabel("Velocity (m/s)")
        axes[1].set_title("Phase Space")
        axes[1].grid(True)
        axes[1].legend()
        axes[1].axis('equal')

        plt.tight_layout()
        plt.show()


def main():
    """Run example simulation."""
    print("=" * 60)
    print("Simulation Template Example: Harmonic Oscillator")
    print("=" * 60)

    # Create simulation
    sim = HarmonicOscillator(mass=1.0, spring_constant=10.0)

    # Initial conditions: [position, velocity]
    initial_state = [1.0, 0.0]

    # Time span
    t_span = (0, 10)
    dt = 0.01

    print("\nRunning simulation...")
    t, states = sim.simulate(initial_state, t_span, dt)

    print(f"Simulation complete!")
    print(f"  Time steps: {len(t)}")
    print(f"  Initial position: {states[0, 0]:.3f} m")
    print(f"  Final position: {states[-1, 0]:.3f} m")

    # Plot
    print("\nGenerating plots...")
    sim.plot_results(t, states)


if __name__ == "__main__":
    main()


"""
TO USE THIS TEMPLATE:

1. Create a new class inheriting from Simulation
2. Override derivatives() with your system's equations
3. (Optional) Override plot_results() for custom visualization
4. Instantiate your class and call simulate()

Example for a pendulum:

class Pendulum(Simulation):
    def __init__(self, length=1.0, gravity=9.81):
        super().__init__(L=length, g=gravity)

    def derivatives(self, t, state):
        theta, omega = state
        L = self.params['L']
        g = self.params['g']

        # dtheta/dt = omega
        # domega/dt = -(g/L) * sin(theta)
        return [omega, -(g / L) * np.sin(theta)]
"""
