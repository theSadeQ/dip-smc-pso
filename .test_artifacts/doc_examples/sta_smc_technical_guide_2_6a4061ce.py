# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 2
# Runnable: False
# Hash: 6a4061ce

@numba.njit(cache=True)
def _sta_smc_core(...):
    # Sliding surface (inline)
    sigma = k1*(th1dot + lam1*th1) + k2*(th2dot + lam2*th2)

    # Continuous term (sqrt is expensive)
    u_cont = -K1 * np.sqrt(np.abs(sigma)) * sgn_sigma

    # Integral update
    new_z = z - K2 * sgn_sigma * dt

    # Anti-windup back-calculation
    new_z += Kaw * (u_sat - u_raw) * dt

    return u_sat, new_z, sigma