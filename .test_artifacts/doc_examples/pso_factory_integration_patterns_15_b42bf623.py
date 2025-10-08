# Example from: docs\pso_factory_integration_patterns.md
# Index: 15
# Runnable: False
# Hash: b42bf623

# example-metadata:
# runnable: false

# ✅ Good: Comprehensive error handling
def robust_fitness_function(gains):
    try:
        # Validate inputs
        if not validate_smc_gains(controller_type, gains):
            return float('inf')

        # Create controller
        controller = factory(gains)

        # Evaluate with timeout
        with timeout(30):  # 30-second timeout
            performance = evaluate_performance(controller)

        # Check for numerical issues
        if not np.isfinite(performance['total_cost']):
            return float('inf')

        return performance['total_cost']

    except TimeoutError:
        logger.warning(f"Evaluation timeout for gains: {gains}")
        return float('inf')
    except Exception as e:
        logger.warning(f"Evaluation failed for gains {gains}: {e}")
        return float('inf')