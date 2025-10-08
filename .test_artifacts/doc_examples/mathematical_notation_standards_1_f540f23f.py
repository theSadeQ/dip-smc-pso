# Example from: docs\examples\mathematical_notation_standards.md
# Index: 1
# Runnable: False
# Hash: f540f23f

# example-metadata:
# runnable: false

"""
Classical SMC sliding surface definition:

s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂

where:
- e₁ = θ₁ - θ₁ᵈ (angular position error for pendulum 1)
- e₂ = θ₂ - θ₂ᵈ (angular position error for pendulum 2)
- ė₁ = θ̇₁ - θ̇₁ᵈ (angular velocity error for pendulum 1)
- ė₂ = θ̇₂ - θ̇₂ᵈ (angular velocity error for pendulum 2)
- λ₁, λ₂ > 0 (sliding surface gains for Hurwitz stability)

Stability Condition:
For exponential convergence to the sliding surface, require:
λ₁, λ₂ > 0 ensuring the characteristic polynomial s² + λ₂s + λ₁ = 0
has roots in the left half-plane.
"""