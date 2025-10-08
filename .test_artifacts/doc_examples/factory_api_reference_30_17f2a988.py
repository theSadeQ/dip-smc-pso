# Example from: docs\factory\factory_api_reference.md
# Index: 30
# Runnable: True
# Hash: 17f2a988

from src.controllers.factory.deprecation import get_controller_migration_guide

guide = get_controller_migration_guide('classical_smc')
for instruction in guide:
    print(f"- {instruction}")