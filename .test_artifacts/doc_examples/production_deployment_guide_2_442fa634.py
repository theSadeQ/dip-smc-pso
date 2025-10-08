# Example from: docs\factory\production_deployment_guide.md
# Index: 2
# Runnable: False
# Hash: 442fa634

def verify_production_dependencies():
    """Verify all required dependencies are available."""

    required_packages = {
        'numpy': '>=1.19.0',
        'scipy': '>=1.6.0',
        'pydantic': '>=1.8.0',
        'pyyaml': '>=5.4.0'
    }

    optional_packages = {
        'psutil': '>=5.8.0',  # For memory monitoring
        'prometheus_client': '>=0.12.0',  # For metrics
        'structlog': '>=21.0.0'  # For structured logging
    }

    print("Verifying production dependencies...")

    # Check required packages
    for package, version in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} {version} - Available")
        except ImportError:
            print(f"❌ {package} {version} - MISSING (REQUIRED)")
            return False

    # Check optional packages
    for package, version in optional_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} {version} - Available")
        except ImportError:
            print(f"⚠️ {package} {version} - Missing (optional)")

    return True

# Verify dependencies
dependencies_ok = verify_production_dependencies()