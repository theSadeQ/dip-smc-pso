# Example from: docs\examples\mathematical_notation_standards.md
# Index: 8
# Runnable: False
# Hash: ce3b93ab

"""
Welch's t-test for comparing controller performance:

H₀: μ₁ = μ₂ (no difference in mean performance)
H₁: μ₁ ≠ μ₂ (significant difference in performance)

Test Statistic:
t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)

Degrees of Freedom (Welch-Satterthwaite):
ν = (s₁²/n₁ + s₂²/n₂)² / ((s₁²/n₁)²/(n₁-1) + (s₂²/n₂)²/(n₂-1))

Reject H₀ if |t| > t_{ν,α/2} where α is the significance level.
"""