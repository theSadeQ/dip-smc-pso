# Example from: docs\test_infrastructure_documentation.md
# Index: 16
# Runnable: True
# Hash: fd40e60b

# Increase statistical power
@pytest.mark.statistical
@settings(max_examples=1000)  # Increase Hypothesis examples
def test_statistical_property():
    # Larger sample size for better statistical power
    pass