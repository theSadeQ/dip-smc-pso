# Example from: docs\testing\reports\2025-09-30\technical\control_theory_analysis.md
# Index: 5
# Runnable: True
# Hash: 1aa003ac

if κ(J) > condition_threshold:
    # Use pseudoinverse with SVD
    U, Σ, Vᵀ = SVD(J)
    Σ_reg = diag(max(σᵢ, ε) for σᵢ in Σ)
    J_pinv = V·Σ_reg⁻¹·Uᵀ