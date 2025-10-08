# Example from: docs\plant\models_guide.md
# Index: 7
# Runnable: False
# Hash: 6bc32752

# example-metadata:
# runnable: false

# Default parameters (balanced for general use)
config = SimplifiedDIPConfig.create_default()

# Benchmark parameters (standardized for comparisons)
config = SimplifiedDIPConfig.create_benchmark()

# Lightweight parameters (optimized for speed)
config = SimplifiedDIPConfig.create_lightweight()

# Custom parameters
config = SimplifiedDIPConfig(
    cart_mass=1.2,
    pendulum1_mass=0.15,
    pendulum2_mass=0.15,
    # ... all required fields
)