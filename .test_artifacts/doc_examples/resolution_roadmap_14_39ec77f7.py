# Example from: docs\testing\reports\2025-09-30\technical\resolution_roadmap.md
# Index: 14
# Runnable: False
# Hash: 39ec77f7

# File: pytest.ini
[tool:pytest]
markers =
    integration: Integration tests requiring full system
    slow: Slow tests (>10 seconds)
    memory: Memory-intensive tests
    numerical: Numerical stability tests
    hardware: Hardware-in-loop tests
    benchmark: Performance benchmark tests
    smoke: Quick smoke tests for CI
    regression: Regression prevention tests

# Test timeout and memory limits
timeout = 300
maxfail = 5