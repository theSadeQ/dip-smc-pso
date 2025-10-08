# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 24
# Runnable: False
# Hash: 395b091b

# example-metadata:
# runnable: false

def debug_import_issues():
    """Debug specific import issues."""

    import sys
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries

    # Test specific imports
    import_tests = [
        ('src', 'Basic src module'),
        ('src.controllers', 'Controllers module'),
        ('src.controllers.factory', 'Factory module'),
        ('src.config', 'Config module'),
        ('src.optimization.algorithms.pso_optimizer', 'PSO optimizer')
    ]

    for module_name, description in import_tests:
        try:
            module = __import__(module_name, fromlist=[''])
            print(f"✅ {description}: {module}")
        except ImportError as e:
            print(f"❌ {description}: {e}")

            # Try to give specific help
            if 'src' in module_name:
                print("   Try: sys.path.insert(0, '/path/to/project/root')")
            elif 'mpc' in module_name.lower():
                print("   Try: pip install control-systems-toolkit")

debug_import_issues()