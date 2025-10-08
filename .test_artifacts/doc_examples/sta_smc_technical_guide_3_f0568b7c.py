# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 3
# Runnable: False
# Hash: f0568b7c

# example-metadata:
# runnable: false

@numba.njit(cache=True)
def _sta_smc_core(
    z, sigma, sgn_sigma,
    alg_gain_K1, alg_gain_K2, damping_gain,
    dt, max_force, u_eq=0.0, Kaw=0.0
):
    """Numba-accelerated STA core with anti-windup."""

    # Continuous term (square-root law)
    u_cont = -alg_gain_K1 * np.sqrt(np.abs(sigma)) * sgn_sigma

    # Integral term (previous z)
    u_dis = z

    # Unsaturated control
    u_raw = u_eq + u_cont + u_dis - damping_gain * sigma

    # Saturate control
    if u_raw > max_force:
        u_sat = max_force
    elif u_raw < -max_force:
        u_sat = -max_force
    else:
        u_sat = u_raw

    # Anti-windup back-calculation
    new_z = z - alg_gain_K2 * sgn_sigma * dt
    new_z += Kaw * (u_sat - u_raw) * dt  # Windup compensation

    # Saturate integrator
    if new_z > max_force:
        new_z = max_force
    elif new_z < -max_force:
        new_z = -max_force

    return float(u_sat), float(new_z), float(sigma)