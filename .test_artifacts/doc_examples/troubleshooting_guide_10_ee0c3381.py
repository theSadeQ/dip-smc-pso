# Example from: docs\factory\troubleshooting_guide.md
# Index: 10
# Runnable: True
# Hash: ee0c3381

import sys
import importlib.util

def diagnose_import_errors():
    print("Diagnosing import errors")

    critical_modules = [
        'src.controllers.factory',
        'src.controllers.smc.algorithms.classical.controller',
        'src.controllers.smc.algorithms.adaptive.controller',
        'src.controllers.smc.algorithms.super_twisting.controller',
        'src.controllers.smc.algorithms.hybrid.controller'
    ]

    for module_name in critical_modules:
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                print(f"✗ Module not found: {module_name}")
            else:
                print(f"✓ Module available: {module_name}")
                # Try importing
                module = importlib.import_module(module_name)
                print(f"  ✓ Import successful")
        except ImportError as e:
            print(f"✗ Import error for {module_name}: {e}")
        except Exception as e:
            print(f"✗ Unexpected error for {module_name}: {e}")

    # Check Python path
    print(f"\nPython path:")
    for path in sys.path:
        print(f"  - {path}")

# Run diagnostic
diagnose_import_errors()