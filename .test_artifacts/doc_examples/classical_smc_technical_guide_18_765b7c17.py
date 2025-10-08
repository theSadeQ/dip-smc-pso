# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 18
# Runnable: True
# Hash: 765b7c17

M, C, G = dynamics._compute_physics_matrices(state)
cond_number = np.linalg.cond(M)
if cond_number > 1e12:
    print(f"WARNING: Ill-conditioned M: κ = {cond_number:.2e}")