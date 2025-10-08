# Example from: docs\reports\PSO_OPTIMIZATION_ENGINEER_COMPREHENSIVE_ANALYSIS_REPORT.md
# Index: 1
# Runnable: True
# Hash: dec88ac1

# Core PSO Update Equations (Verified)
v[i](t+1) = w·v[i](t) + c₁·r₁·(pbest[i] - x[i](t)) + c₂·r₂·(gbest - x[i](t))
x[i](t+1) = x[i](t) + v[i](t+1)

# Advanced Fitness Function (Multi-Component)
J = w_ise·(ISE/norm_ise) + w_u·(U²/norm_u) + w_du·(dU²/norm_du) + w_σ·(σ²/norm_σ) + penalty