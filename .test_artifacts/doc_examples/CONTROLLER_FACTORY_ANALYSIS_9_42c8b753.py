# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 9
# Runnable: False
# Hash: 42c8b753

# example-metadata:
# runnable: false

def _validate_controller_gains(gains, controller_info, controller_type):
    # 1. Basic validation
    if len(gains) != expected_count: raise ValueError(...)
    if not all(isinstance(g, (int, float)) and np.isfinite(g) for g in gains): raise ValueError(...)
    if any(g <= 0 for g in gains): raise ValueError(...)

    # 2. Controller-specific validation
    if controller_type == 'sta_smc' and gains[0] <= gains[1]:
        raise ValueError("Super-Twisting stability requires K1 > K2 > 0")