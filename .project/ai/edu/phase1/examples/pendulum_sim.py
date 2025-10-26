"""
pendulum_sim.py - Simple Pendulum Simulation

This script simulates a simple pendulum using numerical integration.
Demonstrates:
- Differential equations
- Numerical integration (Euler method)
- Physics simulation
- Data visualization

Physics:
    d²θ/dt² = -(g/L) * sin(θ) - b * dθ/dt

where:
    θ = angle (radians)
    g = gravity (9.81 m/s²)
    L = pendulum length (m)
    b = damping coefficient

Requirements: pip install numpy matplotlib

Run: python pendulum_sim.py
"""

import numpy as np
import matplotlib.pyplot as plt


class SimplePendulum:
    """
    Simple pendulum simulator.

    Attributes:
        L: Length (m)
        g: Gravity (m/s²)
        b: Damping coefficient
    """

    def __init__(self, length=1.0, gravity=9.81, damping=0.1):
        """
        Initialize pendulum.

        Args:
            length: Pendulum length in meters
            gravity: Gravitational acceleration (m/s²)
            damping: Damping coefficient (higher = more damping)
        """
        self.L = length
        self.g = gravity
        self.b = damping

    def derivatives(self, state):
        """
        Calculate derivatives for the pendulum system.

        Args:
            state: [theta, omega] where omega = dθ/dt

        Returns:
            [dθ/dt, dω/dt] = [omega, alpha]
        """
        theta, omega = state

        # Angular acceleration: α = -(g/L)*sin(θ) - b*ω
        alpha = -(self.g / self.L) * np.sin(theta) - self.b * omega

        return np.array([omega, alpha])

    def simulate(self, theta0, omega0, t_max, dt):
        """
        Simulate pendulum motion using Euler integration.

        Args:
            theta0: Initial angle (radians)
            omega0: Initial angular velocity (rad/s)
            t_max: Simulation duration (s)
            dt: Time step (s)

        Returns:
            t: Time array
            theta: Angle array
            omega: Angular velocity array
        """
        # Initialize arrays
        n_steps = int(t_max / dt)
        t = np.linspace(0, t_max, n_steps)
        theta = np.zeros(n_steps)
        omega = np.zeros(n_steps)

        # Set initial conditions
        theta[0] = theta0
        omega[0] = omega0

        # Euler integration
        for i in range(n_steps - 1):
            state = np.array([theta[i], omega[i]])
            derivatives = self.derivatives(state)

            theta[i + 1] = theta[i] + derivatives[0] * dt
            omega[i + 1] = omega[i] + derivatives[1] * dt

        return t, theta, omega

    def calculate_energy(self, theta, omega):
        """
        Calculate total mechanical energy.

        Args:
            theta: Angle (rad)
            omega: Angular velocity (rad/s)

        Returns:
            Total energy (J)
        """
        # Mass = 1 kg for simplicity
        m = 1.0
        I = m * self.L**2

        # Kinetic energy: KE = (1/2) * I * ω²
        KE = 0.5 * I * omega**2

        # Potential energy: PE = m * g * h = m * g * L * (1 - cos(θ))
        PE = m * self.g * self.L * (1 - np.cos(theta))

        return KE + PE


def plot_results(t, theta, omega, energy):
    """
    Plot simulation results.

    Args:
        t: Time array
        theta: Angle array
        omega: Angular velocity array
        energy: Energy array
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))

    # Plot 1: Angle vs Time
    axes[0].plot(t, np.degrees(theta), 'b-', linewidth=2)
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Angle (degrees)")
    axes[0].set_title("Pendulum Angle Over Time")
    axes[0].grid(True)

    # Plot 2: Angular Velocity vs Time
    axes[1].plot(t, omega, 'r-', linewidth=2)
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Angular Velocity (rad/s)")
    axes[1].set_title("Angular Velocity Over Time")
    axes[1].grid(True)

    # Plot 3: Energy vs Time
    axes[2].plot(t, energy, 'g-', linewidth=2)
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("Energy (J)")
    axes[2].set_title("Total Mechanical Energy (should decrease with damping)")
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()


def plot_phase_space(theta, omega):
    """
    Plot phase space diagram.

    Args:
        theta: Angle array
        omega: Angular velocity array
    """
    plt.figure(figsize=(8, 8))
    plt.plot(theta, omega, 'b-', linewidth=1.5)
    plt.plot(theta[0], omega[0], 'go', markersize=10, label='Start')
    plt.plot(theta[-1], omega[-1], 'ro', markersize=10, label='End')
    plt.xlabel("Angle θ (rad)")
    plt.ylabel("Angular Velocity ω (rad/s)")
    plt.title("Phase Space Portrait")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()


def main():
    """Run pendulum simulations."""
    print("=" * 60)
    print("Simple Pendulum Simulation")
    print("=" * 60)

    # Create pendulum
    pendulum = SimplePendulum(length=1.0, gravity=9.81, damping=0.1)

    # Simulation parameters
    theta0 = np.radians(30)  # Initial angle: 30 degrees
    omega0 = 0.0              # Initial angular velocity: 0 rad/s
    t_max = 20.0              # Simulate for 20 seconds
    dt = 0.01                 # Time step: 0.01 seconds

    print(f"\nPendulum Parameters:")
    print(f"  Length: {pendulum.L} m")
    print(f"  Gravity: {pendulum.g} m/s²")
    print(f"  Damping: {pendulum.b}")

    print(f"\nInitial Conditions:")
    print(f"  Angle: {np.degrees(theta0):.1f} degrees")
    print(f"  Angular velocity: {omega0} rad/s")

    print(f"\nSimulation Settings:")
    print(f"  Duration: {t_max} s")
    print(f"  Time step: {dt} s")

    # Run simulation
    print("\nRunning simulation...")
    t, theta, omega = pendulum.simulate(theta0, omega0, t_max, dt)

    # Calculate energy
    energy = pendulum.calculate_energy(theta, omega)

    # Print results
    print(f"\nResults:")
    print(f"  Final angle: {np.degrees(theta[-1]):.2f} degrees")
    print(f"  Final angular velocity: {omega[-1]:.4f} rad/s")
    print(f"  Initial energy: {energy[0]:.4f} J")
    print(f"  Final energy: {energy[-1]:.4f} J")
    print(f"  Energy lost to damping: {energy[0] - energy[-1]:.4f} J")

    # Calculate period (approximate)
    # Find zero crossings to estimate period
    crossings = []
    for i in range(len(theta) - 1):
        if theta[i] > 0 and theta[i + 1] <= 0:
            crossings.append(t[i])

    if len(crossings) >= 2:
        measured_period = np.mean(np.diff(crossings))
        theoretical_period = 2 * np.pi * np.sqrt(pendulum.L / pendulum.g)
        print(f"\nPeriod Analysis:")
        print(f"  Measured period: {measured_period:.3f} s")
        print(f"  Theoretical (small angle): {theoretical_period:.3f} s")
        print(f"  Difference: {abs(measured_period - theoretical_period):.3f} s")

    # Plot results
    print("\nGenerating plots...")
    plot_results(t, theta, omega, energy)
    plot_phase_space(theta, omega)

    print("\n" + "=" * 60)
    print("Simulation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
