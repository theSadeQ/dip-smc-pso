# Example from: docs\fault_detection_system_documentation.md
# Index: 12
# Runnable: True
# Hash: 250f5e28

@dataclass
class FDIsystem:
    residual_threshold: float = 0.150      # Calibrated from 0.5
    hysteresis_enabled: bool = False       # Backward compatible
    hysteresis_upper: float = 0.165
    hysteresis_lower: float = 0.135