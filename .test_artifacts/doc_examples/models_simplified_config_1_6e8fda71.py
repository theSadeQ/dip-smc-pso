# Example from: docs\reference\plant\models_simplified_config.md
# Index: 1
# Runnable: False
# Hash: 6e8fda71

# example-metadata:
# runnable: false

default_config = SimplifiedDIPConfig(
    m0=1.0,   # 1 kg cart
    m1=0.2,   # 200g link 1
    m2=0.1,   # 100g link 2
    l1=0.3,   # 30cm link 1
    l2=0.2,   # 20cm link 2
    g=9.81,   # Earth gravity
    d0=0.1,   # Light cart damping
    d1=0.01,  # Light joint damping
    d2=0.01
)