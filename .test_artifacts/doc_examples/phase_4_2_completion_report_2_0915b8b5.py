# Example from: docs\api\phase_4_2_completion_report.md
# Index: 2
# Runnable: True
# Hash: 0915b8b5

if controller_type not in CONTROLLER_REGISTRY:
    available = list(CONTROLLER_REGISTRY.keys())
    raise ValueError(f"Unknown controller type '{controller_type}'. Available: {available}")