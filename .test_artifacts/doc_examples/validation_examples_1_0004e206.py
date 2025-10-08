# Example from: docs\validation\validation_examples.md
# Index: 1
# Runnable: False
# Hash: 0004e206

# Required imports (add to your script)
import numpy as np
from src.analysis.validation.monte_carlo import MonteCarloConfig, MonteCarloAnalyzer
from src.analysis.validation.cross_validation import CrossValidationConfig, CrossValidator
from src.analysis.validation.statistical_tests import StatisticalTestConfig, StatisticalTestSuite
from src.analysis.validation.benchmarking import BenchmarkConfig, BenchmarkSuite