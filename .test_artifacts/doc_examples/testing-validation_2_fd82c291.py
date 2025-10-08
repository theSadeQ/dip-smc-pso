# Example from: docs\guides\how-to\testing-validation.md
# Index: 2
# Runnable: False
# Hash: fd82c291

# example-metadata:
# runnable: false

@pytest.mark.parametrize("gains,expected_valid", [
    ([10, 8, 15, 12, 50, 5], True),   # Valid
    ([0, 8, 15, 12, 50, 5], False),   # k1 = 0 invalid
    ([-10, 8, 15, 12, 50, 5], False), # Negative gain
])
def test_gain_validation(gains, expected_valid):
    """Test gain validation with multiple cases."""
    if expected_valid:
        controller = MyController(gains=gains, max_force=100.0)
        assert controller.gains == gains
    else:
        with pytest.raises(ValueError):
            MyController(gains=gains, max_force=100.0)