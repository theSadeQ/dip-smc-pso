# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 6
# Runnable: False
# Hash: 090ae63d

def _compute_equivalent_control(self, state: np.ndarray) -> float:
    """Compute model-based u_eq with enhanced robustness."""
    if self.dyn is None:
        return 0.0  # No dynamics model

    try:
        # Get physics matrices
        M, C, G = self.dyn._compute_physics_matrices(state)

        # Regularize inertia matrix
        M_reg = M + np.eye(3) * max(self.regularization, 0.0)

        # Solve for controllability scalar
        Minv_B = np.linalg.solve(M_reg, self.B)
        L_Minv_B = float(self.L @ Minv_B)

        # Check controllability
        if abs(L_Minv_B) < self.eq_threshold:
            return 0.0

        # Compute equivalent control
        q_dot = state[3:]
        if getattr(C, "ndim", 1) == 2:
            rhs = C @ q_dot + G
        else:
            rhs = C + G

        Minv_rhs = np.linalg.solve(M_reg, rhs)
        term1 = float(self.L @ Minv_rhs)
        term2 = self.k1 * self.lam1 * q_dot[1] + self.k2 * self.lam2 * q_dot[2]
        u_eq = (term1 - term2) / L_Minv_B

        return float(u_eq)

    except np.linalg.LinAlgError:
        return 0.0  # Singular matrix