# Example from: docs\guides\how-to\testing-validation.md
# Index: 5
# Runnable: True
# Hash: 8594641f

def validate_controller(controller_name, gains):
    """
    Comprehensive controller validation.

    Returns: dict with validation results
    """
    from src.controllers import create_smc_for_pso, SMCType
    from src.core.simulation_runner import SimulationRunner
    from src.config import load_config

    results = {
        'controller': controller_name,
        'gains': gains,
        'tests_passed': [],
        'tests_failed': []
    }

    config = load_config('config.yaml')

    # Test 1: Initialization
    try:
        controller = create_smc_for_pso(
            SMCType[controller_name.upper()],
            gains=gains,
            max_force=100.0
        )
        results['tests_passed'].append('Initialization')
    except Exception as e:
        results['tests_failed'].append(f'Initialization: {e}')
        return results

    # Test 2: Equilibrium stability
    try:
        state = np.zeros(6)
        control, _, _ = controller.compute_control(state, {}, {})
        if abs(control) < 1e-3:
            results['tests_passed'].append('Equilibrium stability')
        else:
            results['tests_failed'].append(f'Equilibrium: control={control:.4f}')
    except Exception as e:
        results['tests_failed'].append(f'Equilibrium: {e}')

    # Test 3: Full simulation
    try:
        runner = SimulationRunner(config)
        result = runner.run(controller)

        if result['metrics']['settling_time'] < 10.0:
            results['tests_passed'].append('Settling time < 10s')
        else:
            results['tests_failed'].append(
                f'Settling time: {result["metrics"]["settling_time"]:.2f}s'
            )

        state_final = np.array(result['state'])
        if np.all(np.abs(state_final) < 10.0):
            results['tests_passed'].append('State remains bounded')
        else:
            results['tests_failed'].append('State diverged')

    except Exception as e:
        results['tests_failed'].append(f'Simulation: {e}')

    return results


# Run validation
validation = validate_controller('CLASSICAL', [10, 8, 15, 12, 50, 5])

print(f"\n{validation['controller']} Validation:")
print(f"  Passed: {len(validation['tests_passed'])}")
print(f"  Failed: {len(validation['tests_failed'])}")

if validation['tests_failed']:
    print("\nFailed tests:")
    for test in validation['tests_failed']:
        print(f"  - {test}")