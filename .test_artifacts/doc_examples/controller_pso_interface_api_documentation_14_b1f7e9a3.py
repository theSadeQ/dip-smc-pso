# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 14
# Runnable: False
# Hash: b1f7e9a3

# example-metadata:
# runnable: false

from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Parameter validation result."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class ParameterValidator:
    """Controller parameter validation utilities."""

    @staticmethod
    def validate_gain_vector(gains: np.ndarray,
                           controller_type: str) -> ValidationResult:
        """Validate gain vector for specific controller type.

        Parameters
        ----------
        gains : np.ndarray
            Controller gain vector
        controller_type : str
            Controller type identifier

        Returns
        -------
        ValidationResult
            Validation outcome with error details
        """
        errors = []
        warnings = []

        # Check dimensionality
        expected_dims = {
            'classical_smc': 6,
            'sta_smc': 6,
            'adaptive_smc': 5,
            'hybrid_adaptive_sta_smc': 4
        }

        if controller_type not in expected_dims:
            errors.append(f"Unknown controller type: {controller_type}")
            return ValidationResult(False, errors, warnings)

        expected_dim = expected_dims[controller_type]
        if len(gains) != expected_dim:
            errors.append(f"Expected {expected_dim} gains, got {len(gains)}")

        # Check for NaN/Inf values
        if not np.all(np.isfinite(gains)):
            errors.append("Gains contain NaN or infinite values")

        # Controller-specific validation
        if controller_type == 'classical_smc':
            c1, lambda1, c2, lambda2, K, kd = gains
            if lambda1 <= 0 or lambda2 <= 0:
                errors.append("Sliding surface coefficients must be positive")
            if K <= 0:
                errors.append("Control gain must be positive")
            if kd < 0:
                warnings.append("Negative derivative gain may cause instability")

        # Add similar validation for other controller types...

        return ValidationResult(len(errors) == 0, errors, warnings)