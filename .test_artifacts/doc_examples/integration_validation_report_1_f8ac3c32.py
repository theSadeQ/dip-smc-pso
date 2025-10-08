# Example from: docs\reports\integration_validation_report.md
# Index: 1
# Runnable: True
# Hash: f8ac3c32

def _resolve_controller_gains(gains, config, controller_type, controller_info):
    """Multi-source parameter resolution with fallback chain"""
    # 1. Explicit gains (highest priority)
    # 2. Configuration extraction
    # 3. Default values (fallback)
    # Result: Robust parameter handling