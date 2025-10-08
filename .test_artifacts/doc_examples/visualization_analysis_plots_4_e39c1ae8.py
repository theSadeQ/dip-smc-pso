# Example from: docs\reference\analysis\visualization_analysis_plots.md
# Index: 4
# Runnable: True
# Hash: e39c1ae8

# FDI system usage
from src.analysis.fault_detection import FDISystem

fdi = FDISystem(config)
residual = fdi.generate_residual(y, u)
fault = fdi.detect(residual)