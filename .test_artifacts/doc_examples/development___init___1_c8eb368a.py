# Example from: docs\reference\utils\development___init__.md
# Index: 1
# Runnable: True
# Hash: c8eb368a

from src.utils.development import load_simulation_environment

# Load environment in Jupyter
%load_ext autoreload
%autoreload 2

# Load simulation tools
from src.utils.development import JupyterTools
tools = JupyterTools()

# Interactive plotting
%matplotlib inline
tools.plot_controller_performance(results)

# Timing analysis
%timeit controller.compute_control(x, state_vars, history)