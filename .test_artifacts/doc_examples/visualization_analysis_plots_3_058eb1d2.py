# Example from: docs\reference\analysis\visualization_analysis_plots.md
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