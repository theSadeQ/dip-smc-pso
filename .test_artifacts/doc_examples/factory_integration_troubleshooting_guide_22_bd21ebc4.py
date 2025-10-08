# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 22
# Runnable: True
# Hash: bd21ebc4

def fix_python_path():
    """Fix Python path for project imports."""

    import sys
    import os
    from pathlib import Path

    # Get project root directory
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir

    # Find project root by looking for key files
    while project_root.parent != project_root:
        if (project_root / 'src').exists() and (project_root / 'config.yaml').exists():
            break
        project_root = project_root.parent

    # Add to Python path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"Added to Python path: {project_root}")

    # Verify imports work
    try:
        from src.controllers.factory import create_controller
        print("✅ Factory imports working")
        return True
    except ImportError as e:
        print(f"❌ Import still failing: {e}")
        return False

# Fix path before imports
fix_python_path()