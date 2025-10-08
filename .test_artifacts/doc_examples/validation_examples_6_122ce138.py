# Example from: docs\validation\validation_examples.md
# Index: 6
# Runnable: False
# Hash: 122ce138

# example-metadata:
# runnable: false

"""
Cross-Validation for PSO Hyperparameter Selection
==================================================

This script uses Monte Carlo cross-validation to select PSO hyperparameters
that produce controller gains with best generalization performance.
"""

import numpy as np
from typing import Dict, Any, Callable
from src.analysis.validation.cross_validation import CrossValidationConfig, CrossValidator
from src.optimization.algorithms.pso_swarm import PSOSwarm  # Example PSO
from src.controllers.smc_classical import ClassicalSMC

# Random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def optimize_controller_with_pso(pso_config: Dict[str, Any],
                                 training_scenarios: np.ndarray) -> Dict[str, float]:
    """
    Optimize controller gains using PSO with given hyperparameters.

    Parameters
    ----------
    pso_config : dict
        PSO hyperparameters: {'pop_size': int, 'w': float, 'c1': float, 'c2': float}
    training_scenarios : np.ndarray
        Training scenarios for optimization

    Returns
    -------
    dict
        Optimized controller gains
    """
    # Extract PSO hyperparameters
    pop_size = pso_config.get('pop_size', 30)
    w = pso_config.get('w', 0.7)
    c1 = pso_config.get('c1', 1.5)
    c2 = pso_config.get('c2', 1.5)

    # Define search space for controller gains
    # [lambda1, lambda2, eta1, eta2, k, phi]
    bounds = np.array([
        [5.0, 20.0],    # lambda1
        [5.0, 20.0],    # lambda2
        [10.0, 30.0],   # eta1
        [10.0, 30.0],   # eta2
        [30.0, 70.0],   # k
        [1.0, 10.0]     # phi (boundary layer)
    ])

    # Create PSO optimizer
    pso = PSOSwarm(
        pop_size=pop_size,
        dim=len(bounds),
        bounds=bounds,
        w=w,
        c1=c1,
        c2=c2,
        max_iter=50  # Limited iterations for CV efficiency
    )

    # Define objective function (simplified)
    def objective(gains):
        """Objective: minimize average settling time on training scenarios."""
        total_cost = 0.0
        for scenario in training_scenarios:
            # Simulate controller with these gains
            controller = ClassicalSMC(gains=gains)
            # ... simulate and compute settling time ...
            # (Simplified - in practice would run full simulation)
            settling_time = 2.0 + 0.5 * np.random.randn()  # Placeholder
            total_cost += settling_time
        return total_cost / len(training_scenarios)

    # Run PSO optimization
    best_gains, best_cost = pso.optimize(objective)

    return {
        'lambda1': best_gains[0],
        'lambda2': best_gains[1],
        'eta1': best_gains[2],
        'eta2': best_gains[3],
        'k': best_gains[4],
        'phi': best_gains[5]
    }


def evaluate_controller_performance(controller_gains: Dict[str, float],
                                   test_scenarios: np.ndarray) -> float:
    """
    Evaluate controller on test scenarios.

    Parameters
    ----------
    controller_gains : dict
        Controller gains to evaluate
    test_scenarios : np.ndarray
        Test scenarios

    Returns
    -------
    float
        Average performance score (negative MSE for minimization)
    """
    # Create controller with optimized gains
    gains = [controller_gains['lambda1'], controller_gains['lambda2'],
             controller_gains['eta1'], controller_gains['eta2'],
             controller_gains['k'], controller_gains['phi']]

    controller = ClassicalSMC(gains=gains)

    # Evaluate on test scenarios
    total_performance = 0.0
    for scenario in test_scenarios:
        # Simulate and compute performance
        # (Simplified - in practice would run full simulation)
        settling_time = 2.0 + 0.3 * np.random.randn()  # Placeholder
        total_performance -= settling_time  # Negative for minimization

    return total_performance / len(test_scenarios)


class PSO_CV_Predictor:
    """Wrapper for PSO hyperparameter configuration as a 'model' for CV."""

    def __init__(self, pso_config: Dict[str, Any]):
        self.pso_config = pso_config
        self.controller_gains = None

    def fit(self, X_train, y_train):
        """Train: optimize controller with this PSO config."""
        # X_train contains training scenarios
        self.controller_gains = optimize_controller_with_pso(
            self.pso_config,
            X_train
        )
        return self

    def predict(self, X_test):
        """Predict: evaluate optimized controller on test scenarios."""
        if self.controller_gains is None:
            raise ValueError("Must fit before predict")

        # Evaluate on each test scenario
        predictions = []
        for scenario in X_test:
            # Return predicted performance
            score = evaluate_controller_performance(
                self.controller_gains,
                scenario.reshape(1, -1)
            )
            predictions.append(score)

        return np.array(predictions)


def main():
    """Main cross-validation script."""

    print("=" * 70)
    print("PSO Hyperparameter Selection via Cross-Validation")
    print("=" * 70)

    # Generate synthetic scenario data (in practice, use real scenarios)
    # Each scenario is a vector of initial conditions and parameters
    n_scenarios = 100
    scenario_dim = 10  # 10 features per scenario
    scenarios = np.random.randn(n_scenarios, scenario_dim)

    # Define PSO hyperparameter configurations to compare
    pso_configs = [
        {'name': 'Small-Explorative', 'pop_size': 20, 'w': 0.9, 'c1': 2.0, 'c2': 1.0},
        {'name': 'Standard', 'pop_size': 30, 'w': 0.7, 'c1': 1.5, 'c2': 1.5},
        {'name': 'Large-Exploitative', 'pop_size': 50, 'w': 0.4, 'c1': 1.0, 'c2': 2.0},
        {'name': 'Adaptive', 'pop_size': 30, 'w': 0.5, 'c1': 1.8, 'c2': 1.2}
    ]

    print(f"\n1. Configuration:")
    print(f"   Number of scenarios: {n_scenarios}")
    print(f"   PSO configurations to compare: {len(pso_configs)}")
    for i, cfg in enumerate(pso_configs, 1):
        print(f"   {i}. {cfg['name']}: pop={cfg['pop_size']}, w={cfg['w']}, "
              f"c1={cfg['c1']}, c2={cfg['c2']}")

    # Configure cross-validation
    cv_config = CrossValidationConfig(
        cv_method="monte_carlo",  # Random train-test splits
        n_repetitions=50,         # 50 random splits for robust estimate
        test_ratio=0.2,           # 80% train, 20% test
        random_state=RANDOM_SEED,
        paired_tests=True,        # Same splits for all configs (paired comparison)
        significance_level=0.05
    )

    validator = CrossValidator(cv_config)

    print(f"\n2. Cross-Validation Setup:")
    print(f"   Method: {cv_config.cv_method}")
    print(f"   Repetitions: {cv_config.n_repetitions}")
    print(f"   Train-test split: {1-cv_config.test_ratio:.0%}-{cv_config.test_ratio:.0%}")

    # Create model objects
    models = [PSO_CV_Predictor(cfg) for cfg in pso_configs]

    print(f"\n3. Running cross-validation...")
    print(f"   (This may take several minutes...)")

    # Prepare dummy targets (CV framework expects targets)
    # In practice, these would be performance scores
    y = np.random.randn(n_scenarios)  # Placeholder

    # Run cross-validation
    result = validator.validate(
        data=scenarios,
        models=models,
        target_variable=None,  # Will use y directly
        feature_variables=None  # Will use all columns
    )

    # Extract results
    if result.status.name == 'SUCCESS':
        print("\n4. Results:")
        print("-" * 70)

        # Monte Carlo CV results
        if 'monte_carlo_validation' in result.data:
            mc_cv = result.data['monte_carlo_validation']

            print("\n   Cross-Validation Scores:")
            cv_scores = []
            for i, cfg in enumerate(pso_configs):
                model_key = f'model_{i}'
                if model_key in mc_cv:
                    scores = mc_cv[model_key]
                    print(f"\n   {cfg['name']}:")
                    print(f"     Mean CV score:   {scores['mean_score']:.4f}")
                    print(f"     Std CV score:    {scores['std_score']:.4f}")
                    print(f"     Median CV score: {scores['median_score']:.4f}")

                    if 'confidence_interval' in scores:
                        ci = scores['confidence_interval']
                        print(f"     95% CI: [{ci['lower']:.4f}, {ci['upper']:.4f}]")

                    cv_scores.append((cfg['name'], scores['mean_score'], scores['std_score']))

        # Model comparison
        if 'model_comparison' in result.data:
            comparison = result.data['model_comparison']

            print("\n5. Statistical Comparison:")

            if 'pairwise_comparisons' in comparison:
                print("\n   Pairwise Tests (after multiple comparison correction):")
                for comp_key, comp_result in comparison['pairwise_comparisons'].items():
                    if comp_result['significant']:
                        better = comp_result['better_method']
                        p_val = comp_result['p_value']
                        diff = comp_result['difference']
                        print(f"     {comp_key}: {better} is significantly better "
                              f"(p={p_val:.4f}, Δ={diff:.4f})")

            if 'model_ranking' in comparison:
                print("\n   Overall Ranking:")
                for rank, (cfg_name, score) in enumerate(comparison['model_ranking'], 1):
                    # Map back to config names
                    model_idx = int(cfg_name.split('_')[1])
                    actual_name = pso_configs[model_idx]['name']
                    print(f"     {rank}. {actual_name:20s} (score: {score:.4f})")

        # Bias-variance analysis
        if 'bias_variance_analysis' in result.data:
            bv_analysis = result.data['bias_variance_analysis']

            print("\n6. Bias-Variance Analysis:")
            for i, cfg in enumerate(pso_configs):
                model_key = f'model_{i}'
                if model_key in bv_analysis:
                    bv = bv_analysis[model_key]
                    print(f"\n   {cfg['name']}:")
                    print(f"     Bias²:    {bv['bias_squared']:.6f}")
                    print(f"     Variance: {bv['variance']:.6f}")

                    # Interpretation
                    ratio = bv['bias_variance_ratio']
                    if ratio > 2.0:
                        print(f"     ⚠ High bias - underfitting (consider larger population)")
                    elif ratio < 0.5:
                        print(f"     ⚠ High variance - overfitting (consider regularization)")
                    else:
                        print(f"     ✓ Good balance")

        print("\n" + "=" * 70)
        print("RECOMMENDATION:")

        # Find best configuration
        if 'model_ranking' in result.data['model_comparison']:
            best_model_key, best_score = result.data['model_comparison']['model_ranking'][0]
            best_idx = int(best_model_key.split('_')[1])
            best_config = pso_configs[best_idx]

            print(f"\n✓ RECOMMENDED PSO Configuration: {best_config['name']}")
            print(f"  Parameters:")
            print(f"    - Population size: {best_config['pop_size']}")
            print(f"    - Inertia weight (w): {best_config['w']}")
            print(f"    - Cognitive coeff (c1): {best_config['c1']}")
            print(f"    - Social coeff (c2): {best_config['c2']}")
            print(f"  Mean CV score: {best_score:.4f}")
            print(f"\n  This configuration showed best generalization across {cv_config.n_repetitions} random splits.")

        print("=" * 70)

    else:
        print(f"\n✗ Cross-validation FAILED: {result.message}")


if __name__ == "__main__":
    main()