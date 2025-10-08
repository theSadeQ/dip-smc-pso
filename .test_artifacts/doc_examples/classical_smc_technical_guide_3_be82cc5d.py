# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 3
# Runnable: True
# Hash: be82cc5d

L_Minv_B = L @ np.linalg.solve(M_reg, B)
if abs(L_Minv_B) < self.eq_threshold:
    return 0.0  # Disable equivalent control