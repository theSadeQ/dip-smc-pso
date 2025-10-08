# Example from: docs\fault_detection_system_documentation.md
# Index: 1
# Runnable: False
# Hash: af60ad23

# example-metadata:
# runnable: false

class FDIsystem:
    # Detection state
    _counter: int                    # Persistence violation counter
    _last_state: np.ndarray         # Previous state for prediction
    tripped_at: Optional[float]     # Fault detection timestamp

    # Adaptive thresholding state
    _residual_window: List[float]   # Sliding window of residuals

    # CUSUM state
    _cusum: float                   # Cumulative sum statistic

    # Analysis history
    times: List[float]              # Timestamps for analysis
    residuals: List[float]          # Residual history for analysis