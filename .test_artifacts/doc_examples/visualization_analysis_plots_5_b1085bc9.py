# Example from: docs\reference\analysis\visualization_analysis_plots.md
# Index: 5
# Runnable: True
# Hash: b1085bc9

# Generate analysis plots
from src.analysis.visualization import AnalysisPlotter

plotter = AnalysisPlotter(style='professional')
fig = plotter.plot_time_series(data)
fig.savefig('analysis.pdf')