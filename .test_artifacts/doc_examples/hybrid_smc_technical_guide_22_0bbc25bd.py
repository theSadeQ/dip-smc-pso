# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 22
# Runnable: False
# Hash: 0bbc25bd

# example-metadata:
# runnable: false

def diagnose_hybrid_controller(controller, state, result):
    """Comprehensive controller diagnostics."""

    diagnostics = {}

    # Extract current values
    k1, k2, u_int = result.state_vars
    s = result.sliding_surface

    # Check adaptation health
    diagnostics['adaptation_active'] = abs(s) > controller.dead_zone
    diagnostics['gains_saturated'] = (k1 >= controller.k1_max * 0.9 or
                                    k2 >= controller.k2_max * 0.9)

    # Check numerical health
    diagnostics['values_finite'] = all(np.isfinite([k1, k2, u_int, s]))
    diagnostics['within_bounds'] = abs(result.control) <= controller.max_force

    # Performance indicators
    diagnostics['surface_distance'] = abs(s)
    diagnostics['adaptation_ratio'] = (k1 + k2) / (controller.k1_max + controller.k2_max)

    return diagnostics