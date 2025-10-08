# Example from: docs\examples\mathematical_notation_standards.md
# Index: 5
# Runnable: False
# Hash: c521b561

# example-metadata:
# runnable: false

"""
Multi-objective cost function for controller optimization:

J(k) = w₁·ISE(k) + w₂·ITAE(k) + w₃·U_max(k) + w₄·Penalty(k)

where:
- ISE(k) = ∫₀ᵀ ‖e(t,k)‖² dt (Integral Squared Error)
- ITAE(k) = ∫₀ᵀ t·‖e(t,k)‖₁ dt (Integral Time Absolute Error)
- U_max(k) = max_{t∈[0,T]} |u(t,k)| (Control effort penalty)
- Penalty(k): Instability penalty (→ ∞ if unstable)
- wᵢ ≥ 0: weighting factors with ∑wᵢ = 1
"""