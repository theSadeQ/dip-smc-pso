# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 40
# Runnable: True
# Hash: ee6792e8

# Old way - basic PSO without factory integration
from src.optimizer.pso_optimizer import PSOTuner

tuner = PSOTuner(controller_factory, config)
result = tuner.optimise()