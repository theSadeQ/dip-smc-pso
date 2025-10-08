# Example from: docs\fdi_threshold_calibration_methodology.md
# Index: 2
# Runnable: False
# Hash: 879b3fc5

@dataclass
class FDIsystem:
    # Core parameters
    residual_threshold: float = 0.150  # Updated from 0.5 → 0.150
    persistence_counter: int = 10
    residual_states: List[int] = field(default_factory=lambda: [0, 1, 2])
    residual_weights: Optional[List[float]] = None

    # Hysteresis parameters (new)
    hysteresis_enabled: bool = False
    hysteresis_upper: float = 0.165  # threshold * 1.1
    hysteresis_lower: float = 0.135  # threshold * 0.9