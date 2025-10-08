# Example from: docs\reference\analysis\fault_detection_residual_generators.md
# Index: 3
# Runnable: True
# Hash: 058eb1d2

# Complete analysis workflow
from src.analysis import analyze

results = analyze(
    data=sensor_data,
    method='enhanced',
    visualization=True
)