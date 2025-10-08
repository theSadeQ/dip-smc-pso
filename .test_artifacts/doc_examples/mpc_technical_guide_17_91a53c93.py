# Example from: docs\controllers\mpc_technical_guide.md
# Index: 17
# Runnable: True
# Hash: 91a53c93

# Custom PD fallback (if SMC unavailable)
mpc = MPCController(
    dynamics,
    fallback_pd_gains=(30.0, 10.0)  # (k_p, k_d)
)