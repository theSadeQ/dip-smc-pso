# Example from: docs\reference\analysis\visualization___init__.md
# Index: 5
# Runnable: True
# Hash: 058eb1d2

# Complete analysis workflow
from src.analysis import analyze

results = analyze(
    data=sensor_data,
    method='enhanced',
    visualization=True
)