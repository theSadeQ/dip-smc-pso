# Example from: docs\api\phase_4_2_completion_report.md
# Index: 14
# Runnable: True
# Hash: bded1bc4

# Future: Validate config.yaml before controller creation
from src.controllers.factory import validate_configuration

errors = validate_configuration("config.yaml")
if errors:
    for error in errors:
        print(f"Config error: {error}")