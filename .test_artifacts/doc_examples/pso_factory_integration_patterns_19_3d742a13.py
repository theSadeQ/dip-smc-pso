# Example from: docs\pso_factory_integration_patterns.md
# Index: 19
# Runnable: False
# Hash: 3d742a13

#!/usr/bin/env python3
"""Comparative study of different SMC controllers."""

from src.controllers.factory import create_all_smc_controllers, SMCType
import matplotlib.pyplot as plt

def comparative_controller_study():
    """Compare performance of different SMC controllers."""

    controller_types = [
        SMCType.CLASSICAL,
        SMCType.ADAPTIVE,
        SMCType.SUPER_TWISTING
    ]

    results = {}

    for controller_type in controller_types:
        print(f"Optimizing {controller_type.value}...")

        # Run PSO optimization
        best_gains, best_fitness = basic_pso_optimization(controller_type)

        # Create optimized controller
        factory = create_pso_controller_factory(controller_type)
        controller = factory(best_gains)

        # Comprehensive evaluation
        performance = evaluate_comprehensive_performance(controller)

        results[controller_type.value] = {
            'gains': best_gains,
            'fitness': best_fitness,
            'performance': performance
        }

    # Generate comparison report
    generate_comparison_report(results)
    plot_performance_comparison(results)

    return results

def plot_performance_comparison(results):
    """Plot performance comparison."""

    metrics = ['ise', 'itae', 'settling_time', 'overshoot', 'control_effort']
    controller_names = list(results.keys())

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for i, metric in enumerate(metrics):
        values = [results[name]['performance'][metric] for name in controller_names]

        axes[i].bar(controller_names, values)
        axes[i].set_title(f'{metric.upper()}')
        axes[i].set_ylabel('Value')

        # Rotate x-axis labels for readability
        plt.setp(axes[i].get_xticklabels(), rotation=45)

    plt.tight_layout()
    plt.savefig('controller_performance_comparison.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    comparative_controller_study()