# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 23
# Runnable: False
# Hash: 027c3888

# Essential test pattern
def test_controller_return_type():
    controller = create_controller(...)
    result = controller.compute_control(...)

    # Explicit type validation
    assert result is not None
    assert isinstance(result, ExpectedType)
    assert hasattr(result, 'required_attribute')