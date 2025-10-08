# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 23
# Runnable: False
# Hash: 9a1b776f

def check_dependencies():
    """Check all project dependencies."""

    required_packages = {
        'numpy': 'pip install numpy',
        'scipy': 'pip install scipy',
        'matplotlib': 'pip install matplotlib',
        'pydantic': 'pip install pydantic',
        'yaml': 'pip install pyyaml',
        'numba': 'pip install numba'
    }

    optional_packages = {
        'control': 'pip install control-systems-toolkit (for MPC)',
        'cvxopt': 'pip install cvxopt (for optimization-based MPC)',
        'streamlit': 'pip install streamlit (for web interface)'
    }

    print("Checking required dependencies:")
    missing_required = []

    for package, install_cmd in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - {install_cmd}")
            missing_required.append((package, install_cmd))

    print("\nChecking optional dependencies:")
    missing_optional = []

    for package, install_cmd in optional_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ⚠️  {package} - {install_cmd}")
            missing_optional.append((package, install_cmd))

    # Installation script
    if missing_required:
        print("\nTo install missing required packages:")
        for package, install_cmd in missing_required:
            print(f"  {install_cmd}")

    if missing_optional:
        print("\nTo install missing optional packages:")
        for package, install_cmd in missing_optional:
            print(f"  {install_cmd}")

    return len(missing_required) == 0

# Check dependencies
check_dependencies()