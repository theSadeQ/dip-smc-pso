# Example from: docs\testing\reports\2025-09-30\technical_analysis.md
# Index: 3
# Runnable: False
# Hash: 2de0f21d

# 1. Adaptive Threshold with Hysteresis
class AdaptiveThreshold:
    def __init__(self, base_threshold=0.135, hysteresis=0.02):
        self.base_threshold = base_threshold
        self.hysteresis = hysteresis
        self.current_state = "OK"

    def evaluate(self, residual_norm):
        if self.current_state == "OK":
            threshold = self.base_threshold
        else:
            threshold = self.base_threshold - self.hysteresis  # Lower for recovery

        if residual_norm > threshold:
            self.current_state = "FAULT"
        elif residual_norm < threshold - self.hysteresis:
            self.current_state = "OK"

        return self.current_state

# 2. Statistical Threshold Calibration
def calibrate_threshold_from_data(residuals, false_positive_rate=0.05):
    """Set threshold based on statistical analysis."""
    return np.percentile(residuals, (1 - false_positive_rate) * 100)

# 3. Enhanced Residual Calculation
def compute_robust_residual(y_actual, y_predicted, outlier_threshold=3.0):
    """Compute residual with outlier rejection."""
    raw_residual = np.linalg.norm(y_actual - y_predicted)

    # Z-score based outlier detection
    if abs(raw_residual - residual_mean) / residual_std > outlier_threshold:
        return previous_valid_residual  # Use previous value for outliers

    return raw_residual