# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 19
# Runnable: True
# Hash: 72a13b30

def validate_emergency_recovery():
    """Validate system after emergency recovery."""

    print("🔍 VALIDATING EMERGENCY RECOVERY")
    print("=" * 40)

    validation_results = {
        'configuration_valid': False,
        'controllers_functional': False,
        'pso_engine_operational': False,
        'simulation_working': False,
        'overall_success': False
    }

    # Test 1: Configuration validation
    try:
        from src.config import load_config
        config = load_config('config.yaml')
        validation_results['configuration_valid'] = True
        print("✅ Configuration loads successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")

    # Test 2: Controller factory
    try:
        from src.controllers.factory import ControllerFactory
        import numpy as np

        test_gains = np.array([5.0, 3.0, 7.0, 2.0, 25.0, 1.0])
        controller = ControllerFactory.create_controller('classical_smc', test_gains)

        test_state = np.zeros(6)
        control = controller.compute_control(test_state)

        if np.isfinite(control):
            validation_results['controllers_functional'] = True
            print("✅ Controller factory operational")
        else:
            print("❌ Controller produces invalid output")

    except Exception as e:
        print(f"❌ Controller factory error: {e}")

    # Test 3: PSO engine
    try:
        from src.optimization.algorithms.pso_optimizer import PSOTuner

        def test_factory(gains):
            return ControllerFactory.create_controller('classical_smc', gains)

        pso_tuner = PSOTuner(test_factory, config, seed=42)

        # Quick test optimization
        test_bounds = (
            np.array([1.0, 1.0, 1.0, 1.0, 1.0, 0.1]),
            np.array([10.0, 10.0, 10.0, 10.0, 50.0, 5.0])
        )

        results = pso_tuner.optimize(
            bounds=test_bounds,
            n_particles=5,
            n_iterations=3
        )

        if results.get('success', False):
            validation_results['pso_engine_operational'] = True
            print("✅ PSO engine operational")
        else:
            print("❌ PSO engine test failed")

    except Exception as e:
        print(f"❌ PSO engine error: {e}")

    # Test 4: Simulation engine
    try:
        from src.simulation.engines.vector_sim import simulate_system_batch

        test_particles = np.array([[5.0, 3.0, 7.0, 2.0, 25.0, 1.0]])

        result = simulate_system_batch(
            controller_factory=test_factory,
            particles=test_particles,
            sim_time=0.5,
            dt=0.01,
            u_max=150.0
        )

        if result is not None:
            validation_results['simulation_working'] = True
            print("✅ Simulation engine operational")
        else:
            print("❌ Simulation engine test failed")

    except Exception as e:
        print(f"❌ Simulation engine error: {e}")

    # Overall assessment
    success_count = sum(validation_results.values())
    total_tests = len(validation_results) - 1  # Exclude overall_success

    if success_count == total_tests:
        validation_results['overall_success'] = True
        print("\n🎉 RECOVERY VALIDATION SUCCESSFUL")
        print("System is ready for normal operation")
    else:
        print(f"\n❌ RECOVERY VALIDATION FAILED")
        print(f"Only {success_count}/{total_tests} tests passed")
        print("Manual intervention required")

    return validation_results

# Run validation
if __name__ == "__main__":
    results = validate_emergency_recovery()
    exit(0 if results['overall_success'] else 1)