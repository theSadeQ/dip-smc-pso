# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 7
# Runnable: True
# Hash: d1889ee7

# Uncovered: Invalid controller type handling
   def create_controller(controller_type: str, **kwargs):
       if controller_type not in VALID_CONTROLLERS:  # ← Not tested
           raise ValueError(f"Unknown controller: {controller_type}")