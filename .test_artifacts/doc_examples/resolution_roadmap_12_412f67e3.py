# Example from: docs\testing\reports\2025-09-30\technical\resolution_roadmap.md
# Index: 12
# Runnable: False
# Hash: 412f67e3

# example-metadata:
# runnable: false

# File: src/utils/validation/gain_validator.py
class GainValidator:
    """Comprehensive gain validation for numerical stability."""

    def __init__(self, stability_margins: dict):
        self.min_gains = stability_margins["min_gains"]
        self.max_gains = stability_margins["max_gains"]
        self.stability_constraints = stability_margins["stability_constraints"]

    def validate_gain_stability(self, gains: List[float], controller_type: str) -> ValidationResult:
        """Validate gains for numerical and control stability."""
        results = ValidationResult()

        # Basic bounds checking
        if not self._check_gain_bounds(gains):
            results.add_error("Gains outside allowable bounds")

        # Stability-specific validation
        if controller_type == "classical_smc":
            results.merge(self._validate_classical_smc_gains(gains))
        elif controller_type == "adaptive_smc":
            results.merge(self._validate_adaptive_smc_gains(gains))

        # Numerical conditioning checks
        results.merge(self._validate_numerical_conditioning(gains))

        return results

    def _validate_numerical_conditioning(self, gains: List[float]) -> ValidationResult:
        """Check for potential numerical conditioning issues."""
        results = ValidationResult()

        # Check for extreme gain ratios
        gain_ratios = [g1/g2 for g1 in gains for g2 in gains if g2 != 0]
        max_ratio = max(gain_ratios)

        if max_ratio > NUMERICAL_CONDITIONING_THRESHOLD:
            results.add_warning(f"Large gain ratio detected: {max_ratio:.2e}")

        # Check for very small or large gains
        if any(g < MINIMUM_STABLE_GAIN for g in gains):
            results.add_error("Gains too small for numerical stability")

        if any(g > MAXIMUM_STABLE_GAIN for g in gains):
            results.add_error("Gains too large for numerical stability")

        return results