# Example from: docs\pso_configuration_schema_documentation.md
# Index: 1
# Runnable: False
# Hash: b1aa37f8

# example-metadata:
# runnable: false

def validate_pso_algorithm_params(params: dict) -> ValidationResult:
    """
    Validate core PSO algorithm parameters for mathematical consistency.

    Validation Rules:
    1. Clerc-Kennedy stability: φ = c₁ + c₂ > 4 for guaranteed convergence
    2. Balanced coefficients: |c₁ - c₂| ≤ 0.5 for exploration-exploitation balance
    3. Inertia bounds: w ∈ [0.4, 0.9] for optimal performance
    4. Swarm size: n ∈ [10, 50] for computational efficiency vs quality
    """
    errors = []

    # PSO stability condition (Clerc-Kennedy)
    phi = params['c1'] + params['c2']
    if phi <= 4.0:
        errors.append(f"PSO convergence risk: φ = c₁ + c₂ = {phi:.3f} ≤ 4.0")

    # Coefficient balance
    coeff_diff = abs(params['c1'] - params['c2'])
    if coeff_diff > 0.5:
        errors.append(f"Unbalanced coefficients: |c₁ - c₂| = {coeff_diff:.3f} > 0.5")

    # Inertia weight validation
    if not (0.4 <= params['w'] <= 0.9):
        errors.append(f"Inertia weight w = {params['w']:.3f} outside optimal range [0.4, 0.9]")

    # Swarm size validation
    if not (10 <= params['n_particles'] <= 50):
        errors.append(f"Swarm size {params['n_particles']} outside recommended range [10, 50]")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)