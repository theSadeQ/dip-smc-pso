# Example from: docs\reports\pso_code_quality_optimization_report.md
# Index: 6
# Runnable: False
# Hash: a73c2681

# BEFORE: High complexity __init__ method (CC=42)
   def __init__(self, controller_factory, config, seed=None, ...):
       # 150+ lines of complex initialization

   # RECOMMENDED: Break into focused methods
   def __init__(self, controller_factory, config, seed=None, ...):
       self._validate_config(config)
       self._setup_random_state(seed)
       self._initialize_cost_function()
       self._configure_optimization_parameters()