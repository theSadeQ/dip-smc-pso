# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 1
# Runnable: True
# Hash: 4858dc56

# Uncovered: Exception branches
   try:
       validate_gains(gains)
   except ValueError as e:  # ← Often uncovered
       logger.error(f"Invalid gains: {e}")
       raise ControllerConfigurationError(e)