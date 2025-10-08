# Example from: docs\reports\DOCUMENTATION_EXPERT_TECHNICAL_ASSESSMENT_REPORT.md
# Index: 1
# Runnable: True
# Hash: 8d216348

# Example: Classical SMC Configuration
"""
Type-safe configuration for Classical SMC controller.

Based on SMC theory requirements:
- Surface gains [k1, k2, λ1, λ2] must be positive for Hurwitz stability
- Switching gain K must be positive for reaching condition
- Derivative gain kd must be non-negative for damping
"""