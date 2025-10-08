# Example from: docs\pso_integration_technical_specification.md
# Index: 2
# Runnable: False
# Hash: e231a5ce

# Controller Registry with PSO Integration Metadata
CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ModularClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [5.0, 5.0, 5.0, 0.5, 0.5, 0.5],
        'n_gains': 6,
        'gain_bounds': [(0.1, 50.0)] * 6,
        'stability_requirements': {
            'sliding_surface_gains': [0, 1, 2, 3],  # Indices for c₁, λ₁, c₂, λ₂
            'switching_gains': [4, 5],              # Indices for K, kd
            'positive_definite': True
        }
    },
    'sta_smc': {
        'class': ModularSuperTwistingSMC,
        'config_class': STASMCConfig,
        'default_gains': [8.0, 4.0, 12.0, 6.0, 4.85, 3.43],  # Issue #2 optimized
        'n_gains': 6,
        'gain_bounds': [(1.0, 100.0), (1.0, 100.0), (1.0, 20.0), (1.0, 20.0), (0.1, 10.0), (0.1, 10.0)],
        'stability_requirements': {
            'algorithmic_gains': [0, 1],    # K₁, K₂ with K₁ > K₂ condition
            'surface_gains': [2, 3],        # k₁, k₂
            'surface_coefficients': [4, 5], # λ₁, λ₂ for target damping ζ = 0.7
            'finite_time_convergence': True
        }
    }
    # Additional controller specifications...
}