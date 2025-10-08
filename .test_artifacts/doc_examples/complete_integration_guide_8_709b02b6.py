# Example from: docs\workflows\complete_integration_guide.md
# Index: 8
# Runnable: True
# Hash: 709b02b6

# scripts/detailed_controller_comparison.py
from src.utils.comparison import ControllerComparator

def comprehensive_comparison():
    """Perform comprehensive controller comparison."""

    # Controllers to compare
    controllers_config = {
        'classical_smc': {
            'gains': [10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
            'color': 'blue',
            'label': 'Classical SMC'
        },
        'adaptive_smc': {
            'gains': [10.0, 8.0, 15.0, 12.0, 0.5],
            'color': 'green',
            'label': 'Adaptive SMC'
        },
        'sta_smc': {
            'gains': [25.0, 10.0, 15.0, 12.0, 20.0, 15.0],
            'color': 'red',
            'label': 'STA SMC'
        },
        'hybrid_adaptive_sta_smc': {
            'gains': [77.6216, 44.449, 17.3134, 14.25],
            'color': 'purple',
            'label': 'Hybrid SMC'
        }
    }

    # Test scenarios
    test_scenarios = [
        {'name': 'nominal', 'disturbance': None, 'uncertainty': 0.0},
        {'name': 'disturbance', 'disturbance': 'step_10N', 'uncertainty': 0.0},
        {'name': 'uncertainty', 'disturbance': None, 'uncertainty': 0.2},
        {'name': 'combined', 'disturbance': 'sine_5N_1Hz', 'uncertainty': 0.15}
    ]

    comparator = ControllerComparator()

    for scenario in test_scenarios:
        print(f"\n📊 Testing scenario: {scenario['name']}")

        results = comparator.compare_controllers(
            controllers_config=controllers_config,
            scenario=scenario,
            duration=10.0,
            monte_carlo_runs=25
        )

        # Generate scenario report
        comparator.generate_scenario_report(
            results=results,
            scenario=scenario,
            output_file=f"comparison_{scenario['name']}.pdf"
        )

    # Generate overall comparison
    comparator.generate_master_comparison(
        output_file="master_controller_comparison.pdf"
    )

if __name__ == "__main__":
    comprehensive_comparison()