# Example from: docs\issue_11_lyapunov_robustness_resolution.md
# Index: 9
# Runnable: True
# Hash: 4c6bed94

from src.analysis.performance.stability_analysis import StabilityAnalyzer, StabilityAnalysisConfig

# Initialize analyzer
config = StabilityAnalysisConfig(eigenvalue_tolerance=1e-10)
analyzer = StabilityAnalyzer(config=config)

# Analyze system stability
A = np.array([[-1.0, 0.5], [0.0, -2.0]])
result = analyzer._analyze_analytical_lyapunov(A)

print(f"Stable: {result['is_stable']}")
print(f"Positive definite: {result['is_positive_definite']}")
print(f"Residual: {result['residual_relative']:.2e}")