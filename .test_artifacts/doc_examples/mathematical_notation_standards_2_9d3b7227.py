# Example from: docs\examples\mathematical_notation_standards.md
# Index: 2
# Runnable: True
# Hash: 9d3b7227

"""
Lyapunov stability analysis for SMC reaching condition:

V(s) = ½s²

Taking the time derivative along system trajectories:
V̇(s) = s·ṡ = s·(λ₁ė₁ + λ₂ė₂ + ë₁ + ë₂)

For the reaching condition V̇ < 0 when s ≠ 0, the switching gain K must satisfy:
K > |f_eq(x)| + δ

where f_eq is the equivalent control and δ > 0 accounts for uncertainties.
"""