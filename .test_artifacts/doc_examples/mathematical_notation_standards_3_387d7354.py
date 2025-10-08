# Example from: docs\examples\mathematical_notation_standards.md
# Index: 3
# Runnable: False
# Hash: 387d7354

"""
Second-order sliding mode (Super-Twisting) control law:

u = u₁ + u₂

where:
u₁ = -α|s|^(1/2)sign(s)
u₂ = ∫₀ᵗ(-β sign(s))dτ

Parameters α, β > 0 must satisfy the convergence condition:
α > √(2L), β > α²/(2(α-√(2L)))

where L is the Lipschitz constant of the uncertainty.
"""