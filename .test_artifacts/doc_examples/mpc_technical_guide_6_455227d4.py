# Example from: docs\controllers\mpc_technical_guide.md
# Index: 6
# Runnable: True
# Hash: 455227d4

θ_err = (θ₁ - π) + (θ₂ - π)
   θ̇_err = θ̇₁ + θ̇₂
   u = -k_p θ_err - k_d θ̇_err