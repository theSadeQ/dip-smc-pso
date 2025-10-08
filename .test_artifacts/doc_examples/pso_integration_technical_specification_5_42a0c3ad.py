# Example from: docs\pso_integration_technical_specification.md
# Index: 5
# Runnable: False
# Hash: 42a0c3ad

# example-metadata:
# runnable: false

class PSOConfigValidator:
    """
    Validates PSO configuration for mathematical consistency and stability.
    """

    @staticmethod
    def validate_hyperparameters(pso_config: PSOConfig) -> ValidationResult:
        """
        Validate PSO hyperparameter relationships for convergence guarantee.

        Mathematical Foundations:
        - Clerc-Kennedy constriction factor: χ = 2/|2 - φ - √(φ² - 4φ)|
        - Stability condition: φ = c₁ + c₂ > 4 for guaranteed convergence
        - Inertia weight bounds: ω ∈ [0.4, 0.9] for balanced exploration
        """
        errors = []

        # PSO stability condition
        phi = pso_config.c1 + pso_config.c2
        if phi <= 4.0:
            errors.append(f"PSO divergence risk: c₁ + c₂ = {phi:.3f} ≤ 4.0")

        # Balanced cognitive/social coefficients
        if abs(pso_config.c1 - pso_config.c2) > 0.5:
            errors.append(f"Unbalanced coefficients: |c₁ - c₂| = {abs(pso_config.c1 - pso_config.c2):.3f} > 0.5")

        # Inertia weight bounds
        if not (0.4 <= pso_config.w <= 0.9):
            errors.append(f"Inertia weight ω = {pso_config.w:.3f} outside optimal range [0.4, 0.9]")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

    @staticmethod
    def validate_bounds_consistency(bounds: PSOBounds, controller_type: str) -> ValidationResult:
        """
        Ensure PSO bounds align with controller stability requirements.
        """
        registry_bounds = CONTROLLER_REGISTRY[controller_type]['gain_bounds']
        errors = []

        for i, ((pso_min, pso_max), (theory_min, theory_max)) in enumerate(zip(
            zip(bounds.min, bounds.max), registry_bounds
        )):
            if pso_min < theory_min:
                errors.append(f"Gain {i}: PSO min {pso_min} < theoretical min {theory_min}")
            if pso_max > theory_max:
                errors.append(f"Gain {i}: PSO max {pso_max} > theoretical max {theory_max}")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)