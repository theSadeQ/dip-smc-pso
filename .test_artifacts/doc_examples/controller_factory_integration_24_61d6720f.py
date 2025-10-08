# Example from: docs\technical\controller_factory_integration.md
# Index: 24
# Runnable: False
# Hash: 61d6720f

# example-metadata:
# runnable: false

def analyze_controller_robustness(controller_type, gains, uncertainty_bounds):
    """Analyze controller robustness to parameter uncertainties."""

    # Create nominal controller
    controller = create_controller(controller_type, gains=gains)

    # Monte Carlo robustness analysis
    n_samples = 1000
    stability_count = 0

    for _ in range(n_samples):
        # Generate random uncertainties
        uncertainties = generate_random_uncertainties(uncertainty_bounds)

        # Test stability with uncertainties
        if test_stability_with_uncertainties(controller, uncertainties):
            stability_count += 1

    robustness_probability = stability_count / n_samples
    return robustness_probability