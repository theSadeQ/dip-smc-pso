# Example from: docs\GitHub_Issue_4_PSO_Integration_Resolution_Report.md
# Index: 2
# Runnable: False
# Hash: 40a49924

# example-metadata:
# runnable: false

def _validate_pso_parameters(self) -> bool:
    """
    Validate PSO parameters for mathematical consistency.

    Validation Rules:
    1. Clerc-Kennedy stability: φ = c₁ + c₂ > 4
    2. Balanced coefficients: |c₁ - c₂| ≤ 0.5
    3. Inertia bounds: w ∈ [0.4, 0.9]
    4. Parameter count consistency
    """
    c1, c2 = self.pso_config['c1'], self.pso_config['c2']
    phi = c1 + c2

    if phi <= 4.0:
        raise ValueError(f"PSO convergence risk: φ = {phi:.3f} ≤ 4.0")

    if abs(c1 - c2) > 0.5:
        raise ValueError(f"Unbalanced coefficients: |c₁ - c₂| = {abs(c1 - c2):.3f}")

    return True