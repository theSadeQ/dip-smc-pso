# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 13
# Runnable: False
# Hash: a6e0399d

# example-metadata:
# runnable: false

def generate_validation_tests(config_class, parameter_specs):
    """Generate comprehensive validation tests for configuration classes."""

    tests = []

    for param_name, spec in parameter_specs.items():
        if spec.get('positive_required', False):
            def test_positive_validation():
                invalid_config = create_invalid_config(param_name, -1.0)
                with pytest.raises(ValueError):
                    config_class(**invalid_config)

            tests.append(test_positive_validation)

        if spec.get('nonzero_required', False):
            def test_nonzero_validation():
                invalid_config = create_invalid_config(param_name, 0.0)
                with pytest.raises(ValueError):
                    config_class(**invalid_config)

            tests.append(test_nonzero_validation)

    return tests