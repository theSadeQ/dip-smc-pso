# Example from: docs\controllers\mpc_technical_guide.md
# Index: 1
# Runnable: True
# Hash: fae3e153

for i in range(n):
    δ = max(eps, 1e-4 * max(|x_eq[i]|, 1.0))
    A[:, i] = [f(x_eq + δeᵢ, u_eq) - f(x_eq - δeᵢ, u_eq)] / (2δ)

δ_u = max(eps, 1e-4 * max(|u_eq|, 1.0))
B = [f(x_eq, u_eq + δ_u) - f(x_eq, u_eq - δ_u)] / (2δ_u)