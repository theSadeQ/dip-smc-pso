# Example from: docs\reference\plant\models_simplified_config.md
# Index: 2
# Runnable: True
# Hash: d8bced2c

from src.plant.models.simplified.config import *
import numpy as np

# Basic initialization
# Load and validate configuration
from src.plant.models.simplified.config import SimplifiedDIPConfig

config = SimplifiedDIPConfig(
    m0=1.5,  # Cart mass (kg)
    m1=0.3,  # Link 1 mass (kg)
    m2=0.2,  # Link 2 mass (kg)
    l1=0.35,  # Link 1 length (m)
    l2=0.25,  # Link 2 length (m)
    g=9.81   # Gravity (m/s²)
)

# Validate physics constraints
if config.is_valid():
    print("Configuration is physically valid")