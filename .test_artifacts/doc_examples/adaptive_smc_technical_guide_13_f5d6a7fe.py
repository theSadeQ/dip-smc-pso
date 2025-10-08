# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 13
# Runnable: False
# Hash: f5d6a7fe

def diagnose_adaptation(controller, history):
    """Diagnose adaptive SMC health."""

    K_history = np.array(history['K'])
    sigma_history = np.array(history['sigma'])
    dK_history = np.array(history['dK'])

    diagnostics = {}

    # Gain statistics
    diagnostics['K_mean'] = np.mean(K_history)
    diagnostics['K_std'] = np.std(K_history)
    diagnostics['K_final'] = K_history[-1]

    # Adaptation activity
    adaptation_active = np.sum(np.abs(sigma_history) > controller.dead_zone)
    diagnostics['adaptation_ratio'] = adaptation_active / len(sigma_history)

    # Gain oscillation check
    sign_changes = np.sum(np.diff(np.sign(dK_history)) != 0)
    diagnostics['gain_oscillations'] = sign_changes

    # Saturation checks
    diagnostics['hit_K_max'] = np.any(K_history >= controller.K_max * 0.99)
    diagnostics['hit_K_min'] = np.any(K_history <= controller.K_min * 1.01)

    # Warnings
    if diagnostics['gain_oscillations'] > len(dK_history) * 0.5:
        print("WARNING: Excessive gain oscillation")

    if diagnostics['hit_K_max']:
        print("WARNING: Gain saturated at K_max")

    if diagnostics['adaptation_ratio'] > 0.9:
        print("WARNING: Rarely in dead zone - check dead_zone parameter")

    return diagnostics