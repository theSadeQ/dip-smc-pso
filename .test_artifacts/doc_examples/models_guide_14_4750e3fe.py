# Example from: docs\plant\models_guide.md
# Index: 14
# Runnable: False
# Hash: 4750e3fe

class NumericalStabilityMonitor:
    """Monitor numerical stability statistics."""

    def record_inversion(
        self,
        condition_number: float,
        was_regularized: bool,
        failed: bool
    ) -> None:
        """Record matrix inversion event."""
        self.condition_numbers.append(condition_number)
        self.regularization_count += int(was_regularized)
        self.failure_count += int(failed)