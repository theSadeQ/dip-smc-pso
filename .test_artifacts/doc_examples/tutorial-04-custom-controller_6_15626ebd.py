# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 6
# Runnable: False
# Hash: 15626ebd

def compute_equivalent_control(self, state: np.ndarray) -> float:
    """
    Compute model-based equivalent control.

    For terminal SMC, this requires computing:
    u_eq = - (L·M⁻¹·B)⁻¹ · (L·M⁻¹·C + ds/dt)

    where s is the terminal sliding surface.
    """
    if self.dyn is None:
        return 0.0  # No model available

    # Get system matrices
    M = self.dyn.mass_matrix(state)
    C = self.dyn.coriolis_centrifugal(state)
    B = self.dyn.control_matrix()

    # Compute L (gradient of sliding surface w.r.t. state)
    L = self.compute_surface_gradient(state)

    # Solve for u_eq (requires matrix operations)
    try:
        M_inv = np.linalg.inv(M)
        LMB = L @ M_inv @ B
        if abs(LMB) < 1e-6:  # Singularity check
            return 0.0

        u_eq = -(1 / LMB) * (L @ M_inv @ C)
        return saturate(u_eq, -self.max_force, self.max_force)

    except np.linalg.LinAlgError:
        return 0.0  # Fallback to robust control only