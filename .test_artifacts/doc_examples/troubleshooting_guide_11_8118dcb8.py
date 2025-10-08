# Example from: docs\factory\troubleshooting_guide.md
# Index: 11
# Runnable: False
# Hash: 8118dcb8

# example-metadata:
# runnable: false

def diagnose_optional_dependencies():
    print("Checking optional dependencies")

    optional_deps = {
        'casadi': 'MPC controller',
        'control': 'Advanced control features',
        'cvxpy': 'Optimization-based controllers'
    }

    for package, feature in optional_deps.items():
        try:
            importlib.import_module(package)
            print(f"✓ {package} available - {feature} supported")
        except ImportError:
            print(f"✗ {package} missing - {feature} not available")

# Run diagnostic
diagnose_optional_dependencies()