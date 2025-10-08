# Example from: docs\api\phase_4_2_completion_report.md
# Index: 9
# Runnable: False
# Hash: 5b2a0a17

# Scenario: Registry defaults violate STA constraint K1 > K2
CONTROLLER_REGISTRY['sta_smc']['default_gains'] = [15.0, 20.0, ...]  # K1=15 ≤ K2=20 ✗

# Factory detection and correction:
try:
    _validate_controller_gains(default_gains, ...)
except ValueError:
    if gains is None:  # Only auto-fix defaults
        controller_gains = [25.0, 15.0, 20.0, 12.0, 8.0, 6.0]  # K1=25 > K2=15 ✓