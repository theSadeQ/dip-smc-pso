#=======================================================================================\\\
#================================= debug_pso_fitness.py =================================\\\
#=======================================================================================\\\

"""Debug PSO fitness calculation to identify zero cost issue."""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import load_config
from src.controllers.smc.algorithms.classical.controller import ClassicalSMC
from src.optimization.algorithms.pso_optimizer import PSOTuner


def create_debug_controller_factory():
    """Create a simple controller factory for debugging."""

    def controller_factory(gains: np.ndarray):
        """Factory function to create ClassicalSMC controllers."""
        try:
            # Load config
            config = load_config("config.yaml")

            # Create controller using backward-compatible interface
            controller = ClassicalSMC(
                gains=gains.tolist(),
                max_force=config.controllers.classical_smc.max_force,
                boundary_layer=config.controllers.classical_smc.boundary_layer,
                dt=config.controllers.classical_smc.dt
            )

            # Add dynamics model if missing
            if not hasattr(controller, 'dynamics_model') or controller.dynamics_model is None:
                print(f"Warning: Controller missing dynamics_model, adding default")
                from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics
                from src.plant.models.simplified.config import SimplifiedDIPConfig
                # Create simplified config from physics config
                physics = config.physics
                dynamics_config = SimplifiedDIPConfig(
                    cart_mass=physics.cart_mass,
                    pendulum1_mass=physics.pendulum1_mass,
                    pendulum2_mass=physics.pendulum2_mass,
                    pendulum1_length=physics.pendulum1_length,
                    pendulum2_length=physics.pendulum2_length,
                    pendulum1_com=physics.pendulum1_com,
                    pendulum2_com=physics.pendulum2_com,
                    pendulum1_inertia=physics.pendulum1_inertia,
                    pendulum2_inertia=physics.pendulum2_inertia,
                    gravity=physics.gravity,
                    cart_friction=physics.cart_friction,
                    joint1_friction=physics.joint1_friction,
                    joint2_friction=physics.joint2_friction
                )
                controller.dynamics_model = SimplifiedDIPDynamics(dynamics_config)

            return controller

        except Exception as e:
            print(f"Controller factory error: {e}")
            raise

    controller_factory.controller_type = "classical_smc"
    controller_factory.n_gains = 6

    return controller_factory


def debug_simulation_directly():
    """Debug the simulation function directly."""
    print("=== Debugging Simulation Function ===")

    try:
        from src.simulation.engines.vector_sim import simulate_system_batch

        # Create simple test particle
        factory = create_debug_controller_factory()
        test_particle = np.array([[10.0, 10.0, 5.0, 5.0, 20.0, 2.0]])

        print(f"Test particle shape: {test_particle.shape}")
        print(f"Test particle values: {test_particle}")

        # Run simulation
        result = simulate_system_batch(
            controller_factory=factory,
            particles=test_particle,
            sim_time=2.0,  # Short simulation
            dt=0.01,
            u_max=150.0
        )

        print(f"Simulation result type: {type(result)}")

        if isinstance(result, tuple):
            t, x_b, u_b, sigma_b = result
            print(f"Time shape: {t.shape if hasattr(t, 'shape') else 'scalar'}")
            print(f"State shape: {x_b.shape}")
            print(f"Control shape: {u_b.shape}")
            print(f"Sigma shape: {sigma_b.shape}")
            print(f"Final state: {x_b[0, -1, :] if x_b.size > 0 else 'empty'}")
            print(f"Final control: {u_b[0, -1] if u_b.size > 0 else 'empty'}")
            print(f"Final sigma: {sigma_b[0, -1] if sigma_b.size > 0 else 'empty'}")
        else:
            print(f"Unexpected result format: {result}")

        return True

    except Exception as e:
        print(f"Simulation debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def debug_cost_calculation():
    """Debug the cost calculation specifically."""
    print("\n=== Debugging Cost Calculation ===")

    try:
        # Create tuner
        factory = create_debug_controller_factory()
        tuner = PSOTuner(
            controller_factory=factory,
            config="config.yaml",
            seed=42
        )

        # Create sample trajectory data manually
        dt = 0.01
        steps = 100
        t = np.arange(0, steps * dt, dt)

        # Sample trajectories for 1 particle
        x_b = np.random.randn(1, len(t), 6) * 0.1  # Small random states
        u_b = np.random.randn(1, len(t)) * 10.0    # Random control
        sigma_b = np.random.randn(1, len(t)) * 0.5  # Random sliding surface

        print(f"Sample trajectory shapes:")
        print(f"  Time: {t.shape}, States: {x_b.shape}")
        print(f"  Control: {u_b.shape}, Sigma: {sigma_b.shape}")

        # Calculate cost
        cost = tuner._compute_cost_from_traj(t, x_b, u_b, sigma_b)
        print(f"Computed cost: {cost}")
        print(f"Cost shape: {cost.shape}")
        print(f"Cost finite: {np.all(np.isfinite(cost))}")
        print(f"Cost positive: {np.all(cost > 0)}")

        # Check individual cost components
        dt_arr = np.diff(t)[None, :]
        N = dt_arr.shape[1]
        time_mask = np.ones((1, N), dtype=bool)

        # State error
        ise = np.sum((x_b[:, :-1, :] ** 2 * dt_arr[:, :, None]) * time_mask[:, :, None], axis=(1, 2))
        print(f"ISE: {ise}, normalized: {tuner._normalise(ise, tuner.norm_ise)}")

        # Control effort
        u_sq = np.sum((u_b[:, :-1] ** 2 * dt_arr) * time_mask, axis=1)
        print(f"Control effort: {u_sq}, normalized: {tuner._normalise(u_sq, tuner.norm_u)}")

        # Sliding surface
        sigma_sq = np.sum((sigma_b[:, :-1] ** 2 * dt_arr) * time_mask, axis=1)
        print(f"Sigma effort: {sigma_sq}, normalized: {tuner._normalise(sigma_sq, tuner.norm_sigma)}")

        print(f"Weights: {tuner.weights}")
        print(f"Normalization constants: ISE={tuner.norm_ise}, U={tuner.norm_u}, DU={tuner.norm_du}, Sigma={tuner.norm_sigma}")

        return True

    except Exception as e:
        print(f"Cost calculation debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def debug_fitness_evaluation():
    """Debug the fitness evaluation function."""
    print("\n=== Debugging Fitness Evaluation ===")

    try:
        # Create tuner
        factory = create_debug_controller_factory()
        tuner = PSOTuner(
            controller_factory=factory,
            config="config.yaml",
            seed=42
        )

        # Create test particles
        test_particles = np.array([
            [10.0, 10.0, 5.0, 5.0, 20.0, 2.0],  # Reasonable gains
            [1.0, 1.0, 1.0, 1.0, 5.0, 0.1],     # Minimum bounds
        ])

        print(f"Test particles: {test_particles}")

        # Evaluate fitness step by step
        print("Evaluating fitness...")

        # Set up tuner internal variables
        ref_ctrl = tuner.controller_factory(test_particles[0])
        tuner._u_max = getattr(ref_ctrl, "max_force", 150.0)
        tuner._T = tuner.sim_cfg.duration

        print(f"Max force: {tuner._u_max}")
        print(f"Simulation time: {tuner._T}")
        print(f"Time step: {tuner.sim_cfg.dt}")

        # Call fitness function
        fitness_values = tuner._fitness(test_particles)

        print(f"Fitness values: {fitness_values}")
        print(f"Fitness finite: {np.all(np.isfinite(fitness_values))}")
        print(f"Fitness positive: {np.all(fitness_values > 0)}")

        return True

    except Exception as e:
        print(f"Fitness evaluation debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all debug tests."""
    print("PSO Fitness Debug Suite")
    print("=" * 50)

    tests = [
        debug_simulation_directly,
        debug_cost_calculation,
        debug_fitness_evaluation
    ]

    for test in tests:
        try:
            success = test()
            print(f"{test.__name__}: {'PASS' if success else 'FAIL'}")
        except Exception as e:
            print(f"{test.__name__}: FAIL - {e}")

    print("\nDebug completed.")


if __name__ == "__main__":
    main()