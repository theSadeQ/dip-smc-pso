#!/usr/bin/env python3
"""
Validate all Streamlit app imports before running Playwright tests.

This script ensures that all required modules can be imported successfully
before running E2E tests. It prevents test failures due to import errors.

Usage:
    python scripts/validate_streamlit_imports.py
    python scripts/validate_streamlit_imports.py && pytest tests/test_ui/

Exit Codes:
    0: All imports successful
    1: One or more imports failed
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def validate_imports():
    """
    Validate all critical imports for Streamlit app.

    Returns:
        True if all imports successful, False otherwise
    """
    errors = []

    # Test 1: Visualizer import
    print("[INFO] Validating Visualizer import...")
    try:
        from src.utils import Visualizer
        print("[OK] Visualizer import successful")
    except Exception as e:
        errors.append(f"[ERROR] Visualizer import failed: {e}")

    # Test 2: Monitoring modules
    print("[INFO] Validating monitoring modules...")
    try:
        from src.utils.monitoring.job_manager import JobManager
        from src.utils.monitoring.pso_config_panel import render_pso_config_panel
        from src.utils.monitoring.progress_monitor import render_progress_monitor
        print("[OK] Monitoring modules import successful")
    except Exception as e:
        errors.append(f"[ERROR] Monitoring import failed: {e}")

    # Test 3: Can create JobManager
    print("[INFO] Validating JobManager instantiation...")
    try:
        job_manager = JobManager()
        print("[OK] JobManager instantiation successful")
    except Exception as e:
        errors.append(f"[ERROR] JobManager creation failed: {e}")

    # Test 4: Config loading
    print("[INFO] Validating config loading...")
    try:
        from src.config import load_config
        config = load_config("config.yaml")
        print("[OK] Config loading successful")
    except Exception as e:
        errors.append(f"[ERROR] Config loading failed: {e}")

    # Test 5: Controllers
    print("[INFO] Validating controller imports...")
    try:
        from src.controllers.factory import create_controller
        print("[OK] Controller factory import successful")
    except Exception as e:
        errors.append(f"[ERROR] Controller import failed: {e}")

    # Report results
    if errors:
        print("\n" + "=" * 80)
        print("[IMPORT VALIDATION FAILED]")
        print("=" * 80)
        for error in errors:
            print(error)
        print("=" * 80)
        return False

    print("\n" + "=" * 80)
    print("[OK] All imports validated successfully")
    print("=" * 80)
    print("Streamlit app is ready for Playwright testing.")
    return True


if __name__ == "__main__":
    success = validate_imports()
    sys.exit(0 if success else 1)
