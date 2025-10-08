# Example from: docs\factory\troubleshooting_guide.md
# Index: 6
# Runnable: True
# Hash: 94186f53

from src.controllers.factory.deprecation import get_controller_migration_guide

def diagnose_deprecation_warnings(controller_type):
    print(f"Checking deprecation warnings for {controller_type}")

    migration_guide = get_controller_migration_guide(controller_type)
    if migration_guide:
        print("Migration guide:")
        for instruction in migration_guide:
            print(f"  - {instruction}")
    else:
        print("No deprecation warnings for this controller type")

# Example usage
diagnose_deprecation_warnings('classical_smc')