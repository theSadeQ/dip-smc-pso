# Example from: docs\examples\mathematical_notation_standards.md
# Index: 6
# Runnable: False
# Hash: bd6f461a

# example-metadata:
# runnable: false

"""
Performance Metrics for Control Systems:

1. Integral Squared Error (ISE):
   ISE = ∫₀ᵀ ‖e(t)‖² dt

2. Integral Time Absolute Error (ITAE):
   ITAE = ∫₀ᵀ t·‖e(t)‖₁ dt

3. Integral Absolute Error (IAE):
   IAE = ∫₀ᵀ ‖e(t)‖₁ dt

4. Root Mean Square Error (RMSE):
   RMSE = √(1/T ∫₀ᵀ ‖e(t)‖² dt)

5. Maximum Overshoot:
   OS = max(x(t)) - x_final / x_final × 100%

6. Settling Time (2% criterion):
   t_s = inf{t > 0 : |x(τ) - x_final| ≤ 0.02|x_final| ∀τ ≥ t}
"""