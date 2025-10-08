# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 11
# Runnable: True
# Hash: dafd5537

@pytest.fixture(scope="function")
def fresh_controller():
    """New controller instance per benchmark"""
    return ClassicalSMC(gains=[10, 5, 8, 3, 15, 2])