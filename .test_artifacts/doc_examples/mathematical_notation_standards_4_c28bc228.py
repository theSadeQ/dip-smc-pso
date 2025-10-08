# Example from: docs\examples\mathematical_notation_standards.md
# Index: 4
# Runnable: False
# Hash: c28bc228

"""
Particle Swarm Optimization update equations:

vᵢᵗ⁺¹ = w·vᵢᵗ + c₁r₁(pᵢ - xᵢᵗ) + c₂r₂(g - xᵢᵗ)
xᵢᵗ⁺¹ = xᵢᵗ + vᵢᵗ⁺¹

where:
- xᵢᵗ ∈ ℝⁿ: position of particle i at iteration t
- vᵢᵗ ∈ ℝⁿ: velocity of particle i at iteration t
- pᵢ ∈ ℝⁿ: personal best position of particle i
- g ∈ ℝⁿ: global best position
- w ∈ [0,1]: inertia weight
- c₁, c₂ > 0: acceleration coefficients
- r₁, r₂ ~ U(0,1): random variables

Convergence requires: w < 1 and c₁ + c₂ < 4(1 + w)
"""