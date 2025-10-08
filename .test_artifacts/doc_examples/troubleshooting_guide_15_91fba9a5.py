# Example from: docs\factory\troubleshooting_guide.md
# Index: 15
# Runnable: True
# Hash: 91fba9a5

def gather_diagnostic_info():
    """Gather comprehensive diagnostic information."""

    import sys
    import platform
    import numpy as np

    info = {
        'system': {
            'platform': platform.platform(),
            'python_version': sys.version,
            'numpy_version': np.__version__
        },
        'factory': {},
        'performance': {},
        'errors': []
    }

    # Factory information
    try:
        from src.controllers.factory import list_available_controllers, CONTROLLER_REGISTRY
        info['factory']['available_controllers'] = list_available_controllers()
        info['factory']['registry_size'] = len(CONTROLLER_REGISTRY)
    except Exception as e:
        info['errors'].append(f"Factory info error: {e}")

    # Performance information
    try:
        start_time = time.perf_counter()
        create_controller('classical_smc', gains=[10]*6)
        creation_time = (time.perf_counter() - start_time) * 1000
        info['performance']['creation_time_ms'] = creation_time
    except Exception as e:
        info['errors'].append(f"Performance test error: {e}")

    return info

# Gather diagnostic information
diagnostic_info = gather_diagnostic_info()
print("Diagnostic information gathered:")
for category, data in diagnostic_info.items():
    print(f"  {category}: {data}")