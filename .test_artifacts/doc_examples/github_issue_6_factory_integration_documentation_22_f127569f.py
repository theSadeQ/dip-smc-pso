# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 22
# Runnable: True
# Hash: f127569f

# Legacy code continues to work unchanged
from controllers.factory import create_controller

# This still works exactly as before
controller = create_controller(
    "classical_smc",
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0
)