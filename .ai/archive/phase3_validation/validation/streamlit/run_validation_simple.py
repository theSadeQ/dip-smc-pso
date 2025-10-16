"""
Simplified Wave 3 Validation Workflow (Python-based).
Avoids PowerShell PATH issues by running everything in Python.
"""
import subprocess
import time
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[4]
CONFIG_FILE = PROJECT_ROOT / "config.yaml"
STREAMLIT_APP = PROJECT_ROOT / "streamlit_app.py"
STREAMLIT_PORT = 8501

def set_theme_config(enable: bool):
    """Toggle theme in config.yaml."""
    config_text = CONFIG_FILE.read_text()
    if enable:
        config_text = config_text.replace(
            "enable_dip_theme: false", "enable_dip_theme: true"
        )
        print(f"[INFO] Theme ENABLED in config.yaml")
    else:
        config_text = config_text.replace(
            "enable_dip_theme: true", "enable_dip_theme: false"
        )
        print(f"[INFO] Theme DISABLED in config.yaml")
    CONFIG_FILE.write_text(config_text)

def run_script(script_name, *args):
    """Run a Python validation script."""
    print(f"\n[STEP] Running: {script_name}")
    cmd = [sys.executable, script_name, *args]
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    if result.returncode != 0:
        print(f"[ERROR] {script_name} failed")
        return False
    print(f"[OK] {script_name} completed")
    return True

def main():
    print("="*70)
    print("Wave 3 Streamlit Theme Validation (Simplified)")
    print("="*70)

    # Manual steps required
    print("\n[MANUAL STEPS REQUIRED]:")
    print("1. Open 2 terminals")
    print("2. Terminal 1: cd D:\\Projects\\main && python -m streamlit run streamlit_app.py")
    print("3. Wait for Streamlit to start (http://localhost:8501)")
    print("4. Terminal 2: Run this script again with --run flag")
    print("\nTo run validation:")
    print("  python run_validation_simple.py --run")

    if "--run" not in sys.argv:
        return

    print("\n" + "="*70)
    print("Starting Validation Workflow...")
    print("="*70)

    # Assume Streamlit is already running
    input("\n[ACTION REQUIRED] Make sure Streamlit is running. Press ENTER when ready...")

    # Step 1: Baseline screenshots (theme disabled)
    print("\n" + "="*70)
    print("Phase 1: Baseline Screenshots (theme disabled)")
    print("="*70)
    set_theme_config(enable=False)
    input("[ACTION] Restart Streamlit, then press ENTER...")
    time.sleep(2)

    if not run_script("wave3_screenshot_capture.py", "baseline"):
        sys.exit(1)

    # Step 2: Themed screenshots (theme enabled)
    print("\n" + "="*70)
    print("Phase 2: Themed Screenshots (theme enabled)")
    print("="*70)
    set_theme_config(enable=True)
    input("[ACTION] Restart Streamlit, then press ENTER...")
    time.sleep(2)

    if not run_script("wave3_screenshot_capture.py", "themed"):
        sys.exit(1)

    # Step 3: Visual regression
    print("\n" + "="*70)
    print("Phase 3: Visual Regression Analysis")
    print("="*70)
    if not run_script("wave3_visual_regression.py"):
        sys.exit(1)

    # Step 4: Accessibility audit (requires Streamlit running)
    print("\n" + "="*70)
    print("Phase 4: Accessibility Audit")
    print("="*70)
    if not run_script("wave3_axe_audit.py"):
        sys.exit(1)

    # Step 5: Performance
    print("\n" + "="*70)
    print("Phase 5: Performance Measurement")
    print("="*70)
    if not run_script("wave3_performance.py"):
        sys.exit(1)

    # Step 6: Summary
    print("\n" + "="*70)
    print("Phase 6: Comparison Analysis")
    print("="*70)
    if not run_script("wave3_comparison_analysis.py"):
        sys.exit(1)

    print("\n" + "="*70)
    print("VALIDATION COMPLETE!")
    print("="*70)
    print("Check: .codex/phase3/validation/streamlit/wave3/VALIDATION_SUMMARY.md")

if __name__ == "__main__":
    main()
