# Example from: docs\guides\api\plant-models.md
# Index: 4
# Runnable: True
# Hash: 670643f5

from src.config import load_config

config = load_config('config.yaml')
physics = config.dip_params

print(f"Cart mass: {physics.m0} kg")
print(f"Pendulum lengths: {physics.l1}, {physics.l2} m")
print(f"Gravity: {physics.g} m/s²")