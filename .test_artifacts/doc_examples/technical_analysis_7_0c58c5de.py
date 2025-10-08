# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 7
# Runnable: False
# Hash: 0c58c5de

# 8 critical numerical stability failures identified:

numerical_failures = {
    'matrix_conditioning': {
        'test': 'test_matrix_inversion_robustness',
        'issue': 'Ill-conditioned matrices causing inversion failures',
        'condition_numbers': [1e14, 2e13, 8e12],  # Near singular
        'frequency': '15% of test cases'
    },
    'lyapunov_stability': {
        'test': 'test_lyapunov_stability_verification',
        'issue': 'Stability analysis diverging for edge cases',
        'lyapunov_derivatives': [-0.001, 0.002],  # Should be negative definite
        'impact': 'Stability guarantees violated'
    },
    'smc_chattering': {
        'test': 'test_chattering_reduction_effectiveness',
        'issue': 'Chattering reduction not working in boundary layer',
        'chattering_index': 4.7,  # Should be < 2.0
        'boundary_layer_effectiveness': 0.23  # Should be > 0.8
    },
    'division_by_zero': {
        'test': 'test_zero_division_robustness',
        'issue': 'Insufficient safeguards for small denominators',
        'min_denominators': [1e-16, 3e-15],  # Below safe threshold
        'safe_threshold': 1e-12
    },
    'matrix_regularization': {
        'test': 'test_matrix_regularization',
        'issue': 'Regularization not applied consistently',
        'singular_value_ratios': [1e-8, 2e-9],  # Below stability threshold
        'regularization_parameter': 1e-6  # Too small
    }
}