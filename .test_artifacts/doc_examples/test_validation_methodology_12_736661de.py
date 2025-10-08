# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 12
# Runnable: False
# Hash: 736661de

# example-metadata:
# runnable: false

def generate_linearity_test(component_class, property_name):
    """Generate linearity test for any mathematical component."""

    def test_linearity(self):
        component = component_class(default_params)

        x1 = generate_random_input()
        x2 = generate_random_input()

        result1 = getattr(component, property_name)(x1)
        result2 = getattr(component, property_name)(x2)
        result_combined = getattr(component, property_name)(x1 + x2)

        assert np.allclose(result_combined, result1 + result2, rtol=1e-10)

    return test_linearity

def generate_monotonicity_test(function, domain):
    """Generate monotonicity test for mathematical functions."""

    def test_monotonicity(self):
        x_values = np.linspace(domain[0], domain[1], 100)
        y_values = [function(x) for x in x_values]

        # Check monotonicity
        for i in range(len(y_values) - 1):
            assert y_values[i+1] >= y_values[i]

    return test_monotonicity