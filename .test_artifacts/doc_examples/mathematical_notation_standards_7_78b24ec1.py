# Example from: docs\examples\mathematical_notation_standards.md
# Index: 7
# Runnable: False
# Hash: 78b24ec1

"""
Monte Carlo Uncertainty Quantification:

Given N independent samples {J₁, J₂, ..., Jₙ} of the cost function:

Sample Mean: μ̂ = 1/N ∑ᵢ₌₁ᴺ Jᵢ

Sample Variance: σ̂² = 1/(N-1) ∑ᵢ₌₁ᴺ (Jᵢ - μ̂)²

Confidence Interval (α = 0.05):
CI₀.₉₅ = μ̂ ± t_{N-1,α/2} · σ̂/√N

where t_{N-1,α/2} is the (1-α/2) quantile of the t-distribution with N-1 degrees of freedom.
"""