# Example from: docs\guides\api\simulation.md
# Index: 1
# Runnable: True
# Hash: f13a7b52

from src.core import SimulationRunner
from src.config import load_config

config = load_config('config.yaml')
runner = SimulationRunner(config)